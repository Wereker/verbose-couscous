# 🟢 Remove Duplicates from Sorted Array (LeetCode #26)

## 📌 Условия задачи

## 🚀 Решение

### ❌ Первая версия (75ms runtime)

```python
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
```

### ✅ Вторая версия (0ms runtime)

```python
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
```