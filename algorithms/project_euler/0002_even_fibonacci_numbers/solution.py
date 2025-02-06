class Solution:
    def __init__(self):
        self.hashMap = {0: 1, 1: 1}

    def fib(self, number: int):
        if number not in self.hashMap:
            self.hashMap[number] = self.hashMap[number - 1] + self.hashMap[number - 2]
        return self.hashMap[number]
    
    def even_fibonacci_numbers(self):
        n = 1
        ans = 0
        while True:
            temp = self.fib(n)

            if temp % 2 == 0:
                ans += temp

            if temp > 4 * 10**6:
                return ans

            n += 1

solution = Solution()
print(solution.even_fibonacci_numbers())

# 4613732