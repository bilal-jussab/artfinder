# Tech Test for Artfinder
# Author: Bilal Jussab
# Date: 25 - 04 - 2024

import os
import unittest
import tempfile
import shutil
from unittest.mock import patch
from simplesearch import read_files, build_index, search

class TestTextSearch(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_files = [
            ("file1.txt", "merc audi bmw"),
            ("file2.txt", "merc audi"),
            ("file3.txt", "audi bmw"),
            ("file4.txt", "merc"),
        ]
        for filename, content in self.test_files:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write(content)

    def tearDown(self):
        # Remove the temporary directory and files
        shutil.rmtree(self.test_dir)

    def test_read_files(self):
        files = read_files(self.test_dir)
        self.assertEqual(len(files), len(self.test_files))
        for filename, content in self.test_files:
            self.assertIn((filename, content), files)

    def test_search_no_match(self):
        # Search for a word that doesn't exist in the files
        search_word = "volvo"
        files = read_files(self.test_dir)
        index = build_index(files)
        results = search(index, search_word)
        self.assertEqual(len(results), 0)

    def test_search(self):
        files = read_files(self.test_dir)
        index = build_index(files)
        results = search(index, "merc")
        self.assertEqual(len(results), 3)
        # Asserting filenames are in the results
        self.assertIn("file1.txt", [filename for filename, score in results])
        self.assertIn("file2.txt", [filename for filename, score in results])
        self.assertIn("file4.txt", [filename for filename, score in results])

if __name__ == "__main__":
    unittest.main()
