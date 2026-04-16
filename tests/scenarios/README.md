# Test Scenarios — CSV File Management Agent

## Scenario 1: Happy Path (Full Pipeline)
**Description**: Run all 7 steps on clean state, verify 100 rows filled.
**Expected**: Status = SUCCESS, 100/100 rows updated, 7/7 steps complete.
**File**: `test_pipeline.py::TestFullPipeline::test_end_to_end`

---

## Scenario 2: Missing CSV File
**Description**: Manually delete `csv_5.csv` from all root copies before step 5.
**Expected**: Agent searches subfolders, finds file in a folder with circular overlap,
              processes it correctly. No row is left empty.

---

## Scenario 3: Re-run Idempotency
**Description**: Run the full pipeline twice without clearing Output/.
**Expected**: No crash. All files overwritten cleanly. master.csv still has 100 rows.

---

## Scenario 4: Empty Sublist Edge Case
**Description**: Change range to 1–5 with 10 sublists (more sublists than numbers).
**Expected**: Some sublists will be empty. Agent logs warning but does not crash.
              master.csv has 5 rows, all with squares.

---

## Scenario 5: Verification Failure Detection
**Description**: Manually corrupt master.csv (remove square values from 10 rows).
**Expected**: VerifierAgent detects 10 empty rows and reports FAIL.