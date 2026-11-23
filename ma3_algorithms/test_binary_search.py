"""Tests unitaires pour BinarySearch (MA3, REF-182)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from binary_search import BinarySearch


class TestBinarySearchSearch:
    def test_found(self):
        assert BinarySearch.search([1, 2, 3, 4, 5, 6, 7], 4) == 3

    def test_not_found(self):
        assert BinarySearch.search([1, 2, 3, 4, 5, 6, 7], 9) == -1

    def test_empty_list(self):
        assert BinarySearch.search([], 1) == -1

    def test_single_element_found(self):
        assert BinarySearch.search([42], 42) == 0

    def test_single_element_not_found(self):
        assert BinarySearch.search([42], 7) == -1

    def test_first_element(self):
        assert BinarySearch.search([1, 2, 3], 1) == 0

    def test_last_element(self):
        assert BinarySearch.search([1, 2, 3], 3) == 2


class TestBinarySearchLowerUpperBound:
    def test_lower_bound_exact(self):
        assert BinarySearch.lower_bound([1, 3, 5, 7], 5) == 2

    def test_lower_bound_insert(self):
        assert BinarySearch.lower_bound([1, 3, 5, 7], 4) == 2

    def test_lower_bound_empty(self):
        assert BinarySearch.lower_bound([], 1) == 0

    def test_upper_bound_exact(self):
        assert BinarySearch.upper_bound([1, 3, 5, 7], 5) == 3

    def test_upper_bound_insert(self):
        assert BinarySearch.upper_bound([1, 3, 5, 7], 4) == 2


class TestBinarySearchSearchInsert:
    def test_insert_middle(self):
        assert BinarySearch.search_insert([1, 3, 5, 7], 4) == 2

    def test_insert_beginning(self):
        assert BinarySearch.search_insert([1, 3, 5, 7], 0) == 0

    def test_insert_end(self):
        assert BinarySearch.search_insert([1, 3, 5, 7], 9) == 4


class TestBinarySearchCountOccurrences:
    def test_multiple_occurrences(self):
        assert BinarySearch.count_occurrences([1, 2, 2, 2, 3], 2) == 3

    def test_single_occurrence(self):
        assert BinarySearch.count_occurrences([1, 2, 3], 2) == 1

    def test_no_occurrence(self):
        assert BinarySearch.count_occurrences([1, 3, 5], 2) == 0

    def test_empty(self):
        assert BinarySearch.count_occurrences([], 1) == 0


class TestBinarySearchFts5RowidLookup:
    def test_found_rowid(self):
        assert BinarySearch.fts5_rowid_lookup([10, 20, 30, 40, 50], 30) == 2

    def test_not_found_rowid(self):
        assert BinarySearch.fts5_rowid_lookup([10, 20, 30, 40, 50], 25) == -1

    def test_empty_rowids(self):
        assert BinarySearch.fts5_rowid_lookup([], 1) == -1

