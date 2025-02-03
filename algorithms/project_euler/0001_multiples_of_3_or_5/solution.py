class Solution:
    def multiples_3_or_5(self, number: int):
        answer = 0
        for i in range(number):
            if i % 5 == 0 or i % 3 == 0:
                answer += i

        return answer

solution = Solution()
print(solution.multiples_3_or_5(1000))