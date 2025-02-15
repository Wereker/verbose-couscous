# 🟢 Palindrome Number (LeetCode #9)

## 📌 Условия задачи

Given an integer `x`, return true if `x` is a palindrome, and `false` otherwise.

 
**Example 1:**

> **Input:** x = 121
> **Output:** true
> **Explanation:** 121 reads as 121 from left to right and from right to left.

**Example 2:**

> **Input:** x = -121
> **Output:** false
> **Explanation:** From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

**Example 3:**

> **Input:** x = 10
> **Output:** false
> **Explanation:** Reads 01 from right to left. Therefore it is not a palindrome.
 

**Constraints:**

- `-231 <= x <= 231 - 1`
 

**Follow up:** Could you solve it without converting the integer to a string?

## 🚀 Решение

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        
        if x < 0:
            return False
        
        num = x
        reverse_num = 0

        while x > 0:
            reverse_num = reverse_num * 10 + x % 10
            x //= 10

        return num == reverse_num
```