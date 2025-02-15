class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        ans = 0
        k = 0

        for char in s:
            k += 1
            if char != " ":
                ans = k
            else:
                k = 0

        return ans