import os
import glob
import subprocess
import hashlib
import json
import time
import psutil
from simulation.qualification_worker import run_simulation

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def qualify_platform():
    data_dir = r"d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex\data\m1"
    datasets = glob.glob(os.path.join(data_dir, "*.parquet"))
    
    report = {
        "repeatability": [],
        "reproducibility": [],
        "dataset_integrity": [],
        "performance_stability": []
    }
    
    os.makedirs('qualification_logs', exist_ok=True)
    
    # ---------------------------------------------------------
    # TEST 1 & 6 & 7: Same Process Repeatability (5 runs on XAUUSD)
    # ---------------------------------------------------------
    target_dataset = os.path.join(data_dir, "XAUUSD_M1.parquet")
    print("Running Test 1 (Repeatability - Same Process)...")
    
    same_process_hashes = []
    mem_usage = []
    cpu_times = []
    
    process = psutil.Process(os.getpid())
    
    for i in range(5):
        log_file = f"qualification_logs/run_sp_{i}.log"
        
        t0 = time.time()
        # Call the simulation inline (same memory space)
        run_simulation(target_dataset, log_file)
        t1 = time.time()
        
        mem_mb = process.memory_info().rss / (1024 * 1024)
        mem_usage.append(mem_mb)
        cpu_times.append(t1 - t0)
        
        h = hash_file(log_file)
        same_process_hashes.append(h)
        print(f"  Run {i}: Hash={h}, Time={t1-t0:.2f}s, Mem={mem_mb:.1f}MB")
        
    report["repeatability"] = {
        "hashes": same_process_hashes,
        "is_deterministic": len(set(same_process_hashes)) == 1
    }
    
    report["performance_stability"] = {
        "cpu_times": cpu_times,
        "memory_mb": mem_usage,
        "memory_leak_detected": mem_usage[-1] > mem_usage[0] * 1.5 # Arbitrary generous threshold
    }

    # ---------------------------------------------------------
    # TEST 2: Reproducibility (5 Isolated Subprocesses)
    # ---------------------------------------------------------
    print("\nRunning Test 2 (Reproducibility - Isolated Processes)...")
    isolated_hashes = []
    
    for i in range(5):
        log_file = f"qualification_logs/run_iso_{i}.log"
        cmd = ["python", "simulation/qualification_worker.py", target_dataset, log_file]
        subprocess.run(cmd, check=True, capture_output=True)
        
        h = hash_file(log_file)
        isolated_hashes.append(h)
        print(f"  Subprocess {i}: Hash={h}")
        
    report["reproducibility"] = {
        "hashes": isolated_hashes,
        "is_deterministic": len(set(isolated_hashes)) == 1,
        "matches_same_process": isolated_hashes[0] == same_process_hashes[0]
    }

    # ---------------------------------------------------------
    # TEST 3, 4, 5: Dataset Integrity across all Canonical Parquets
    # ---------------------------------------------------------
    print("\nRunning Test 3 (Dataset Integrity - All Datasets)...")
    for ds in datasets:
        ds_name = os.path.basename(ds)
        log_file = f"qualification_logs/run_{ds_name}.log"
        
        t0 = time.time()
        run_simulation(ds, log_file)
        t1 = time.time()
        
        h = hash_file(log_file)
        print(f"  Dataset {ds_name}: Hash={h}, Time={t1-t0:.2f}s")
        report["dataset_integrity"].append({
            "dataset": ds_name,
            "hash": h,
            "time": t1-t0
        })

    # Output JSON report
    report_path = r"C:\Users\User10\.gemini\antigravity-ide\brain\1b73ef8e-c034-4d4f-9ea6-ffe8c7aa8368\qualification_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print("\nQualification run complete. Report saved.")

if __name__ == '__main__':
    qualify_platform()
