class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        letterCombinations = {
            "2" : "abc",
            "3" : "def",
            "4" : "ghi",
            "5" : "jkl",
            "6" : "mno",
            "7" : "pqrs",
            "8" : "tuv",
            "9" : "wxyz",
        }
        ans = []

        for i in digits:
            if not ans:
                ans = [a for a in letterCombinations[i]]
            else:
                ans = [a + b for a in ans for b in letterCombinations[i]]
        

        return ans