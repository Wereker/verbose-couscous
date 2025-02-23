class Solution:
    def intToRoman(self, num: int) -> str:
        intToRoman = {
            1 : "I",
            5 : "V",
            10 : "X",
            50 : "L",
            100 : "C",
            500 : "D",
            1000 : "M",
        }

        i = 0
        ans = ""
        while num > 0:
            digit = num % 10
            
            if digit % 5 == 4:
                ans = intToRoman[10 ** i] + intToRoman[(digit + 1) * 10 ** i] + ans
            else:
                if digit < 5:
                    ans = intToRoman[10 ** i] * digit + ans
                else:
                    ans = intToRoman[5 * 10 ** i] + intToRoman[10 ** i] * (digit % 5) + ans
            i += 1
            num //= 10
        
        return ans