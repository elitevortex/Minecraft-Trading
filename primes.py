"""Contains code for PrimeNumberIterator class, a prime number generator """

from __future__ import annotations

__author__ = ''
__docformat__ = 'reStructuredText'

def is_prime(n: int) -> bool:
    """
    Checks whether n is prime or not.
    Returns true if prime, false otherwise.
    from week 9 applied class - Miller Rabin algorithm
    complexity:
        best case: O(1) when n is < 2
        worst case: O(S*log(N)) where N is the number to be checked
                    and S is the variable s (number of iterations performed)
    """
    # these checks work for up to 2^32.
    vals = [2, 7, 61]
    # not prime when number is less than 2
    if n < 2:
        return False
    d, s = n - 1, 0
    # not prime when number is even
    while d % 2 == 0:
        d //= 2
        s += 1
    for v in vals:
        if v >= n:
            break
        x = pow(v, d, n)
        if x == 1 or x == n-1:
            continue
        good = False
        for r in range(1, s):
            x = (x*x) % n
            if x == n-1:
                good = True
                break
        if not good:
            return False
    return True


class LargestPrimeIterator():
    """ 
    Prime number generator
    in each iteration finds the first (largest) prime number less than the upper bound

    complexity:
        unless otherwise stated all methods have a best/worst case complexity of O(1)
    """
    
    def __init__(self, upper_bound: int, factor: int):
        """ initialises the class and checks that numbers are integers """
        assert(type(upper_bound) == int), "Upper bound is not of type int"
        self.upper_bound = upper_bound

        assert(type(factor) == int), "Factor is not of type int"
        self.factor = factor

    def __iter__(self): 
        '''Returns self'''
        return self
    
    def __next__(self) -> int:
        """ returns the largest prime number less than the upper bound 
        complexity:
            best case: O(is_prime) where the upper_bound - 1 is a prime number
            worst case: O(n * is_prime) where n is the difference between the upper_bound 
            and the next largest prime number less than the upper_bound
        """
        for num in range(self.upper_bound - 1, 0, -1):
            if is_prime(num):
                """ upper bound is updated when a prime number is found, prime number is returned """
                self.upper_bound = num * self.factor
                return num
