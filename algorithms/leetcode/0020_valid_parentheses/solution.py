class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        map_dtls = {')':'(',']':'[','}':'{'}
        for str_val in s:
            if stack and str_val in map_dtls and stack[-1] == map_dtls[str_val]:
                stack.pop()
            else:
                stack.append(str_val)
        print(stack)
        if not stack:
            return True
        else:
            return False