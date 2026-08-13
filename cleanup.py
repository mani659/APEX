import os
import glob
import shutil

repo_root = r"d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex"

def get_dir_size(start_path):
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                file_count += 1
    return total_size, file_count

def format_size(size):
    return f"{size / (1024*1024):.2f} MB"

def main():
    pre_size, pre_count = get_dir_size(repo_root)
    print(f"PRE-CLEANUP: {pre_count} files, {format_size(pre_size)}")
    
    rc009_size = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        for f in filenames:
            if 'rc009' in f.lower():
                rc009_size += os.path.getsize(os.path.join(dirpath, f))
    print(f"RC009 artifacts size: {format_size(rc009_size)}")

    files_deleted = 0
    bytes_recovered = 0

    def delete_file(path):
        nonlocal files_deleted, bytes_recovered
        if os.path.exists(path):
            size = os.path.getsize(path)
            os.remove(path)
            files_deleted += 1
            bytes_recovered += size
            print(f"DELETED: {path}")

    def delete_dir(path):
        nonlocal files_deleted, bytes_recovered
        if os.path.exists(path) and os.path.isdir(path):
            s, c = get_dir_size(path)
            shutil.rmtree(path)
            files_deleted += c
            bytes_recovered += s
            print(f"DELETED DIR: {path}")

    # 1. __pycache__ and .pyc
    for dirpath, dirnames, filenames in list(os.walk(repo_root)):
        if '__pycache__' in dirnames:
            delete_dir(os.path.join(dirpath, '__pycache__'))
            dirnames.remove('__pycache__')
        for f in filenames:
            if f.endswith('.pyc'):
                delete_file(os.path.join(dirpath, f))

    # 2. Temporary texts and scripts
    for f in glob.glob(os.path.join(repo_root, "reports", "Development_Status_*.txt")):
        delete_file(f)
    for f in glob.glob(os.path.join(repo_root, "reports", "ProjectAudit_*.txt")):
        delete_file(f)
    
    delete_file(os.path.join(repo_root, "dummy.txt"))
    delete_file(os.path.join(repo_root, "tmp_probe.py"))
    delete_file(os.path.join(repo_root, "reports", "analyze_005.py"))

    # 3. Intermediate RC009 Parquets
    delete_file(os.path.join(repo_root, "reports", "RC009_Study_003_Sequence_Dataset.parquet"))
    delete_file(os.path.join(repo_root, "reports", "RC009_Study_004_Cross_Market_Dataset.parquet"))
    delete_file(os.path.join(repo_root, "reports", "RC009_Study_006_HTF_Regime_Dataset.parquet"))
    
    print(f"\nFiles deleted: {files_deleted}")
    print(f"Space recovered: {format_size(bytes_recovered)}")
    
    post_size, post_count = get_dir_size(repo_root)
    print(f"POST-CLEANUP: {post_count} files, {format_size(post_size)}")

if __name__ == '__main__':
    main()
