# CSV File Management Agent — Documentation

## Overview
This agent automates a structured CSV file management pipeline originally
designed as a university assignment (Muhammad Haseeb, F2024332157).

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE FLOW                               │
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐  │
│  │  STEP 1      │────▶│  STEP 2      │────▶│  STEP 3        │  │
│  │  Generate    │     │  Write Files │     │  Organize      │  │
│  │  Data (1–100)│     │  master.csv  │     │  Into Folders  │  │
│  │  + sublists  │     │  csv_N.csv   │     │  (circular)    │  │
│  └──────────────┘     └──────────────┘     └───────┬────────┘  │
│                                                    │            │
│  ┌──────────────┐     ┌──────────────┐     ┌──────▼────────┐  │
│  │  STEP 7      │◀────│  STEP 6      │◀────│  STEP 4       │  │
│  │  Verify      │     │  Update      │     │  Cleanup Root │  │
│  │  master.csv  │     │  master.csv  │     │  CSV Files    │  │
│  │  (100 rows)  │     │  (squares)   │     │               │  │
│  └──────────────┘     └──────┬───────┘     └───────────────┘  │
│                              │                                  │
│                       ┌──────▼───────┐                         │
│                       │  STEP 5      │                         │
│                       │  Read CSVs   │                         │
│                       │  Compute X²  │                         │
│                       │  (search if  │                         │
│                       │   missing)   │                         │
│                       └──────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### Circular File Assignment
Each folder gets 3 files using modular arithmetic:
```
folder_1 → [csv_1, csv_2, csv_3]
folder_2 → [csv_2, csv_3, csv_4]
...
folder_10 → [csv_10, csv_1, csv_2]
```
This ensures every file appears in multiple folders — enabling recovery
if a file is missing from its primary location.

### Fault-Tolerant File Search
Before failing on a missing CSV, the agent searches all subfolders.
This is why the circular assignment above is essential — it creates
natural redundancy.

### Idempotent Writes
All folder and file creation operations use `exist_ok=True` or
existence checks so the pipeline can be safely re-run.

## Running the Pipeline

```bash
# Full run with verification
python src/pipeline.py --verify

# Full run, skip verification
python src/pipeline.py --no-verify

# Run tests
python tests/test_pipeline.py
```

## Output Structure After Run
```
Output/
├── master.csv          ← 100 rows: number + square
├── folder_1/
│   ├── csv_1.csv
│   ├── csv_2.csv
│   └── csv_3.csv
├── folder_2/
│   ├── csv_2.csv
│   ├── csv_3.csv
│   └── csv_4.csv
└── ...
```