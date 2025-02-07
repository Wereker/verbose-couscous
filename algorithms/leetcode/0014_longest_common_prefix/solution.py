from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        first_str = min(strs, key=len)
        i = 0
        prefix = ""

        while i < len(first_str):
            if any([first_str[i] not in string[i] for string in strs]):
                return prefix

            prefix += first_str[i]
            i += 1
            
        return prefix