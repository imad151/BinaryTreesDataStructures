class TwoFourTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_parent', '_keys', '_children'  # streamline memory usage
        
        def __init__(self, parent=None, keys=None, children=None):
            self._parent = parent
            self._keys = keys if keys is not None else []
            self._children = children if children is not None else []
        
        def is_leaf(self):
            """Check if this node is a leaf."""
            return len(self._children) == 0
        
        def is_full(self):
            """Check if this node has the maximum number of keys (3)."""
            return len(self._keys) == 3
        
        def find_child_index(self, key):
            """Find the index of the child where key should be inserted."""
            for i, k in enumerate(self._keys):
                if key < k:
                    return i
            return len(self._keys)
    
    def __init__(self):
        """Create an initially empty 2-4 tree."""
        self._root = None
        self._size = 0
    
    def search(self, element):
        """Search for an element in the tree. Returns True if found, False otherwise."""
        if self._root is None:
            return False
        return self._search_helper(self._root, element)
    
    def _search_helper(self, node, element):
        """Recursive helper for search."""
        # Check if element is in current node's keys
        if element in node._keys:
            return True
        
        # If leaf node and element not found, return False
        if node.is_leaf():
            return False
        
        # Find appropriate child to search
        child_index = node.find_child_index(element)
        if child_index < len(node._children):
            return self._search_helper(node._children[child_index], element)
        
        return False
    
    def insert(self, element):
        """Insert an element into the tree."""
        # If tree is empty, create root
        if self._root is None:
            self._root = self._Node(keys=[element])
            self._size += 1
            return
        
        # Find leaf node where element should be inserted
        leaf = self._find_leaf(self._root, element)
        
        # If element already exists, don't insert
        if element in leaf._keys:
            return
        
        # Insert element into leaf
        leaf._keys.append(element)
        leaf._keys.sort()
        self._size += 1
        
        # If leaf is overfull, split it
        if leaf.is_full() and len(leaf._keys) > 3:
            self._split_node(leaf)
    
    def _find_leaf(self, node, element):
        """Find the leaf node where element should be inserted."""
        if node.is_leaf():
            return node
        
        child_index = node.find_child_index(element)
        if child_index < len(node._children):
            return self._find_leaf(node._children[child_index], element)
        
        return node  # This shouldn't happen in a well-formed tree
    
    def _split_node(self, node):
        """Split a node that has 4 keys."""
        if len(node._keys) != 4:
            return
        
        # Middle key moves up to parent
        middle_key = node._keys[1]
        left_keys = [node._keys[0]]
        right_keys = [node._keys[2], node._keys[3]]
        
        # Create new right node
        right_node = self._Node(parent=node._parent, keys=right_keys)
        
        # Handle children if not leaf
        if not node.is_leaf():
            left_children = node._children[:2]
            right_children = node._children[2:]
            
            node._children = left_children
            right_node._children = right_children
            
            # Update parent pointers for right children
            for child in right_children:
                child._parent = right_node
        
        # Update current node to be left node
        node._keys = left_keys
        
        # If this is root, create new root
        if node._parent is None:
            new_root = self._Node(keys=[middle_key], children=[node, right_node])
            node._parent = new_root
            right_node._parent = new_root
            self._root = new_root
        else:
            # Insert middle key into parent
            parent = node._parent
            parent._keys.append(middle_key)
            parent._keys.sort()
            
            # Insert right node into parent's children
            key_index = parent._keys.index(middle_key)
            parent._children.insert(key_index + 1, right_node)
            
            # If parent is overfull, split it recursively
            if len(parent._keys) > 3:
                self._split_node(parent)
    
    def delete(self, element):
        """Delete an element from the tree."""
        if self._root is None:
            return False
        
        # Find the node containing the element
        node = self._find_node_with_key(self._root, element)
        if node is None:
            return False
        
        self._size -= 1
        
        # Case 1: Element is in a leaf node
        if node.is_leaf():
            node._keys.remove(element)
            if len(node._keys) == 0 and node != self._root:
                self._fix_underflow(node)
            elif len(node._keys) == 0 and node == self._root:
                self._root = None
        else:
            # Case 2: Element is in internal node
            # Replace with predecessor or successor
            key_index = node._keys.index(element)
            
            # Find inorder predecessor (rightmost key in left subtree)
            predecessor_node = node._children[key_index]
            while not predecessor_node.is_leaf():
                predecessor_node = predecessor_node._children[-1]
            
            # Replace element with predecessor
            predecessor = predecessor_node._keys[-1]
            node._keys[key_index] = predecessor
            
            # Remove predecessor from leaf
            predecessor_node._keys.remove(predecessor)
            if len(predecessor_node._keys) == 0:
                self._fix_underflow(predecessor_node)
        
        return True
    
    def _find_node_with_key(self, node, key):
        """Find the node containing the specified key."""
        if key in node._keys:
            return node
        
        if node.is_leaf():
            return None
        
        child_index = node.find_child_index(key)
        if child_index < len(node._children):
            return self._find_node_with_key(node._children[child_index], key)
        
        return None
    
    def _fix_underflow(self, node):
        """Fix underflow when a node has no keys."""
        if node == self._root:
            if len(node._children) == 1:
                self._root = node._children[0]
                self._root._parent = None
            return
        
        parent = node._parent
        node_index = parent._children.index(node)
        
        # Try to borrow from left sibling
        if node_index > 0:
            left_sibling = parent._children[node_index - 1]
            if len(left_sibling._keys) > 1:
                # Borrow from left sibling
                borrowed_key = left_sibling._keys.pop()
                parent_key = parent._keys[node_index - 1]
                parent._keys[node_index - 1] = borrowed_key
                node._keys.insert(0, parent_key)
                
                if not left_sibling.is_leaf():
                    borrowed_child = left_sibling._children.pop()
                    borrowed_child._parent = node
                    node._children.insert(0, borrowed_child)
                return
        
        # Try to borrow from right sibling
        if node_index < len(parent._children) - 1:
            right_sibling = parent._children[node_index + 1]
            if len(right_sibling._keys) > 1:
                # Borrow from right sibling
                borrowed_key = right_sibling._keys.pop(0)
                parent_key = parent._keys[node_index]
                parent._keys[node_index] = borrowed_key
                node._keys.append(parent_key)
                
                if not right_sibling.is_leaf():
                    borrowed_child = right_sibling._children.pop(0)
                    borrowed_child._parent = node
                    node._children.append(borrowed_child)
                return
        
        # Merge with sibling
        if node_index > 0:
            # Merge with left sibling
            left_sibling = parent._children[node_index - 1]
            separator_key = parent._keys.pop(node_index - 1)
            left_sibling._keys.append(separator_key)
            left_sibling._keys.extend(node._keys)
            left_sibling._children.extend(node._children)
            
            # Update parent pointers
            for child in node._children:
                child._parent = left_sibling
            
            parent._children.remove(node)
        else:
            # Merge with right sibling
            right_sibling = parent._children[node_index + 1]
            separator_key = parent._keys.pop(node_index)
            node._keys.append(separator_key)
            node._keys.extend(right_sibling._keys)
            node._children.extend(right_sibling._children)
            
            # Update parent pointers
            for child in right_sibling._children:
                child._parent = node
            
            parent._children.remove(right_sibling)
        
        # Check if parent needs fixing
        if len(parent._keys) == 0:
            self._fix_underflow(parent)
    
    def display(self):
        """Display the tree structure."""
        if self._root is None:
            print("Tree is empty")
        else:
            self._display(self._root, 0)
    
    def _display(self, node, depth):
        """Recursive helper to display the tree structure."""
        if node is None:
            return
        
        # Display current node
        indent = "  " * depth
        print(f"{indent}Keys: {node._keys}")
        
        # Display children
        if not node.is_leaf():
            print(f"{indent}Children:")
            for i, child in enumerate(node._children):
                print(f"{indent}  Child {i}:")
                self._display(child, depth + 2)
    
    def size(self):
        """Return the number of elements in the tree."""
        return self._size
    
    def is_empty(self):
        """Check if the tree is empty."""
        return self._size == 0


