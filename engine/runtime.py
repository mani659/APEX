from typing import List, Optional
import time
from engine.core.market_data import MarketDataLayer, MarketSnapshot
from engine.core.signal_observation import SignalObservation
from engine.core.context_interpretation import ContextInterpretation, ParticipationState
from engine.core.execution_permission import ExecutionPermission, PermissionState
from engine.core.capital_allocation import CapitalAllocation
from engine.core.execution_engine import ExecutionEngine, OrderDirection, Position
from engine.core.inventory_management import InventoryManagement, InventoryDecision
from engine.core.experimental_exits import ExperimentalExitManager, ExperimentalConfig, ExperimentalExitDecision
from engine.telemetry import TelemetryLayer
import uuid

class ApexRuntime:
    def __init__(self, telemetry: TelemetryLayer = None, symbol: str = "UNKNOWN", mode: str = "NORMAL", exit_config: Optional[ExperimentalConfig] = None):
        self.market_data = MarketDataLayer()
        self.signal_obs = SignalObservation()
        self.context_interp = ContextInterpretation()
        self.exec_perm = ExecutionPermission()
        self.cap_alloc = CapitalAllocation()
        self.exec_engine = ExecutionEngine()
        self.inv_mgmt = InventoryManagement()
        
        self.mode = mode
        self.experimental_exits = ExperimentalExitManager(exit_config) if exit_config else None
        
        self.telemetry = telemetry if telemetry else TelemetryLayer()
        self.symbol = symbol
        self.active_positions: List[Position] = []
        
        # State machine
        self.is_waiting_stabilization = False
        self.wait_bars_count = 0
        self.current_trace_id = None

    def on_tick(self, price: float, ts: str = None):
        snapshot = self.market_data.update_tick(price)
        self._process_cycle(snapshot, ts)
        
    def on_bar(self, o: float, h: float, l: float, c: float, v: float, ts: str = None):
        snapshot = self.market_data.update_bar(o, h, l, c, v)
        if self.is_waiting_stabilization:
            self.wait_bars_count += 1
        self._process_cycle(snapshot, ts)

    def _process_cycle(self, snapshot: MarketSnapshot, ts: str):
        if ts is None:
            ts = str(time.time())
            
        try:
            if self.mode == "ENTRY_ISOLATION":
                self._process_cycle_isolation(snapshot, ts)
            else:
                self._process_cycle_normal(snapshot, ts)
        except Exception as e:
            self.telemetry.emit(
                trace_id=self.current_trace_id or "NONE", ts=ts, symbol=self.symbol,
                module="ApexRuntime", layer="Runtime", event_type="ERROR",
                decision_state="ERROR",
                context={"error": str(e), "mode": self.mode}
            )

    def _process_cycle_normal(self, snapshot: MarketSnapshot, ts: str):
        # 1. Observe
        if not self.is_waiting_stabilization:
            event_triggered = self.signal_obs.detect_behavioral_event(snapshot)
            if not event_triggered:
                self._run_inventory(snapshot, ts)
                return
            
            # We have a behavioral event! Mint a Trace ID.
            self.current_trace_id = f"{self.symbol}_{ts}_{uuid.uuid4().hex[:8]}"
            
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="SignalObservation", layer="Observation", event_type="EVENT_DETECTED",
                decision_state="OBSERVED",
                context={"atr": snapshot.current_atr}
            )
            
            # 2. Interpret
            part_state = self.context_interp.evaluate_participation_state(snapshot, True)
            if part_state == ParticipationState.HIGH_ENTROPY:
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ContextInterpretation", layer="Interpretation", event_type="REJECT_HIGH_ENTROPY",
                    decision_state="REJECT",
                    context={"entropy": "high"}
                )
                self._run_inventory(snapshot, ts)
                self.current_trace_id = None
                return
            else:
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ContextInterpretation", layer="Interpretation", event_type="LOW_ENTROPY",
                    decision_state="PASS",
                    context={"entropy": "low"}
                )
                
            self.is_waiting_stabilization = True
            self.wait_bars_count = 0
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="WAIT",
                decision_state="WAIT",
                context={"wait_counter": self.wait_bars_count}
            )
            
        # 3. Permission
        current_part_state = self.context_interp.evaluate_participation_state(snapshot, True)
        perm_state = self.exec_perm.confirm_stabilization(snapshot, current_part_state)
        if perm_state == PermissionState.REJECT:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="REJECT_PERMISSION",
                decision_state="REJECT",
                context={"reason": "Permission Denied"}
            )
            self.is_waiting_stabilization = False
            self.current_trace_id = None
            self._run_inventory(snapshot, ts)
            return
        elif perm_state == PermissionState.WAIT:
            if self.wait_bars_count > 5: # Timeout
                self.is_waiting_stabilization = False
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ExecutionPermission", layer="Permission", event_type="REJECT_TIMEOUT",
                    decision_state="REJECT",
                    context={"wait_counter": self.wait_bars_count}
                )
                self.current_trace_id = None
            self._run_inventory(snapshot, ts)
            return
        else:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="EXECUTE",
                decision_state="PASS",
                context={"wait_counter": self.wait_bars_count}
            )
            
        # 4. Allocation (Execute)
        self.is_waiting_stabilization = False
        grid_dist = self.cap_alloc.calculate_grid_spacing(snapshot.current_atr, len(self.active_positions))
        
        self.telemetry.emit(
            trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
            module="CapitalAllocation", layer="Allocation", event_type="GRID_CALCULATED",
            decision_state="PASS",
            context={"inventory_size": len(self.active_positions), "grid_distance": grid_dist}
        )
        
        last_close = snapshot.closes[-1] if snapshot.closes else snapshot.current_price
        direction = OrderDirection.BUY if snapshot.current_price < last_close else OrderDirection.SELL
        
        pos = self.exec_engine.execute_trade(direction, snapshot.current_price, grid_dist)
        pos.trace_id = self.current_trace_id
        self.active_positions.append(pos)
        
        self.telemetry.emit(
            trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
            module="ExecutionEngine", layer="Execution", event_type="ORDER_ACCEPTED",
            decision_state="EXECUTE",
            context={"direction": direction.name, "entry_price": pos.entry_price, "volume": pos.volume, "ticket": pos.ticket}
        )
        
        if len(self.active_positions) == 1:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="InventoryManagement", layer="Inventory", event_type="BASKET_CREATED",
                decision_state="PASS",
                context={"basket_size": 1}
            )
        else:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="InventoryManagement", layer="Inventory", event_type="BASKET_EXPANDED",
                decision_state="PASS",
                context={"basket_size": len(self.active_positions)}
            )
        
        # Reset current trace since the basket inherited it.
        self.current_trace_id = None
        
        # 5. Inventory
        self._run_inventory(snapshot, ts)

    def _process_cycle_isolation(self, snapshot: MarketSnapshot, ts: str):
        # 0. Single-position enforcement: if we have a position, ignore new behavioural signals and just evaluate exit
        if len(self.active_positions) >= 1:
            self._run_experimental_exits(snapshot, ts)
            return

        # 1. Observe
        if not self.is_waiting_stabilization:
            event_triggered = self.signal_obs.detect_behavioral_event(snapshot)
            if not event_triggered:
                return  # No active positions to manage
            
            # We have a behavioral event! Mint a Trace ID.
            self.current_trace_id = f"{self.symbol}_{ts}_{uuid.uuid4().hex[:8]}"
            
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="SignalObservation", layer="Observation", event_type="EVENT_DETECTED",
                decision_state="OBSERVED",
                context={"atr": snapshot.current_atr, "mode": "ENTRY_ISOLATION"}
            )
            
            # 2. Interpret
            part_state = self.context_interp.evaluate_participation_state(snapshot, True)
            if part_state == ParticipationState.HIGH_ENTROPY:
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ContextInterpretation", layer="Interpretation", event_type="REJECT_HIGH_ENTROPY",
                    decision_state="REJECT",
                    context={"entropy": "high"}
                )
                self.current_trace_id = None
                return
            else:
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ContextInterpretation", layer="Interpretation", event_type="LOW_ENTROPY",
                    decision_state="PASS",
                    context={"entropy": "low"}
                )
                
            self.is_waiting_stabilization = True
            self.wait_bars_count = 0
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="WAIT",
                decision_state="WAIT",
                context={"wait_counter": self.wait_bars_count}
            )
            
        # 3. Permission
        current_part_state = self.context_interp.evaluate_participation_state(snapshot, True)
        perm_state = self.exec_perm.confirm_stabilization(snapshot, current_part_state)
        if perm_state == PermissionState.REJECT:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="REJECT_PERMISSION",
                decision_state="REJECT",
                context={"reason": "Permission Denied"}
            )
            self.is_waiting_stabilization = False
            self.current_trace_id = None
            return
        elif perm_state == PermissionState.WAIT:
            if self.wait_bars_count > 5: # Timeout
                self.is_waiting_stabilization = False
                self.telemetry.emit(
                    trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                    module="ExecutionPermission", layer="Permission", event_type="REJECT_TIMEOUT",
                    decision_state="REJECT",
                    context={"wait_counter": self.wait_bars_count}
                )
                self.current_trace_id = None
            return
        else:
            self.telemetry.emit(
                trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
                module="ExecutionPermission", layer="Permission", event_type="EXECUTE",
                decision_state="PASS",
                context={"wait_counter": self.wait_bars_count}
            )
            
        # 4. Execution (Isolated)
        self.is_waiting_stabilization = False
        
        last_close = snapshot.closes[-1] if snapshot.closes else snapshot.current_price
        direction = OrderDirection.BUY if snapshot.current_price < last_close else OrderDirection.SELL
        
        pos = self.exec_engine.execute_trade(direction, snapshot.current_price, 0.0) # grid_dist = 0 in isolation
        pos.trace_id = self.current_trace_id
        self.active_positions.append(pos)
        
        self.telemetry.emit(
            trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
            module="ExecutionEngine", layer="Execution", event_type="ORDER_ACCEPTED",
            decision_state="EXECUTE",
            context={"direction": direction.name, "entry_price": pos.entry_price, "volume": pos.volume, "ticket": pos.ticket}
        )
        
        self.telemetry.emit(
            trace_id=self.current_trace_id, ts=ts, symbol=self.symbol,
            module="InventoryManagement", layer="Inventory", event_type="BASKET_CREATED",
            decision_state="PASS",
            context={"basket_size": 1, "mode": "ENTRY_ISOLATION"}
        )
        
        # Initialize experimental exit state
        if self.experimental_exits:
            self.experimental_exits.initialize_state(pos, snapshot.current_atr)
        
        self.current_trace_id = None
        
        # 5. Inventory bypass: evaluate immediately
        self._run_experimental_exits(snapshot, ts)

    def _run_experimental_exits(self, snapshot: MarketSnapshot, ts: str):
        if not self.active_positions or not self.experimental_exits:
            return
            
        pos = self.active_positions[0] # Single-position enforcement guarantees this is length 1
        decision, reason = self.experimental_exits.evaluate(pos, snapshot.current_price)
        
        if decision == ExperimentalExitDecision.EXIT:
            state = self.experimental_exits.states.get(pos.ticket)
            mae = state.mae if state else 0.0
            mfe = state.mfe if state else 0.0
            bars_held = state.bars_held if state else 0
            
            self.telemetry.emit(
                trace_id=pos.trace_id, ts=ts, symbol=self.symbol,
                module="ExperimentalExits", layer="Inventory", event_type="BASKET_CLOSED",
                decision_state="TERMINATE",
                context={
                    "basket_size": 1, 
                    "exit_reason": reason, 
                    "exit_price": snapshot.current_price,
                    "mae": mae,
                    "mfe": mfe,
                    "bars_held": bars_held
                }
            )
            
            self.experimental_exits.clear_state(pos)
            self.active_positions.clear()

    def _run_inventory(self, snapshot: MarketSnapshot, ts: str):
        if not self.active_positions:
            return
            
        decision = self.inv_mgmt.manage_inventory(self.active_positions, snapshot.current_price, snapshot.current_atr, time.time())
        if decision in (InventoryDecision.EXIT_PROFIT, InventoryDecision.AGING_EXIT):
            for pos in self.active_positions:
                self.telemetry.emit(
                    trace_id=pos.trace_id, ts=ts, symbol=self.symbol,
                    module="InventoryManagement", layer="Inventory", event_type="BASKET_CLOSED",
                    decision_state="TERMINATE",
                    context={"basket_size": len(self.active_positions), "exit_reason": decision.name, "exit_price": snapshot.current_price}
                )
            self.active_positions.clear()
