class AVLTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_height' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._height = 0

        def left_height(self):
            return self._left._height if self._left != None else 0

        def right_height(self):
            return self._right._height if self._right != None else 0

        def set_height(self, new_height):
            self._height = new_height

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        return self._search_node(element) is not None

    def _search_node(self, element):
        current = self._root
        while current is not None:
            if element == current._element:
                return current
            elif element < current._element:
                current = current._left
            else:
                current = current._right
        return None

    def insert(self, element):
        if self._root is None:
            self._root = self._Node(element)
            self._size = 1
        else:
            self._root = self._insert_recursive(self._root, element, None)

    def _insert_recursive(self, node, element, parent):
        # Base case: create new node
        if node is None:
            new_node = self._Node(element, parent)
            self._size += 1
            return new_node
        
        # Duplicate elements not allowed
        if element == node._element:
            return node
        
        # Recursively insert
        if element < node._element:
            node._left = self._insert_recursive(node._left, element, node)
        else:
            node._right = self._insert_recursive(node._right, element, node)
        
        # Update height
        self._update_height(node)
        
        # Check balance and perform rotations if needed
        return self._rebalance(node)

    def delete(self, element):
        if self._root is None:
            return False
        
        self._root = self._delete_recursive(self._root, element)
        return True

    def _delete_recursive(self, node, element):
        if node is None:
            return None
        
        if element < node._element:
            node._left = self._delete_recursive(node._left, element)
        elif element > node._element:
            node._right = self._delete_recursive(node._right, element)
        else:
            # Node to be deleted found
            self._size -= 1
            
            # Case 1: Node with only right child or no child
            if node._left is None:
                if node._right:
                    node._right._parent = node._parent
                return node._right
            
            # Case 2: Node with only left child
            elif node._right is None:
                node._left._parent = node._parent
                return node._left
            
            # Case 3: Node with two children
            # Find inorder successor (smallest in right subtree)
            successor = self._find_min(node._right)
            
            # Replace node's element with successor's element
            node._element = successor._element
            
            # Delete the successor
            node._right = self._delete_recursive(node._right, successor._element)
        
        self._update_height(node)
        
        return self._rebalance(node)

    def _find_min(self, node):
        while node._left is not None:
            node = node._left
        return node

    def _update_height(self, node):
        if node is not None:
            node._height = 1 + max(node.left_height(), node.right_height())

    def _get_balance(self, node):
        if node is None:
            return 0
        return node.left_height() - node.right_height()

    def _rebalance(self, node):
        if node is None:
            return node
        
        balance = self._get_balance(node)
        
        # Left heavy
        if balance > 1:
            # Left-Right case
            if self._get_balance(node._left) < 0:
                node._left = self._rotate_left(node._left)
            # Left-Left case
            node = self._rotate_right(node)
        
        # Right heavy
        elif balance < -1:
            # Right-Left case
            if self._get_balance(node._right) > 0:
                node._right = self._rotate_right(node._right)
            # Right-Right case
            node = self._rotate_left(node)
        
        return node

    def _rotate_left(self, node):
        new_root = node._right
        node._right = new_root._left
        
        if new_root._left:
            new_root._left._parent = node
        
        new_root._left = node
        new_root._parent = node._parent
        node._parent = new_root
        
        self._update_height(node)
        self._update_height(new_root)
        
        return new_root

    def _rotate_right(self, node):
        new_root = node._left
        node._left = new_root._right
        
        if new_root._right:
            new_root._right._parent = node
        
        new_root._right = node
        new_root._parent = node._parent
        node._parent = new_root
        
        self._update_height(node)
        self._update_height(new_root)
        
        return new_root

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def height(self):
        return self._root._height if self._root else -1

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node._left, result)
            result.append(node._element)
            self._inorder_recursive(node._right, result)

    def display(self):
        self._display(self._root, 0)

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            self._display(node._right, depth+1)
        label = ''
        if node == self._root:
            label += '  <- root'
        print(f'{"    "*depth}* {node._element}({node._height}){label}')
        if node._left != None:
            self._display(node._left, depth+1)


