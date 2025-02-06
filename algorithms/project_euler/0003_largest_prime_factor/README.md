# Largest Prime Factor (Problem #3)

## 📌 Условия задачи

The prime factors of `13195` are `5`, `7`, `13` and `29`.
What is the largest prime factor of the number `600851475143`?


## 🚀 Решение

```python
class Solution:
    def largest_prime_factor(self, number: int) -> int:
        n = 2
        sqrt_number = math.sqrt(number)
        while n < sqrt_number:
            if number % n == 0:
                number //= n
                sqrt_number = math.sqrt(number)
            else:
                n += 1

        return number
    

solution = Solution()
print(solution.largest_prime_factor(600851475143))
```