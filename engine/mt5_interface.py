class MT5Interface:
    def __init__(self, symbol: str = 'XAUUSD'):
        self.symbol = symbol
        self.connected = False

    def connect(self) -> bool:
        # Dummy connection for reference engine
        self.connected = True
        return True

    def get_latest_tick(self):
        if not self.connected:
            raise ConnectionError("Not connected to MT5")
        return 0.0

    def get_historical_bars(self, count: int):
        if not self.connected:
            raise ConnectionError("Not connected to MT5")
        return []

    def send_order(self, direction, volume, price):
        pass

    def shutdown(self):
        self.connected = False
