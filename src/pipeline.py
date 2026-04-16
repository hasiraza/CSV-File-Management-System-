"""
src/pipeline.py
───────────────
CSV File Management Agent — Full Pipeline
Author : Muhammad Haseeb (F2024332157, Section D3)
Version: 1.0.0
"""

import os
import csv
import shutil
import time
import json
import argparse
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIG  (mirrors .env defaults)
# ─────────────────────────────────────────
OUTPUT_FOLDER    = os.getenv("OUTPUT_FOLDER",    "Output")
MASTER_FILE      = os.getenv("MASTER_FILE",      "master.csv")
NUM_SUBLISTS     = int(os.getenv("NUM_SUBLISTS", 10))
RANGE_START      = int(os.getenv("NUM_RANGE_START", 1))
RANGE_END        = int(os.getenv("NUM_RANGE_END",  101))
FILES_PER_FOLDER = int(os.getenv("FILES_PER_FOLDER", 3))
LOG_FILE         = os.getenv("LOG_FILE", "data/memories/run.log")

result = {
    "status": "running",
    "steps_completed": 0,
    "total_rows_updated": 0,
    "duration_seconds": 0,
    "errors": [],
    "timestamp": datetime.now().isoformat(),
}

# ─────────────────────────────────────────
#  LOGGER
# ─────────────────────────────────────────
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg: str, level: str = "INFO"):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as lf:
        lf.write(line + "\n")


# ═══════════════════════════════════════════════════════════
#  STEP 1 — Data Generation
# ═══════════════════════════════════════════════════════════
def step1_generate_data():
    log("STEP 1 ▶ Generating list X and sublists")
    x = list(range(RANGE_START, RANGE_END))
    chunk = len(x) // NUM_SUBLISTS
    sublists = [x[i:i+chunk] for i in range(0, len(x), chunk)][:NUM_SUBLISTS]
    log(f"  List X: {len(x)} items | {len(sublists)} sublists of ~{chunk}")
    return x, sublists


