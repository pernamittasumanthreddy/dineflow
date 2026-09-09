"""
TrainPlex Compliance Verifier and Packaging Utility.
Counts prod LOC, commits, pull requests, and packages dineflow into a zip with .git included.
"""

import os
import sys
import subprocess
import zipfile

BASE_DIR = r"c:\Users\BABI\Desktop\dineflow"
ZIP_OUTPUT = r"c:\Users\BABI\Desktop\dineflow_trainplex_submission.zip"

def count_prod_loc():
    out = subprocess.run(['git', 'ls-files'], cwd=BASE_DIR, capture_output=True, text=True).stdout.splitlines()
    total_lines = 0
    by_ext = {}
    valid_exts = {'.py', '.html', '.css', '.js', '.sql'}
    
    for f in out:
        if f.startswith('tests/') or f.startswith('docs/') or f.endswith('.md') or f.endswith('.sqlite3'):
            continue
        ext = os.path.splitext(f)[1]
        if ext in valid_exts:
            full_p = os.path.join(BASE_DIR, f)
            try:
                with open(full_p, 'r', encoding='utf-8', errors='ignore') as fp:
                    lines = sum(1 for _ in fp)
                    total_lines += lines
                    by_ext[ext] = by_ext.get(ext, 0) + lines
            except Exception:
                pass
    return total_lines, by_ext

def count_commits():
    out = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], cwd=BASE_DIR, capture_output=True, text=True).stdout.strip()
    return int(out) if out.isdigit() else 0

def count_prs():
    out = subprocess.run(['git', 'log', '--merges', '--oneline'], cwd=BASE_DIR, capture_output=True, text=True).stdout.strip().splitlines()
    return len(out)

def create_submission_zip():
    print(f"Creating TrainPlex submission zip at {ZIP_OUTPUT} (including .git)...")
    if os.path.exists(ZIP_OUTPUT):
        os.remove(ZIP_OUTPUT)
        
    excluded_dirs = {'venv', '.venv', '.ruff_cache', '__pycache__'}
    
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file.endswith('.pyc') or file == 'db.sqlite3.bak':
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                zf.write(full_path, rel_path)
                
    zip_size_mb = os.path.getsize(ZIP_OUTPUT) / (1024 * 1024)
    print(f"Successfully packaged {ZIP_OUTPUT} ({zip_size_mb:.2f} MB)")
    return ZIP_OUTPUT

def main():
    print("=== TrainPlex Compliance Verification ===")
    loc, by_ext = count_prod_loc()
    commits = count_commits()
    prs = count_prs()

    print(f"1. Production Lines of Code: {loc:,}")
    for ext, count in sorted(by_ext.items(), key=lambda x: -x[1]):
        print(f"   - {ext}: {count:,} lines")
    print(f"2. Total Git Commits: {commits}")
    print(f"3. Total Pull Requests (Merges): {prs}")

    # Validation against standards
    passed_loc = loc >= 50000
    passed_target_loc = loc >= 600000
    passed_commits = commits >= 100
    passed_prs = prs >= 90

    print("\n=== Validation Results ===")
    print(f"TrainPlex Minimum (50,000+ LOC): {'PASS' if passed_loc else 'FAIL'}")
    print(f"User Target (600,000+ LOC / 6 Lakhs): {'PASS' if passed_target_loc else 'FAIL'}")
    print(f"Commits (100+ required): {'PASS' if passed_commits else 'FAIL'}")
    print(f"Pull Requests (90 required): {'PASS' if passed_prs else 'FAIL'}")

if __name__ == '__main__':
    main()
