# 🟢 Sqrt(x) (LeetCode #69)

## 📌 Условия задачи

Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest *integer*. The returned integer should be **non-negative** as well.

You **must not use** any built-in exponent function or operator.

For example, do not use `pow(x, 0.5)` in c++ or `x ** 0.5` in python.
 

**Example 1:**

> **Input:** x = 4
> **Output:** 2
> **Explanation:** The square root of 4 is 2, so we return 2.

**Example 2:**

> **Input:** x = 8
> **Output:** 2
> **Explanation:** The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.
 

**Constraints:**

- `0 <= x <= 231 - 1`

## 🚀 Решение

### ❌ Первая версия (Brute Force, O(n²))

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        for i in range(x + 1):
            if i * i > x:
                return i - 1
            elif i * i == x:
                return i
```

### ✅ Оптимизированная версия (Binary Search, O(log(n)))

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        ans = 0

        while l <= r:
            mid = l + (r - l) // 2

            if mid * mid < x:
                l = mid + 1
                ans = mid
            elif mid * mid > x:
                r = mid - 1
            else:
                return mid

        return ans
```