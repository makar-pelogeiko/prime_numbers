class DLinkedList:
    def __init__(self, def_value='B'):
        self.default_val = def_value
        self.curr = Node(val=self.default_val)

    @property
    def data(self):
        return self.curr.value

    @data.setter
    def data(self, val):
        self.curr.value = val

    def get_to_left_end(self):
        while not(self.curr.left is None):
            self.curr = self.curr.left

    def get_to_right_end(self):
        while not(self.curr.right is None):
            self.curr = self.curr.right

    def left_step(self):
        if self.curr.left is None:
            left = Node(val=self.default_val)
            left.right = self.curr
            self.curr.left = left

        self.curr = self.curr.left

    def right_step(self):
        if self.curr.right is None:
            right = Node(val=self.default_val)
            right.left = self.curr
            self.curr.right = right

        self.curr = self.curr.right

    def __str__(self):
        temp = self.curr
        while not (temp.left is None):
            temp = temp.left

        str_res = '['
        while not(temp is None):
            str_res += f"'{temp.value}'"
            temp = temp.right
            if not(temp is None):
                str_res += ', '

        str_res += ']'
        return str_res


class Node:
    def __init__(self, val=None):
        self.value = val
        self.left = None
        self.right = None
