"""TwoPointers — Algorithme a deux pointeurs deterministe.

Utilise pour la reconciliation d etats entre kilo.db et agent-manager.json,
et tout probleme nécessitant une traversale lineaire de deux sequences
triees ou un tableau avec contraintes de somme/cible.
"""


class TwoPointers:
    """Algorithme a deux pointeurs (O(n) temps, O(1) espace supplementaire)."""

    @staticmethod
    def find_pair_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
        """Retourne les indices (i, j) tels que nums[i] + nums[j] == target.

        nums doit etre trie par ordre croissant. Retourne None si aucune paire.
        """
        left = 0
        right = len(nums) - 1
        while left < right:
            current = nums[left] + nums[right]
            if current == target:
                return (left, right)
            if current < target:
                left += 1
            else:
                right -= 1
        return None

    @staticmethod
    def reconcile_states(left_keys: list[str], right_keys: list[str]) -> dict[str, list[str]]:
        """Reconciliation d etats entre deux listes de cles triees.

        Retourne un dict avec les cles communes, presentes seulement a gauche,
        et presentes seulement a droite.
        """
        i = j = 0
        common: list[str] = []
        left_only: list[str] = []
        right_only: list[str] = []
        while i < len(left_keys) and j < len(right_keys):
            if left_keys[i] == right_keys[j]:
                common.append(left_keys[i])
                i += 1
                j += 1
            elif left_keys[i] < right_keys[j]:
                left_only.append(left_keys[i])
                i += 1
            else:
                right_only.append(right_keys[j])
                j += 1
        while i < len(left_keys):
            left_only.append(left_keys[i])
            i += 1
        while j < len(right_keys):
            right_only.append(right_keys[j])
            j += 1
        return {
            "common": common,
            "left_only": left_only,
            "right_only": right_only,
        }

    @staticmethod
    def trap_rain_water(height: list[int]) -> int:
        """Volume d eau retenu apres la pluie (TwoPointers, O(n), O(1))."""
        if not height:
            return 0
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        total = 0
        while left < right:
            if height[left] < height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    total += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    total += right_max - height[right]
                right -= 1
        return total

