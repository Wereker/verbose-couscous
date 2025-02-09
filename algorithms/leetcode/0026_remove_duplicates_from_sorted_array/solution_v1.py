from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        stack = []
        i = 0

        while i < len(nums):
            if nums[i] in stack:
                nums.pop(i)
            else:
                stack.append(nums[i])
                i += 1
                
        return i