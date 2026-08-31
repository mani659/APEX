import os
import pandas as pd
from pathlib import Path
import databento

def run_recovery():
    print("Initializing recovery...")
    key = os.environ.get("DATABENTO_API_KEY")
    if not key:
        key_file = Path("DATABENTO_API_KEY.md")
        if key_file.exists():
            key = key_file.read_text().strip()
    if not key:
        print("API KEY NOT FOUND")
        return

    client = databento.Historical(key=key)

    requests = [
        {
            "id": "2022-04-27",
            "start": "2022-04-27T00:00:00",
            "end": "2022-04-28T00:00:00",
            "symbols": ["591595", "403252", "11232"]
        },
        {
            "id": "2025-12-24",
            "start": "2025-12-24T18:45:00",
            "end": "2025-12-25T00:00:00",
            "symbols": ["42419356", "42299839", "57062"]
        },
        {
            "id": "2025-12-31",
            "start": "2025-12-31T21:59:58",
            "end": "2026-01-01T00:00:00",
            "symbols": ["42566521", "42193907", "42713270", "42764677", "57062"]
        }
    ]

    total_cost = 0.0
    for req in requests:
        try:
            cost = client.metadata.get_cost(
                dataset="GLBX.MDP3",
                start=req["start"],
                end=req["end"],
                symbols=req["symbols"],
                schema="bbo-1m",
                stype_in="instrument_id"
            )
            req["cost"] = cost
            total_cost += cost
            print(f"Cost for {req['id']}: ${cost:.4f}")
        except Exception as e:
            print(f"Error getting cost for {req['id']}: {e}")
            req["cost"] = 0.0

    print(f"Total Estimated Recovery Cost: ${total_cost:.4f}")

    if total_cost > 5.0:
        print("COST ABNORMALLY HIGH. STOPPING.")
        return

    recovery_dir = Path("data/databento/rc015_stage2_recovery")
    recovery_dir.mkdir(parents=True, exist_ok=True)

    for req in requests:
        out_file = recovery_dir / f"recovery_{req['id']}.dbn"
        if out_file.exists():
            print(f"File {out_file} already exists. Skipping download.")
            continue
            
        print(f"Downloading {req['id']}...")
        try:
            store = client.timeseries.get_range(
                dataset="GLBX.MDP3",
                start=req["start"],
                end=req["end"],
                symbols=req["symbols"],
                schema="bbo-1m",
                stype_in="instrument_id",
                path=out_file
            )
            df = store.to_df()
            print(f"Downloaded {len(df)} rows for {req['id']}")
        except Exception as e:
            print(f"Download failed for {req['id']}: {e}")

if __name__ == "__main__":
    run_recovery()
