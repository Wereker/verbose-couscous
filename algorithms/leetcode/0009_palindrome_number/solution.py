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