"""BinarySearch — Recherche binaire deterministe.

Utilise pour naviguer dans shard_graph.db (M3-Graph) et optimiser les
requetes FTS5, et tout probleme necessitant une recherche logarithmique
dans une sequence triee.
"""


class BinarySearch:
    """Recherche binaire (O(log n) temps, O(1) espace)."""

    @staticmethod
    def search(nums: list[int], target: int) -> int:
        """Retourne l index de target dans nums trie, ou -1 si absent."""
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    @staticmethod
    def lower_bound(nums: list[int], target: int) -> int:
        """Premier index i tel que nums[i] >= target, ou len(nums) si absent."""
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    @staticmethod
    def upper_bound(nums: list[int], target: int) -> int:
        """Premier index i tel que nums[i] > target, ou len(nums) si absent."""
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left

    @staticmethod
    def search_insert(nums: list[int], target: int) -> int:
        """Index où target devrait etre insere pour maintenir l ordre trie."""
        return BinarySearch.lower_bound(nums, target)

    @staticmethod
    def count_occurrences(nums: list[int], target: int) -> int:
        """Nombre d occurrences de target dans nums trie."""
        lo = BinarySearch.lower_bound(nums, target)
        if lo == len(nums) or nums[lo] != target:
            return 0
        hi = BinarySearch.upper_bound(nums, target)
        return hi - lo

    @staticmethod
    def fts5_rowid_lookup(rowids: list[int], target_rowid: int) -> int:
        """Recherche d un rowid FTS5 dans une liste triee d rowids.

        Retourne l index du rowid ou -1. Optimise les requetes FTS5
        en evitant un scan lineaire sur les rowids retournes.
        """
        return BinarySearch.search(rowids, target_rowid)

