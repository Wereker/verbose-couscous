# 🟡 Longest Substring Without Repeating Characters (LeetCode #3)

## 📌 Условия задачи

Given a string s, find the length of the longest substring without repeating characters.

 

**Example 1:**

**Input:** s = "abcabcbb"
**Output:** 3
**Explanation**: The answer is "abc", with the length of 3.
**Example 2:**

**Input:** s = "bbbbb"
**Output:** 1
**Explanation:** The answer is "b", with the length of 1.
**Example 3:**

**Input:** s = "pwwkew"
**Output:** 3
**Explanation:** The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
 

Constraints:

- `0 <= s.length <= 5 * 104`
- `s` consists of English letters, digits, symbols and spaces.


## 🚀 Решение

### ❌ Первая версия

```python
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
```

### ✅ Оптимизированная версия

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        n = len(s)
        answer = 0
        left = 0
        right = 0

        while left < n and right < n:
            if s[right] not in seen:
                seen.add(s[right])
                right += 1

                answer = max(answer, right - left)
            else:
                seen.remove(s[left])
                left += 1

        return answer
```