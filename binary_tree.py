class BinarySearchTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    def __init__(self):
        """Create an initially empty binary search tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        node = self._root
        while node is not None:
            if element == node._element:
                return node
            elif element < node._element:
                node = node._left
            else:
                node = node._right
        return None

    def contains(self, element):
        return self.search(element) is not None

    def insert(self, element):
        if self._root is None:
            self._root = self._Node(element)
            self._size = 1
            return

        node = self._root
        while True:
            if element < node._element:
                if node._left is None:
                    node._left = self._Node(element, parent=node)
                    self._size += 1
                    break
                node = node._left
            elif element > node._element:
                if node._right is None:
                    node._right = self._Node(element, parent=node)
                    self._size += 1
                    break
                node = node._right
            else:
                # Element already exists, don't insert duplicate
                break

    def delete(self, element):
        node = self.search(element)
        if node is None:
            return False

        # Case 1: Node has two children
        if node._left is not None and node._right is not None:
            successor = self._find_successor(node)
            node._element = successor._element
            node = successor

        # Case 2 & 3: Node has at most one child
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        
        if node._parent is None:
            self._root = child
        elif node == node._parent._left:
            node._parent._left = child
        else:
            node._parent._right = child

        self._size -= 1
        return True

    def _find_successor(self, current_node):
        return self._go_left(current_node._right)

    def _find_predecessor(self, current_node):
        return self._go_right(current_node._left)

    def _go_left(self, node):
        while node._left is not None:
            node = node._left
        return node

    def _go_right(self, node):
        while node._right is not None:
            node = node._right
        return node

    def find_min(self):
        if self._root is None:
            return None
        return self._go_left(self._root)._element

    def find_max(self):
        if self._root is None:
            return None
        return self._go_right(self._root)._element

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def height(self):
        return self._height_recursive(self._root)

    def _height_recursive(self, node):
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node._left), 
                      self._height_recursive(node._right))

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node._left, result)
            result.append(node._element)
            self._inorder_recursive(node._right, result)

    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self._root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node is not None:
            result.append(node._element)
            self._preorder_recursive(node._left, result)
            self._preorder_recursive(node._right, result)

    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self._root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node is not None:
            self._postorder_recursive(node._left, result)
            self._postorder_recursive(node._right, result)
            result.append(node._element)

    def level_order_traversal(self):
        """breadth-first."""
        if self._root is None:
            return []
        
        result = []
        queue = [self._root]
        
        while queue:
            node = queue.pop(0)
            result.append(node._element)
            
            if node._left:
                queue.append(node._left)
            if node._right:
                queue.append(node._right)
        
        return result

    def range_query(self, min_val, max_val):
        """Return all elements in the BST within the range [min_val, max_val]."""
        result = []
        self._range_query_recursive(self._root, min_val, max_val, result)
        return result

    def _range_query_recursive(self, node, min_val, max_val, result):
        if node is None:
            return
        
        # If current node is greater than min_val, explore left subtree
        if node._element > min_val:
            self._range_query_recursive(node._left, min_val, max_val, result)
        
        # If current node is within range, add it
        if min_val <= node._element <= max_val:
            result.append(node._element)
        
        # If current node is less than max_val, explore right subtree
        if node._element < max_val:
            self._range_query_recursive(node._right, min_val, max_val, result)

    def validate_bst(self):
        return self._validate_bst_recursive(self._root, float('-inf'), float('inf'))

    def _validate_bst_recursive(self, node, min_val, max_val):
        if node is None:
            return True
        
        if node._element <= min_val or node._element >= max_val:
            return False
        
        return (self._validate_bst_recursive(node._left, min_val, node._element) and
                self._validate_bst_recursive(node._right, node._element, max_val))

    def clear(self):
        self._root = None
        self._size = 0

    def to_list(self):
        return self.inorder_traversal()

    def display(self):
        if self._root is None:
            print("Empty tree")
            return
        self._display(self._root, 0)

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            self._display(node._right, depth+1)
        label = ''
        if node == self._root:
            label += '  <- root'
        print(f'{"    "*depth}* {node._element}{label}')
        if node._left != None:
            self._display(node._left, depth+1)

    def __len__(self):
        return self._size

    def __contains__(self, element):
        return self.contains(element)

    def __iter__(self):
        return iter(self.inorder_traversal())

    def __str__(self):
        if self.is_empty():
            return "Empty BST"
        return f"BST({self.inorder_traversal()})"

    def __repr__(self):
        return f"BinarySearchTree(size={self._size}, elements={self.inorder_traversal()})"

