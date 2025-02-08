from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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