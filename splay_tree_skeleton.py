class SplayTree:
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right'
        
        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
    
    def __init__(self):
        """Create an initially empty splay tree."""
        self._root = None
        self._size = 0
    
    def _set_parent(self, child, parent):
        """Helper to set parent-child relationship."""
        if child is not None:
            child._parent = parent
    
    def _rotate_right(self, node):
        """Rotate right around node."""
        left_child = node._left
        node._left = left_child._right
        self._set_parent(node._left, node)
        
        left_child._parent = node._parent
        if node._parent is None:
            self._root = left_child
        elif node == node._parent._left:
            node._parent._left = left_child
        else:
            node._parent._right = left_child
        
        left_child._right = node
        node._parent = left_child
        return left_child
    
    def _rotate_left(self, node):
        """Rotate left around node."""
        right_child = node._right
        node._right = right_child._left
        self._set_parent(node._right, node)
        
        right_child._parent = node._parent
        if node._parent is None:
            self._root = right_child
        elif node == node._parent._right:
            node._parent._right = right_child
        else:
            node._parent._left = right_child
        
        right_child._left = node
        node._parent = right_child
        return right_child
    
    def _splay(self, node):
        """Splay the given node to the root."""
        if node is None:
            return
        
        while node._parent is not None:
            parent = node._parent
            grandparent = parent._parent
            
            if grandparent is None:
                # Zig case: parent is root
                if node == parent._left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            elif ((node == parent._left) == (parent == grandparent._left)):
                # Zig-zig case: same direction
                if node == parent._left:
                    self._rotate_right(grandparent)
                    self._rotate_right(parent)
                else:
                    self._rotate_left(grandparent)
                    self._rotate_left(parent)
            else:
                # Zig-zag case: different directions
                if node == parent._left:
                    self._rotate_right(parent)
                    self._rotate_left(grandparent)
                else:
                    self._rotate_left(parent)
                    self._rotate_right(grandparent)
    
    def search(self, element):
        """Search for an element and splay it to root if found."""
        node = self._find_node(element)
        if node is not None:
            self._splay(node)
            return True
        return False
    
    def _find_node(self, element):
        """Find and return the node containing element."""
        current = self._root
        last_node = None
        
        while current is not None:
            last_node = current
            if element == current._element:
                return current
            elif element < current._element:
                current = current._left
            else:
                current = current._right
        
        # If element not found, splay the last accessed node
        if last_node is not None:
            self._splay(last_node)
        
        return None
    
    def insert(self, element):
        """Insert an element into the tree."""
        if self._root is None:
            self._root = self._Node(element)
            self._size = 1
            return
        
        # Find insertion point
        current = self._root
        parent = None
        
        while current is not None:
            parent = current
            if element == current._element:
                # Element already exists, just splay it
                self._splay(current)
                return
            elif element < current._element:
                current = current._left
            else:
                current = current._right
        
        # Create and insert new node
        new_node = self._Node(element, parent)
        if element < parent._element:
            parent._left = new_node
        else:
            parent._right = new_node
        
        self._size += 1
        self._splay(new_node)
    
    def delete(self, element):
        """Delete an element from the tree."""
        node = self._find_node(element)
        if node is None:
            return False
        
        # Splay the node to be deleted to the root
        self._splay(node)
        
        # Now delete the root
        left_subtree = self._root._left
        right_subtree = self._root._right
        
        if left_subtree is None:
            # No left subtree, right becomes new root
            self._root = right_subtree
            self._set_parent(self._root, None)
        elif right_subtree is None:
            # No right subtree, left becomes new root
            self._root = left_subtree
            self._set_parent(self._root, None)
        else:
            # Both subtrees exist
            # Find maximum in left subtree
            self._root = left_subtree
            left_subtree._parent = None
            
            # Find the rightmost node in left subtree
            max_node = left_subtree
            while max_node._right is not None:
                max_node = max_node._right
            
            # Splay the maximum node to root
            self._splay(max_node)
            
            # Attach right subtree
            self._root._right = right_subtree
            self._set_parent(right_subtree, self._root)
        
        self._size -= 1
        return True
    
    def find_min(self):
        """Find and return the minimum element."""
        if self._root is None:
            return None
        
        current = self._root
        while current._left is not None:
            current = current._left
        
        self._splay(current)
        return current._element
    
    def find_max(self):
        """Find and return the maximum element."""
        if self._root is None:
            return None
        
        current = self._root
        while current._right is not None:
            current = current._right
        
        self._splay(current)
        return current._element
    
    def size(self):
        """Return the number of elements in the tree."""
        return self._size
    
    def is_empty(self):
        """Check if the tree is empty."""
        return self._size == 0
    
    def height(self):
        """Return the height of the tree."""
        return self._height_helper(self._root)
    
    def _height_helper(self, node):
        """Recursive helper for height calculation."""
        if node is None:
            return -1
        return 1 + max(self._height_helper(node._left), 
                      self._height_helper(node._right))
    
    def inorder_traversal(self):
        """Return inorder traversal of the tree."""
        result = []
        self._inorder_helper(self._root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """Recursive helper for inorder traversal."""
        if node is not None:
            self._inorder_helper(node._left, result)
            result.append(node._element)
            self._inorder_helper(node._right, result)
    
    def preorder_traversal(self):
        """Return preorder traversal of the tree."""
        result = []
        self._preorder_helper(self._root, result)
        return result
    
    def _preorder_helper(self, node, result):
        """Recursive helper for preorder traversal."""
        if node is not None:
            result.append(node._element)
            self._preorder_helper(node._left, result)
            self._preorder_helper(node._right, result)
    
    def split(self, element):
        """Split the tree at element, returning two trees."""
        if self._root is None:
            return SplayTree(), SplayTree()
        
        # Find the element or closest node
        node = self._find_node(element)
        
        # Create two new trees
        left_tree = SplayTree()
        right_tree = SplayTree()
        
        if self._root._element <= element:
            # Root goes to left tree
            left_tree._root = self._root
            right_tree._root = self._root._right
            
            if left_tree._root is not None:
                left_tree._root._right = None
                left_tree._root._parent = None
            
            if right_tree._root is not None:
                right_tree._root._parent = None
        else:
            # Root goes to right tree
            right_tree._root = self._root
            left_tree._root = self._root._left
            
            if right_tree._root is not None:
                right_tree._root._left = None
                right_tree._root._parent = None
            
            if left_tree._root is not None:
                left_tree._root._parent = None
        
        # Update sizes
        left_tree._size = self._count_nodes(left_tree._root)
        right_tree._size = self._count_nodes(right_tree._root)
        
        # Clear original tree
        self._root = None
        self._size = 0
        
        return left_tree, right_tree
    
    def join(self, other_tree):
        """Join this tree with another tree."""
        if self._root is None:
            self._root = other_tree._root
            self._size = other_tree._size
            return
        
        if other_tree._root is None:
            return
        
        # Find maximum in current tree and splay it
        self.find_max()
        
        # Attach other tree as right subtree
        self._root._right = other_tree._root
        self._set_parent(other_tree._root, self._root)
        self._size += other_tree._size
        
        # Clear other tree
        other_tree._root = None
        other_tree._size = 0
    
    def _count_nodes(self, node):
        """Count nodes in subtree rooted at node."""
        if node is None:
            return 0
        return 1 + self._count_nodes(node._left) + self._count_nodes(node._right)
    
    def clear(self):
        """Clear the tree."""
        self._root = None
        self._size = 0
    
    def display(self):
        """Display the tree structure."""
        if self._root is None:
            print("Empty tree")
            return
        self._display_helper(self._root, 0)
    
    def _display_helper(self, node, depth):
        """Recursive helper for display."""
        if node is None:
            return
        
        # Display right subtree first (higher values)
        if node._right is not None:
            self._display_helper(node._right, depth + 1)
        
        # Display current node
        indent = "    " * depth
        label = "  <- root" if node == self._root else ""
        print(f"{indent}* {node._element}{label}")
        
        # Display left subtree
        if node._left is not None:
            self._display_helper(node._left, depth + 1)
    
    def __len__(self):
        return self._size
    
    def __contains__(self, element):
        return self.search(element)
    
    def __iter__(self):
        return iter(self.inorder_traversal())
    
    def __str__(self):
        if self.is_empty():
            return "Empty Splay Tree"
        return f"Splay Tree({self.inorder_traversal()})"


