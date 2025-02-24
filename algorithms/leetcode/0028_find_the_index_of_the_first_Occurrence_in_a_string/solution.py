class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if len(needle) > len(haystack):
            return -1

        for i in range(len(haystack)):
            if haystack[i] == needle[0]:
                k = 0
                for j in range(len(needle)):
                    if i + j >= len(haystack):
                        break

                    if haystack[i + j] != needle[j]:
                        break
                    k += 1
                
                if k == len(needle):
                    return i
        return -1