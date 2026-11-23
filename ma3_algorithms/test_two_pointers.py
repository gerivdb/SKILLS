"""Tests unitaires pour TwoPointers (MA3, REF-182)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from two_pointers import TwoPointers


class TestTwoPointersFindPairSorted:
    def test_found_pair(self):
        assert TwoPointers.find_pair_sorted([1, 2, 3, 4, 6], 6) == (1, 3)

    def test_not_found(self):
        assert TwoPointers.find_pair_sorted([1, 2, 3, 4, 6], 20) is None

    def test_single_element(self):
        assert TwoPointers.find_pair_sorted([5], 10) is None

    def test_empty_list(self):
        assert TwoPointers.find_pair_sorted([], 5) is None

    def test_negative_numbers(self):
        nums = [-3, -1, 0, 2, 4, 7]
        result = TwoPointers.find_pair_sorted(nums, 1)
        assert result is not None
        i, j = result
        assert nums[i] + nums[j] == 1


class TestTwoPointersReconcileStates:
    def test_identical_lists(self):
        result = TwoPointers.reconcile_states(["a", "b", "c"], ["a", "b", "c"])
        assert result == {"common": ["a", "b", "c"], "left_only": [], "right_only": []}

    def test_disjoint_lists(self):
        result = TwoPointers.reconcile_states(["a", "b"], ["c", "d"])
        assert result == {"common": [], "left_only": ["a", "b"], "right_only": ["c", "d"]}

    def test_partial_overlap(self):
        result = TwoPointers.reconcile_states(["a", "b", "d"], ["b", "c", "d", "e"])
        assert result == {
            "common": ["b", "d"],
            "left_only": ["a"],
            "right_only": ["c", "e"],
        }

    def test_empty_left(self):
        result = TwoPointers.reconcile_states([], ["a", "b"])
        assert result == {"common": [], "left_only": [], "right_only": ["a", "b"]}

    def test_empty_right(self):
        result = TwoPointers.reconcile_states(["a", "b"], [])
        assert result == {"common": [], "left_only": ["a", "b"], "right_only": []}


class TestTwoPointersTrapRainWater:
    def test_standard_case(self):
        assert TwoPointers.trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    def test_empty(self):
        assert TwoPointers.trap_rain_water([]) == 0

    def test_no_trap(self):
        assert TwoPointers.trap_rain_water([1, 2, 3, 4]) == 0

    def test_single_barrier(self):
        assert TwoPointers.trap_rain_water([4, 2, 0, 3, 2, 5]) == 9

