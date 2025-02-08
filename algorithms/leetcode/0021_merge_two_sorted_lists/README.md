# 🟢 Merge Two Sorted Lists (LeetCode #21)

## 📌 Условия задачи

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.


**Example 1:**

**Input:** list1 = [1,2,4], list2 = [1,3,4]
**Output:** [1,1,2,3,4,4]

**Example 2:**

**Input:** list1 = [], list2 = []
**Output:** []

**Example 3:**

**Input:** list1 = [], list2 = [0]
**Output:** [0]
 

**Constraints:**

The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

## 🚀 Решение

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        mergeListHead = ListNode(-1)
        mergeList = mergeListHead

        while list1 != None and list2 != None:
            num1 = list1.val if list1 else 0
            num2 = list2.val if list2 else 0

            if num1 < num2:
                nextNode = ListNode(num1)
                list1 = list1.next if list1 else None

            else:
                nextNode = ListNode(num2)
                list2 = list2.next if list2 else None

            mergeList.next = nextNode
            mergeList = nextNode
        
        mergeList.next = list1 or list2

        return mergeListHead.next
```