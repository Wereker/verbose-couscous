class Solution:
    def climbStairs(self, n: int) -> int:
        lst = [1] * n
        
        if n == 1:
            return 1

        for i in range(n - 2):
            lst[i + 1] += lst[i] 
            lst[i + 2] += lst[i]

        return lst[n - 2] + 1