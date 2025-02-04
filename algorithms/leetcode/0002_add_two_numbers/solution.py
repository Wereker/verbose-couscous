from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummyHead = ListNode(0)
        answer = dummyHead
        carry = 0

        while l1 != None or l2 != None or carry != 0:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            digit = val1 + val2 + carry
            carry = digit // 10

            nextNode = ListNode(digit % 10)
            answer.next = nextNode
            answer = nextNode

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummyHead.next