# ═══════════════════════════════════════════════════════════
#  STEP 2 — File Writing
# ═══════════════════════════════════════════════════════════
def step2_write_files(x, sublists):
    log("STEP 2 ▶ Creating Output folder, master.csv, and sublist CSVs")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # master.csv
    master_path = os.path.join(OUTPUT_FOLDER, MASTER_FILE)
    with open(master_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "square"])
        for num in x:
            writer.writerow([num])
    log(f"  Created: {master_path}")

    # csv_N.csv files
    for i, sublist in enumerate(sublists, start=1):
        path = os.path.join(OUTPUT_FOLDER, f"csv_{i}.csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["X"])
            for val in sublist:
                writer.writerow([val])
        log(f"  Created: {path}")


# ═══════════════════════════════════════════════════════════
#  STEP 3 — Folder Organization
# ═══════════════════════════════════════════════════════════
def step3_organize_folders():
    log("STEP 3 ▶ Creating folders and distributing CSV files")

    files = list(range(1, NUM_SUBLISTS + 1))
    n = len(files)
    folder_assignments = [
        [files[(i + j) % n] for j in range(FILES_PER_FOLDER)]
        for i in range(n)
    ]

    for i, combo in enumerate(folder_assignments, start=1):
        folder_path = os.path.join(OUTPUT_FOLDER, f"folder_{i}")
        os.makedirs(folder_path, exist_ok=True)
        for file_num in combo:
            src = os.path.join(OUTPUT_FOLDER, f"csv_{file_num}.csv")
            dst = os.path.join(folder_path,   f"csv_{file_num}.csv")
            if os.path.exists(src):
                shutil.copy(src, dst)
                log(f"  Copied csv_{file_num}.csv → folder_{i}/")
            else:
                log(f"  WARN: {src} not found — skipped", "WARNING")

    return folder_assignments


# ═══════════════════════════════════════════════════════════
#  STEP 4 — Cleanup Root CSV Files
# ═══════════════════════════════════════════════════════════
def step4_cleanup():
    log("STEP 4 ▶ Removing root-level csv_N.csv files")
    for i in range(1, NUM_SUBLISTS + 1):
        path = os.path.join(OUTPUT_FOLDER, f"csv_{i}.csv")
        if os.path.exists(path):
            os.remove(path)
            log(f"  Deleted: {path}")


# ═══════════════════════════════════════════════════════════
#  STEP 5 — CSV Processing (search + compute squares)
# ═══════════════════════════════════════════════════════════
def find_file(filename, folders):
    for folder in folders:
        path = os.path.join(OUTPUT_FOLDER, folder, filename)
        if os.path.exists(path):
            return path
    return None

def step5_process_csvs():
    log("STEP 5 ▶ Reading CSV files and computing squares")

    folders = sorted([
        d for d in os.listdir(OUTPUT_FOLDER)
        if os.path.isdir(os.path.join(OUTPUT_FOLDER, d))
    ])

    number_to_square = {}

    for i in range(1, NUM_SUBLISTS + 2):   # +2 catches the intentional missing csv_11
        filename  = f"csv_{i}.csv"
        file_path = find_file(filename, folders)

        if file_path:
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    num = int(row["X"])
                    number_to_square[num] = num ** 2
            log(f"  Processed: {filename} ({len(number_to_square)} entries so far)")
        else:
            log(f"  SKIP: {filename} not found in any folder", "WARNING")

    return number_to_square


# ═══════════════════════════════════════════════════════════
#  STEP 6 — Update master.csv
# ═══════════════════════════════════════════════════════════
def step6_update_master(number_to_square):
    log("STEP 6 ▶ Updating master.csv with computed squares")

    master_path = os.path.join(OUTPUT_FOLDER, MASTER_FILE)

    with open(master_path, "r") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    with open(master_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["number", "square"])
        writer.writeheader()
        for row in rows:
            num = int(row["number"])
            row["square"] = number_to_square.get(num, "")
            if row["square"] != "":
                updated += 1
            writer.writerow(row)

    log(f"  Updated {updated}/{len(rows)} rows in master.csv")
    return updated


# ═══════════════════════════════════════════════════════════
#  STEP 7 — Verification
# ═══════════════════════════════════════════════════════════
def step7_verify():
    log("STEP 7 ▶ Verifying master.csv integrity")

    master_path = os.path.join(OUTPUT_FOLDER, MASTER_FILE)
    with open(master_path, "r") as f:
        rows = list(csv.DictReader(f))

    total      = len(rows)
    filled     = sum(1 for r in rows if r.get("square", "") != "")
    empty      = total - filled

    status = "✅ PASS" if empty == 0 else f"❌ FAIL ({empty} empty rows)"
    log(f"  Rows: {total} | Filled: {filled} | Empty: {empty} | {status}")

    return empty == 0


# ═══════════════════════════════════════════════════════════
#  MAIN PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════
def run_pipeline(verify: bool = True):
    start = time.time()
    log("=" * 55)
    log("  CSV FILE MANAGEMENT AGENT — PIPELINE START")
    log("=" * 55)

    try:
        x, sublists         = step1_generate_data();  result["steps_completed"] += 1
        step2_write_files(x, sublists);               result["steps_completed"] += 1
        step3_organize_folders();                     result["steps_completed"] += 1
        step4_cleanup();                              result["steps_completed"] += 1
        number_to_square    = step5_process_csvs();   result["steps_completed"] += 1
        updated             = step6_update_master(number_to_square)
        result["total_rows_updated"] = updated;       result["steps_completed"] += 1

        if verify:
            passed = step7_verify();                  result["steps_completed"] += 1
            result["status"] = "success" if passed else "partial"
        else:
            result["status"] = "success"

    except Exception as exc:
        result["status"] = "failed"
        result["errors"].append(str(exc))
        log(f"FATAL: {exc}", "ERROR")

    result["duration_seconds"] = round(time.time() - start, 2)

    # Save memory
    mem_path = "data/memories/last_run.json"
    os.makedirs(os.path.dirname(mem_path), exist_ok=True)
    with open(mem_path, "w") as f:
        json.dump(result, f, indent=2)

    log("=" * 55)
    log(f"  DONE — Status: {result['status'].upper()} | "
        f"{result['steps_completed']} steps | "
        f"{result['duration_seconds']}s")
    log("=" * 55)


# ─────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV File Management Agent Pipeline")
    parser.add_argument("--verify", action="store_true", help="Run verification step")
    parser.add_argument("--no-verify", dest="verify", action="store_false")
    parser.set_defaults(verify=True)
    args = parser.parse_args()
    run_pipeline(verify=args.verify)