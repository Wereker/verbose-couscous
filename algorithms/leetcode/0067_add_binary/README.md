# 🟢 Add Binary (LeetCode #67)

## 📌 Условия задачи

Given two binary strings `a` and `b`, return their *sum as a binary string*.


**Example 1:**

> **Input:** a = "11", b = "1"
> **Output:** "100"

**Example 2:**

> **Input:** a = "1010", b = "1011"
> **Output:** "10101"
 

**Constraints:**

- `1 <= a.length, b.length <= 104`
- `a` and `b` consist only of `'0'` or `'1'` characters.
- Each string does not contain leading zeros except for the zero itself.

## 🚀 Решение

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        answer = ""
        i = -1
        carry = 0
        min_str = min(a, b, key=len)
        max_str = max(b, a, key=len)

        while i >= -len(max_str):
            if i >= -len(min_str):
                new_digit = int(max_str[i]) + int(min_str[i]) + carry
            else:
                new_digit = int(max_str[i]) + carry

            carry = new_digit // 2
            answer = str(new_digit % 2) + answer
            i -= 1
            

        if carry:
            return "1" + answer

        return answer
```