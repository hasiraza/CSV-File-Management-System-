# Agents: Worker Pool
# These agents each own a single stage of the pipeline

---

## DataGeneratorAgent
**Stage**: 1
**Input**: `NUM_RANGE_START`, `NUM_RANGE_END`, `NUM_SUBLISTS` from `.env`
**Output**: `list X`, `sublists[]` (in memory)

Responsibilities:
- Build `x = list(range(1, 101))`
- Chunk into 10 equal sublists of 10 elements each
- Validate chunk count matches `NUM_SUBLISTS`

---

## FolderOrganizerAgent
**Stage**: 3
**Input**: `folder_assignments[]`, `OUTPUT_FOLDER`
**Output**: 10 subfolders, each containing 3 copied CSV files

Responsibilities:
- Create `Output/folder_1` through `Output/folder_10`
- Assign files using circular combination:
  `combo = [files[i%n], files[(i+1)%n], files[(i+2)%n]]`
- Copy (not move) files from `Output/` into each subfolder
- Log each copy operation

---

## CleanupAgent
**Stage**: 4
**Input**: Root-level `csv_N.csv` paths
**Output**: Cleaned `Output/` directory (no loose CSV files)

Responsibilities:
- Confirm all files were copied successfully before deleting
- Delete `Output/csv_1.csv` through `Output/csv_10.csv`
- Log each deletion

---

## CSVProcessorAgent
**Stage**: 5
**Input**: Folder list, `find_file()` skill
**Output**: `number_to_square` dictionary populated

Responsibilities:
- Iterate `csv_1.csv` → `csv_10.csv` in order
- For each file, call `SearchSkill.find_file()` to locate it
- Read column `X`, compute `X²`, store in dict
- Handle `csv_11.csv` gracefully (expected missing — log, skip)

---

## UpdaterAgent
**Stage**: 6
**Input**: `master.csv` path, `number_to_square` dict
**Output**: Updated `master.csv` with all 100 squares filled

Responsibilities:
- Read all rows from `master.csv` into memory
- Match each `number` → look up square in dict
- Rewrite entire file with `DictWriter`
- Verify no row has an empty `square` after write

---

## VerifierAgent
**Stage**: 7
**Input**: `master.csv` path
**Output**: Verification report printed to console + saved to `data/memories/`

Responsibilities:
- Load `master.csv`
- Assert row count == 100
- Assert no empty `square` values
- Print pass/fail summary with counts