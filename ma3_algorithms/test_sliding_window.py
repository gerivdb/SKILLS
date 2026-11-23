"""Tests unitaires pour SlidingWindow (MA3, REF-182)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sliding_window import SlidingWindow


class TestSlidingWindowMaxSumSubarray:
    def test_standard(self):
        assert SlidingWindow.max_sum_subarray([1, 2, 3, 4, 5], 2) == 9

    def test_k_equals_length(self):
        assert SlidingWindow.max_sum_subarray([1, 2, 3], 3) == 6

    def test_k_invalid(self):
        assert SlidingWindow.max_sum_subarray([1, 2, 3], 5) is None
        assert SlidingWindow.max_sum_subarray([1, 2, 3], 0) is None

    def test_empty_list(self):
        assert SlidingWindow.max_sum_subarray([], 2) is None

    def test_negative_numbers(self):
        assert SlidingWindow.max_sum_subarray([-1, -2, -3, -4], 2) == -3


class TestSlidingWindowMinSubarrayLen:
    def test_standard(self):
        assert SlidingWindow.min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2

    def test_not_possible(self):
        assert SlidingWindow.min_subarray_len(100, [1, 2, 3]) == 0

    def test_exact_match(self):
        assert SlidingWindow.min_subarray_len(5, [5]) == 1

    def test_empty(self):
        assert SlidingWindow.min_subarray_len(5, []) == 0


class TestSlidingWindowLongestSubstringKDistinct:
    def test_standard(self):
        assert SlidingWindow.longest_substring_k_distinct("eceba", 2) == 3

    def test_k_zero(self):
        assert SlidingWindow.longest_substring_k_distinct("abc", 0) == 0

    def test_empty_string(self):
        assert SlidingWindow.longest_substring_k_distinct("", 2) == 0

    def test_k_larger_than_unique(self):
        assert SlidingWindow.longest_substring_k_distinct("abc", 5) == 3


class TestSlidingWindowDomDensity:
    def test_returns_chunks(self):
        result = SlidingWindow.dom_density("abcdefghij", 4, 3)
        assert len(result) > 0
        assert all(len(chunk) >= 3 for _, _, chunk in result)

    def test_empty_text(self):
        assert SlidingWindow.dom_density("", 4, 3) == []

    def test_min_chars_filter(self):
        result = SlidingWindow.dom_density("ab", 4, 5)
        assert result == []

