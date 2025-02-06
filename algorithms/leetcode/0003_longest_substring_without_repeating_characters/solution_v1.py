class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        count = 0
        answer = 0

        for i in range(1, len(s)):
            if s[i] not in s[i-count:i]:
                count += 1
            else:
                answer = max(count, answer)
                count = 0
        
        return answer