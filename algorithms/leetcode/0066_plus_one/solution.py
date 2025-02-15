from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        digits[-1] += 1

        i = -1
        l = len(digits)
        carry = 0
        while i >= -l:
            new_digits = digits[i] + carry
            carry = new_digits // 10
            digits[i] = new_digits % 10
            i -= 1
        
        if carry:
            return [1] + digits
        
        return digits