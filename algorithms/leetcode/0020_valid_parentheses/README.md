# 🟢 Valid Parentheses (LeetCode #20)

## 📌 Условия задачи

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.
 

**Example 1:**

**Input:** s = "()"

**Output:** true

**Example 2:**

**Input:** s = "()[]{}"

**Output:** true

**Example 3:**

**Input:** s = "(]"

**Output:** false

**Example 4:**

**Input:** s = "([])"

**Output:** true

 

Constraints:

- `1 <= s.length <= 104`
- `s` consists of parentheses only `'()[]{}'`.

## 🚀 Решение

```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        map_dtls = {')':'(',']':'[','}':'{'}
        for str_val in s:
            if stack and str_val in map_dtls and stack[-1] == map_dtls[str_val]:
                stack.pop()
            else:
                stack.append(str_val)
        print(stack)
        if not stack:
            return True
        else:
            return False
```