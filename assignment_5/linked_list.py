class Node:
    """
    A base item of LinkedList, has value and a link to next item stored
    in attributes
    """
    def __init__(self, value, next_=None):
        """
        constructor with built-in data validation through property
        :param value: value of Node
        :param next_: next node
        """
        self.value = value
        self.next = next_

    def __iter__(self):
        """
        allows iteration through Nodes
        :return: node data
        """
        current_node = self
        while current_node is not None:
            if isinstance(current_node._value, int):
                yield current_node._value
            else:
                sublist = iter(current_node._value)
                for item in sublist:
                    yield item
            current_node = current_node._next

    def flatten(self):
        """
        method flattens the nested linked list
        :return:
        """
        current = self
        while current:
            if isinstance(current._value, Node):
                temp = current._value
                current.value = temp._value
                next_node = temp._next
                while temp._next:
                    temp = temp._next
                temp.next = current._next
                current.next = next_node if next_node else current._next
            if not isinstance(current._value, Node):
                current = current._next

    @property
    def value(self):
        """
        getter method for _value attribute
        :return: _value attribute value
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        setter method for _value attribute with data validation
        :param new_value: new value for attribute
        :return: None
        """
        assert isinstance(new_value, (int, Node)), 'Node values must be ' \
                                                   'integer or a Node ' \
                                                   'instance '
        self._value = new_value

    @property
    def next(self):
        """
        getter method for next attribute of Node
        :return: _next attribute value
        """
        return self._next

    @next.setter
    def next(self, new_next):
        """
        setter method for _value attribute with data validation
        :param new_next:
        :return:
        """
        assert isinstance(new_next, Node) \
               or new_next is None, 'next item must be a Node instance ' \
                                    'or None'
        self._next = new_next


if __name__ == "__main__":
    # 1 -> None - just one no
    r1 = Node(1)
    assert [1] == list(r1)

    # 7 -> 2 -> 9 -> None
    r2 = Node(7, Node(2, Node(9)))
    assert [7, 2, 9] == list(r2)

    # 3 -> (19 -> 25 -> None ) -> 12 -> None
    r3 = Node(3, Node(Node(19, Node(25)), Node(12)))
    print(list(r3))
    assert [3, 19, 25, 12] == list(r3)

    r3.flatten()
    assert [3, 19, 25, 12] == list(r3)

    r3_node = r3
    while r3_node is not None:
        assert not isinstance(r3.value, Node)
        r3_node = r3_node.next

