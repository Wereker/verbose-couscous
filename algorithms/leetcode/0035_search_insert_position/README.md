# 🟢 Search Insert Position (LeetCode #35)

## 📌 Условия задачи

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with `O(log n)` runtime complexity.

 

**Example 1:**

**Input:** nums = [1,3,5,6], target = 5
**Output:** 2

**Example 2:**

**Input:** nums = [1,3,5,6], target = 2
**Output**: 1

**Example 3:**

**Input:** nums = [1,3,5,6], target = 7
**Output:** 4
 

**Constraints:**

- `1 <= nums.length <= 104`
- `-104 <= nums[i] <= 104`
- `nums` contains distinct values sorted in ascending order.
- `-104 <= target <= 104`

## 🚀 Решение

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        i = 0
        j = len(nums) - 1

        while i <= j:
            k = (i + j) // 2

            if nums[k] == target:
                return k

            if nums[k] > target:
                j = k - 1
            else:
                i = k + 1

        return i
```