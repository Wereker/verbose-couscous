class Solution:
    def addBinary(self, a: str, b: str) -> str:
        answer = ""
        i = -1
        carry = 0
        min_str = min(a, b, key=len)
        max_str = max(b, a, key=len)

        while i >= -len(max_str):
            if i >= -len(min_str):
                new_digit = int(max_str[i]) + int(min_str[i]) + carry
            else:
                new_digit = int(max_str[i]) + carry

            carry = new_digit // 2
            answer = str(new_digit % 2) + answer
            i -= 1
            

        if carry:
            return "1" + answer

        return answer