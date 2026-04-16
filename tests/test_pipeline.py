"""
tests/test_pipeline.py
──────────────────────
End-to-end and unit tests for the CSV File Management Agent.
Run: python tests/test_pipeline.py
"""

import os
import csv
import sys
import shutil
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pipeline import (
    step1_generate_data,
    step2_write_files,
    step3_organize_folders,
    step4_cleanup,
    step5_process_csvs,
    step6_update_master,
    step7_verify,
    find_file,
    OUTPUT_FOLDER,
    MASTER_FILE,
)

TEST_OUTPUT = "test_output_temp"


class TestDataGeneration(unittest.TestCase):
    def test_list_length(self):
        x, sublists = step1_generate_data()
        self.assertEqual(len(x), 100)

    def test_sublist_count(self):
        _, sublists = step1_generate_data()
        self.assertEqual(len(sublists), 10)

    def test_sublist_coverage(self):
        x, sublists = step1_generate_data()
        all_vals = [v for s in sublists for v in s]
        self.assertEqual(sorted(all_vals), x)


class TestFileCreation(unittest.TestCase):
    def setUp(self):
        global OUTPUT_FOLDER
        import pipeline
        self._orig = pipeline.OUTPUT_FOLDER
        pipeline.OUTPUT_FOLDER = TEST_OUTPUT

    def tearDown(self):
        import pipeline
        pipeline.OUTPUT_FOLDER = self._orig
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_master_csv_exists(self):
        import pipeline
        x, sublists = step1_generate_data()
        step2_write_files(x, sublists)
        self.assertTrue(os.path.exists(os.path.join(TEST_OUTPUT, MASTER_FILE)))

    def test_sublist_csvs_created(self):
        import pipeline
        x, sublists = step1_generate_data()
        step2_write_files(x, sublists)
        for i in range(1, 11):
            self.assertTrue(
                os.path.exists(os.path.join(TEST_OUTPUT, f"csv_{i}.csv")),
                f"csv_{i}.csv should exist"
            )


class TestSearchSkill(unittest.TestCase):
    def setUp(self):
        os.makedirs(os.path.join(TEST_OUTPUT, "folderA"), exist_ok=True)
        with open(os.path.join(TEST_OUTPUT, "folderA", "target.csv"), "w") as f:
            f.write("X\n1\n2\n")

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_find_existing_file(self):
        result = find_file("target.csv", ["folderA"], TEST_OUTPUT)
        self.assertIsNotNone(result)

    def test_find_missing_file_returns_none(self):
        result = find_file("ghost.csv", ["folderA"], TEST_OUTPUT)
        self.assertIsNone(result)


class TestFullPipeline(unittest.TestCase):
    """Scenario: Full run should produce a master.csv with 100 filled rows."""

    def setUp(self):
        import pipeline
        self._orig = pipeline.OUTPUT_FOLDER
        pipeline.OUTPUT_FOLDER = TEST_OUTPUT

    def tearDown(self):
        import pipeline
        pipeline.OUTPUT_FOLDER = self._orig
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_end_to_end(self):
        import pipeline
        x, sublists = step1_generate_data()
        step2_write_files(x, sublists)
        step3_organize_folders()
        step4_cleanup()
        number_to_square = step5_process_csvs()
        updated = step6_update_master(number_to_square)
        passed = step7_verify()

        self.assertEqual(updated, 100)
        self.assertTrue(passed)


if __name__ == "__main__":
    unittest.main(verbosity=2)