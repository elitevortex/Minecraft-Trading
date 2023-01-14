""" Hash Table Implementation

Defines a Hash Table using Linear Probing for conflict resolution.
"""

from __future__ import annotations
__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'


from referential_array import ArrayR
from typing import TypeVar, Generic

from primes import LargestPrimeIterator

T = TypeVar('T')


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
        arguments:
            expected_size (int) - the maximum number of elements that will be added to the table
            tablesize_override (int) - given if user wants to override the table size
        
        Complexity: O(1)
        """
        # Makes sure expected size is of type int
        assert(type(expected_size) == int), "Expected size is not of type int"
        self.expected_size = expected_size
        
        # setting the table size to the exact value of overrided value of table size
        if tablesize_override > -1:
            tablesize = tablesize_override
            
        else:
            # class creates a reasonably sized table size based on value of expected size
            prime = iter(LargestPrimeIterator(int(self.expected_size * 2.2), 2))
            tablesize = next(prime)
            
        self.tablesize = tablesize
        self.table = ArrayR(tablesize)

        # Number of elements
        self.count = 0

        # Statistic variables
        # Number of total conflicts
        self.conflict_count = 0
        # Total distance probed
        self.probe_total = 0
        # Length of the longest probe
        self.probe_max = 0
        # Number of times rehashing is done
        self.rehash_count = 0

        
    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
            Args: key (str) - a string that we want to hash 
            Complexity: O(N) where N is the length of the key
        """
        value = 0
        a = 31415
        b = 27183
        for char in key:
            value = (ord(char) + a*value) % len(self.table)
            a = a * b % (len(self.table)-1)
        return value

    def statistics(self) -> tuple:
        """ finds various statistics of the hash table 
        returns a tuple containing the following information:
            conflict_count (int) - the total number of conflicts
            probe_total (int) - the total distance probed throughout the execution of the code 
            probe_max (int) - the length of the longest probe chain throughout the execution of the code
            rehash_count (int) - the total number of times the table has been rehashed

        complexity:
            O(K*N*L) where N is the number of items in the table
                and L is the length of the hashes list (number of unique hash indexes)
                and K is the length of the key
            worst-case: O(K*N^2) where each key hashes to a different index
             best-case: O(K*N) where each key hases to the same index
        """
        # -----TOTAL CONFLICTS-------#
        # add each index each item is hashed to
        hashes = list()
        for key in self.keys():         # O(n) where n is the number of items in the hash table
            cur_hash = self.hash(key)   # O(K)
            # if the hash pos is already in the list add to the conflict count
            if cur_hash in hashes:      # O(L), where L is the length of the hashes list
                self.conflict_count += 1 
            else:
                # otherwise, append the current index
                hashes.append(cur_hash)
        
        return (self.conflict_count, self.probe_total, self.probe_max, self.rehash_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)
        
        cur_probe_chain = 0

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    # update probe max if necessary
                    if cur_probe_chain > self.probe_max:
                        self.probe_max = cur_probe_chain
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                # update probe max if necessary
                if cur_probe_chain > self.probe_max:
                        self.probe_max = cur_probe_chain
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)

                # update probe total and chain length
                self.probe_total += 1
                cur_probe_chain += 1

        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
            
            :complexity: O(linear_probe) -> best case O(K), worst case O(K+N)
            where K is the size of the key and N is tablesize
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
            
            :complexity: O(linear_probe) -> best case O(K), worst case O(K+N)
            where K is the size of the key and N is tablesize
        """
        # rehash if the table is more than half full
        if self.count > self.tablesize / 2:
            self._rehash()
        
        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)


    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data
        

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values
            :complexity:
            best/worst case: O(N * (__setitem__ complexity)) 
            therefore:
                best case: O(N * K) when first pos is empty
                worst case: O(N * K * N) when whole array is searched 
                where K is the size of the key and N is tablesize
        """ 
        # Instantiate new table size using iterator
        # Multiply by 2.2 to ensure maximal prime number table size
        new_size = next(iter(LargestPrimeIterator(int(self.tablesize * 2.2), 2)))
        old_table = self.table
        self.table = ArrayR(new_size)
        self.count = 0
        self.tablesize = new_size

        # move everything from the old table to the new table
        for i in range(len(old_table)): # O(n)
            if old_table[i] is not None:
                # Gets key & data from old_table
                key, data = old_table[i]    # O(get_item) = O(linear_probe)

                # Stores in new self.table
                self[key] = data        # O(set_item) = O(linear_probe)

        # Update rehash count every call
        self.rehash_count += 1


    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
