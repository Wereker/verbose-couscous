> # 🟢 Longest Common Prefix (LeetCode #14)

## 📌 Условия задачи

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

 

**Example 1:**

> **Input:** strs = ["flower","flow","flight"]
> **Output:** "fl"
> 
**Example 2:**

> **Input:** strs = ["dog","racecar","car"]
> **Output:** ""
> **Explanation:** There is no common prefix among the input strings.
 
**Constraints:**

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters if it is non-empty.


## 🚀 Решение

```python
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
```