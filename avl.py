""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_tree_size(self, current: AVLTreeNode) -> int:
        """
            Get the size of the tree under the current node
            return current.tree_size if current is not None, otherwise return 0
            :complexity: O(1)
        """

        if current is not None:
            return current.tree_size
        return 0

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :raise: KeyError if the key already exists
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
                where D is the depth of the tree
                CompK is the complexity of comparing the keys
        """

        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
            
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise KeyError('Inserting duplicate item')

        # update current height and tree_size
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        current.tree_size = 1 + self.get_tree_size(current.left) + self.get_tree_size(current.right)
        # rebalance if nessessary:
        current = self.rebalance(current)
        
        return current


    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
                where D is the depth of the tree
                CompK is the complexity of comparing the keys

        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        # update current height and tree size
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        current.tree_size = 1 + self.get_tree_size(current.left) + self.get_tree_size(current.right)

        # rebalance if nessessary:
        current = self.rebalance(current)

        return current


    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        # find the child node and center tree
        child = current.right
        center = child.left

        # reassigning
        child.left = current
        current.right = center

        # recompute heights of child and current
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        # recompute tree sizes of child and current
        current.tree_size = 1 + self.get_tree_size(current.left) + self.get_tree_size(current.right)
        child.tree_size = 1 + self.get_tree_size(child.left) + self.get_tree_size(child.right)

        # return the new root
        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """
        # find the child node and center tree
        child = current.left
        center = child.right

        # reassigning
        child.right = current
        current.left = center

        # recompute heights of child and current
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        # recompute tree sizes of child and current
        current.tree_size = 1 + self.get_tree_size(current.left) + self.get_tree_size(current.right)
        child.tree_size = 1 + self.get_tree_size(child.left) + self.get_tree_size(child.right)

        # return the new root
        return child


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ 
        Compute the balance of the current node.

            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.

            Complexity: O(1)
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):  # O(1)
                current.right = self.right_rotate(child)                    # O(1)
            return self.left_rotate(current)                                # O(1)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def range_between(self, i: int, j: int) -> List:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.

        pre: 
            0 <= i <= j < self.length
        
        :complexity O(j - i + log(N)) where N is the total number of nodes in the tree
                    worst case: O(N) when i = 0 and j = N-1 (the whole tree is traversed)
        """
        return self.range_between_aux(self.root, i, j, self.length - 1, [])


    def range_between_aux(self, current : AVLTreeNode, i: int, j: int, max_index: int, l: List):
        """
        the auxilary method for range between
        arg:
            current - the current tree node
            i - the min index of the sorted list wanted
            j - the max index of the sorted list wanted
            max_index - the maximum index this node can have based on it's position in the tree
            l - the sorted list so far

        :complexity: O(j - i + log(N)) where N is the total number of nodes in the tree
            worst case: O(N) when i = 0 and j = N-1 (the whole tree is traversed)
        """
        # base case: if current is none return the list
        if current is None:
            return l

        # find the index of current by basing it on its max index and the number of nodes to its right
        if current.right is None:
            current_index = max_index
        else:
            current_index = max_index - current.right.tree_size

        # if the index is greater then i, check left
        if current_index > i:
            l = self.range_between_aux(current.left, i, j, current_index - 1, l)
        
        # if the index is within the desired range, add the node's item to the list
        if i <= current_index <= j:
            l.append(current.item)

        # if the index is less than j, check right
        if current_index < j:
            l = self.range_between_aux(current.right, i, j, max_index, l)

        return l
            

    def get_max(self) -> tuple([K,I]):
        """
        Returns a tuple of the biggest key and its value in the entire tree
        complexity: O(D) where D is the depth of the tree
        """
        current = self.root
        while current.right is not None:
            current = current.right
        return (current.key, current.item)
