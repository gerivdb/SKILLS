"""SlidingWindow — Algorithme a fenetre glissante deterministe.

Utilise pour les algorithmes de densite DOM (remplacement du DENSITY_JS bugge
sur Shadow DOM Gemini) et tout probleme nécessitant une traversale avec
contrainte de taille de fenetre fixe ou variable.
"""


class SlidingWindow:
    """Algorithme a fenetre glissante (O(n) temps, O(k) espace)."""

    @staticmethod
    def max_sum_subarray(nums: list[int], k: int) -> int | None:
        """Somme maximale d un sous-tableau contigu de taille k."""
        if not nums or k <= 0 or k > len(nums):
            return None
        window_sum = sum(nums[:k])
        max_sum = window_sum
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            if window_sum > max_sum:
                max_sum = window_sum
        return max_sum

    @staticmethod
    def min_subarray_len(target: int, nums: list[int]) -> int:
        """Longueur minimale d un sous-tableau dont la somme >= target.

        Retourne 0 si aucun sous-tableau ne satisfait.
        """
        left = 0
        current_sum = 0
        min_len = float("inf")
        for right in range(len(nums)):
            current_sum += nums[right]
            while current_sum >= target:
                window_len = right - left + 1
                if window_len < min_len:
                    min_len = window_len
                current_sum -= nums[left]
                left += 1
        return 0 if min_len == float("inf") else min_len

    @staticmethod
    def longest_substring_k_distinct(s: str, k: int) -> int:
        """Longueur de la plus longue sous-chaine avec au plus k caracteres distincts."""
        if k == 0 or not s:
            return 0
        char_count: dict[str, int] = {}
        left = 0
        max_len = 0
        for right in range(len(s)):
            char_count[s[right]] = char_count.get(s[right], 0) + 1
            while len(char_count) > k:
                char_count[s[left]] -= 1
                if char_count[s[left]] == 0:
                    del char_count[s[left]]
                left += 1
            window_len = right - left + 1
            if window_len > max_len:
                max_len = window_len
        return max_len

    @staticmethod
    def dom_density(text: str, window_size: int, min_chars: int) -> list[tuple[int, int, str]]:
        """Densite DOM par fenetre glissante sur un texte extrait.

        Retourne une liste de (start, end, substring) pour chaque fenetre
        dont le nombre de caracteres >= min_chars. Conçu pour remplacer
        DENSITY_JS qui retourne 0 char sur le Shadow DOM de Gemini.
        """
        results: list[tuple[int, int, str]] = []
        if not text or window_size <= 0:
            return results
        n = len(text)
        for start in range(0, n, max(1, window_size // 2)):
            end = min(start + window_size, n)
            chunk = text[start:end]
            if len(chunk) >= min_chars:
                results.append((start, end, chunk))
            if end >= n:
                break
        return results

