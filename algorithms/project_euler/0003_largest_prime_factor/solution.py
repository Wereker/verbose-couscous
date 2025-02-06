import math


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

# 6857