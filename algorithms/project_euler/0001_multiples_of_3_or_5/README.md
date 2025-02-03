# Multiples of 3 or 5 (Problem #1)
## 📌 Условия задачи

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

## 🚀 Решение

```python
class Solution:
    def multiples_3_or_5(self, number: int):
        answer = 0
        for i in range(number):
            if i % 5 == 0 or i % 3 == 0:
                answer += i

        return answer
```