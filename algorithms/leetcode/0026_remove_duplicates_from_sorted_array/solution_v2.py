from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0
        count = 0

        while i < len(nums):
            if nums[i] != nums[count]:
                count += 1
                nums[count] = nums[i]
            i += 1

        return count + 1