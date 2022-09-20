class ListNode(object):
    """
    An implementation of basic node for a LinkedList
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def merge_two_lists(self, list1, list2):
        """
        The function merges two sorted LinkedLists into a new sorted
        LinkedList
        :type list1: Optional[ListNode] a first linked list
        :type list2: Optional[ListNode] a second linked list
        :rtype: Optional[ListNode]
        """
        new_head = cur_new = ListNode()

        while list1 and list2:
            if list1.val <= list2.val:
                cur_new.next = ListNode(val=list1.val)
                list1 = list1.next
            else:
                cur_new.next = ListNode(val=list2.val)
                list2 = list2.next
            cur_new = cur_new.next

        while list1 or list2:
            if list1:
                cur_new.next = ListNode(val=list1.val)
                list1 = list1.next
            if list2:
                cur_new.next = ListNode(val=list2.val)
                list2 = list2.next
            cur_new = cur_new.next

        return new_head.next
