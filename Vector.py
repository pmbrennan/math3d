#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,R0904,W0511,W0142
# C0103 : Invalid name "%s" (should match %s)
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0212 : Access to a protected member %s of a client class
# W0142 : Used * or ** magic

"""
Vector definition.
"""

import math
import unittest

########################################################################
class Vector:

    """Vector : a 1-dimensional array of real numbers."""

    def __init__(self, *args, **kwargs):
        """Initialize a vector with the passed elements.

        The arguments list is assumed to be a some number of items which can be
        cast as numbers. Any other input will raise an exception.

        size=n will be honored as a keyword argument, but will raise
        an exception if the requested size is smaller than the number of
        items allocated to accomodate any previously specified elements.

        """
        self.mV = [] # Elements of the vector
        self.mPrintSpec = '%f' # String formatter for elements
        for x in args:
            self.mV.append(float(x))
        
        for arg in kwargs:
            if arg not in [ 'size', ]: # Add keywords here
                raise ValueError("keyword '%s' not recognized" % arg)

        if 'size' in kwargs and kwargs['size'] is not None:
            if kwargs['size'] < len(args):
                raise IndexError('Cannot allocate fewer items ' + 
                                 'than already specified.')
            else:
                nToAdd = kwargs['size'] - len(args)
                while nToAdd > 0:
                    self.mV.append(0.0)
                    nToAdd -= 1

    @staticmethod
    def fromSequence(seq): # returns Vector
        """Initialize a vector from a single sequence object, e.g. a list
        or tuple."""
        return Vector(*seq)

    @staticmethod
    def zeros(num):
        """Initialize a vector as a sequence of num zeros."""
        if num < 1:
            raise IndexError('num must be >= 1.')
        return Vector.fromSequence([0] * num)

    @staticmethod
    def ones(num):
        """Initialize a vector as a sequence of num ones."""
        if num < 1:
            raise IndexError('num must be >= 1.')
        return Vector.fromSequence([1] * num)

    def clone(self):
        """Return a copy of the Vector."""
        v = self.mV[:]
        return Vector.fromSequence(v)

    def __str__(self):
        """Returns the string representation of the vector."""
        rv = '[ '
        n = len(self.mV)
        i = 0
        for f in self.mV:
            rv += self.mPrintSpec % f
            i += 1
            if (i < n):
                rv += ', '
            else:
                rv += ' '
        rv += ']'
        return rv

    def __len__(self):
        "Return the length of the vector."
        return self.mV.__len__()

    def __getitem__(self, key):
        "Get an item in the vector."
        return self.mV.__getitem__(key)

    def __setitem__(self, key, value):
        "Set the value of an item in the vector."
        self.mV.__setitem__(key, value)

    def __delitem__(self, key):
        self.mV.__delitem__(key)

    def __add__(self, v):
        if (len(self) != len(v)):
            raise IndexError('Vectors to be added must be the same size.')
        return Vector.fromSequence([ x[0]+x[1] for x in zip(self, v) ])

    def __sub__(self, v):
        if (len(self) != len(v)):
            raise IndexError('Vectors to be added must be the same size.')
        return Vector.fromSequence([ x[0]-x[1] for x in zip(self, v) ])

    def scale(self, s):
        """Scale a vector in place by a given scalar."""
        for n in range(len(self.mV)):
            self.mV[n] *= s

    def mults(self, s):
        """Multiply a vector by a scalar, return the scaled
        vector. The original vector remains unchanged."""
        prod = Vector.fromSequence(self.mV)
        prod.scale(s)
        return prod

    def dot(self, v):
        """Dot Product or Scalar Product or Inner Product"""
        if (len(self) != len(v)):
            raise IndexError('Vectors to be dotted must be the same size.')
        return sum([x[0]*x[1] for x in zip(self, v)])

    def __eq__(self, v):
        """Equality"""
        if (len(self) != len(v)):
            return False

        n = len(self)
        for i in range(0, n):
            if self[i] != v[i]:
                return False
        return True

    def __ne__(self, v):
        """Not equals"""
        return not(self.__eq__(v))

    def cross(self, v):
        """Cross Product or Vector Product
        Multiply 2 3x3 vectors to get a 3rd vector which obeys the relation
        R = v1 v2 sin theta

        | i   j   k  |
        | x1  y1  z1 |
        | x2  y2  z2 |

        """
        if (len(self.mV) != 3) or (len(v) != 3):
            raise IndexError('Cross product is only for 2 3-vectors.')

        (x1, y1, z1) = (self.mV[0], self.mV[1], self.mV[2])
        (x2, y2, z2) = (v[0], v[1], v[2])
        x = y1 * z2 - y2 * z1
        y = z1 * x2 - z2 * x1
        z = x1 * y2 - x2 * y1
        return Vector(x, y, z)

    def norm(self):
        """Return the Euclidean norm of the vector"""
        return math.sqrt(sum([x*x for x in self.mV]))

    def normalize(self):
        """Turn the vector into a unit vector pointing in the same direction.
        Do the operation in place."""
        n = 1.0 / self.norm()
        self.mV = [ x * n for x in self.mV ]
        return self

    def round(self, places):
        'Round the vector elements to a given number of decimal places.'
        self.mV = [ round(x, places) for x in self.mV ]
        return self

########################################################################
# Vector Unit Tests
class VectorTest(unittest.TestCase):
    """Unit tests for Vector class."""

    def testLen(self):
        """Test len()"""
        vector = Vector()
        assert len(vector) == 0
        vector.mV = [ 1, 2, -3 ]
        assert vector.__len__() == 3
        assert len(vector) == 3
        assert vector[0] == 1
        assert vector[1] == 2
        assert vector[2] == -3

    def testMultipleConstructors(self):
        'Test multiple ways of constructing a vector.'
        vector = Vector(3, 4, 5, 7)
        assert len(vector) == 4
        assert vector[2] == 5.0

        hitError = False
        try:
            vec = Vector(1, 2, 3, foo='bar')
        except ValueError, e:
            assert e.message == "keyword 'foo' not recognized"
            hitError = True
        assert hitError

    def testStaticCtor(self):
        'Test the static fromSequence ctor.'
        v1 = Vector.fromSequence((1, 2, 3))
        assert len(v1) == 3
        assert v1[0] == 1
        assert v1[1] == 2
        assert v1[2] == 3

        v2 = Vector.fromSequence([21, 6, -9, 8.0/4.0])
        assert len(v2) == 4
        assert v2[0] == 21
        assert v2[1] == 6
        assert v2[2] == -9
        assert v2[3] == 2

    def testSettersAndGetters(self):
        'Test vector setters and getters.'
        vector = Vector(4, 5, 6)
        assert vector[1] == 5
        vector[1] = -8
        assert vector[1] == -8

    def testDel(self):
        'test the delete function.'
        vector = Vector(4, 5, 6)
        assert len(vector) == 3
        del(vector[1])
        assert len(vector) == 2

    def testScale(self):
        'test vector scaling.'
        v1 = Vector(-3, .8, 7)
        v1.scale(11)
        assert v1 == [ -33.000000, 8.800000, 77.000000 ]
        v2 = v1.mults(-2)
        assert v1 == [ -33.000000, 8.800000, 77.000000 ]
        assert v2 == [ 66, -17.6, -154]

    def testAdd(self):
        'test vector addition.'
        v1 = Vector(4, 5, 6)
        v2 = Vector(7, 8, 9, 10)
        v3 = Vector(-9, 3, 8)
        v4 = [1, 2, 3]

        hitException = False
        try:
            vsum = v1 + v2
        except IndexError:
            hitException = True
        assert hitException

        vsum = v1 + v3
        assert len(vsum) == 3
        assert vsum[0] == -5
        assert vsum[1] == 8
        assert vsum[2] == 14

        vsum = v1 + v4
        assert len(vsum) == 3
        assert vsum[0] == 5
        assert vsum[1] == 7
        assert vsum[2] == 9

    def testSub(self):
        'test vector subraction.'
        v1 = Vector(4, 5, 6)
        v2 = Vector(7, 8, 9, 10)
        v3 = Vector(-9, 3, 8)
        v4 = [1, 2, 3]

        hitException = False
        try:
            vsum = v1 - v2
        except IndexError:
            hitException = True
        assert hitException

        vsum = v1 - v3
        assert len(vsum) == 3
        assert vsum[0] == 13
        assert vsum[1] == 2
        assert vsum[2] == -2

        vsum = v1 - v4
        assert len(vsum) == 3
        assert vsum[0] == 3
        assert vsum[1] == 3
        assert vsum[2] == 3

    def testSum(self):
        """Test vector summing code."""
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        v1 += v2
        assert(len(v1) == 3)
        assert v1[0] == 5
        assert v1[1] == 7
        assert v1[2] == 9

        v1 = Vector(9, 8, 7)
        v2 = Vector(3, 2, 1)
        v1 -= v2
        assert len(v1) == 3
        assert v1[0] == 6
        assert v1[1] == 6
        assert v1[2] == 6

    def testDot(self):
        """Test the vector dot routine."""
        v1 = Vector(1, 2, 3, 4)
        v2 = Vector(0, 1, 0, 0)
        v3 = Vector(1, 1, 1, 1)
        assert(v1.dot(v2) == 2)
        assert(v1.dot(v3) == 10)

        assert Vector(0.1, -0.2, 0.3).dot(Vector(5, 1, -1)) == 0

        hitException = False
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6, 7)
        try:
            v3 = v1.dot(v2)
        except IndexError:
            hitException = True
        assert hitException

    def testNorm(self):
        """Test computation of the vector norm."""
        assert(Vector(0, 3, 4).norm() == 5)
        assert(Vector(3, 4).norm() == 5)
        assert Vector(0, 3, 0, 0, 4, 0, size=10).norm() == 5

    def testStringify(self):
        """Test the string code."""
        v1 = Vector(1, 6, -8, 0)
        assert ('%s' % v1) == '[ 1.000000, 6.000000, -8.000000, 0.000000 ]'

    def testEquals(self):
        """Test the equality operator."""
        v1 = Vector(3, 4, 5)
        assert (v1 == [3, 4, 5])
        assert (v1 != [0, 2, 4])
        v2 = Vector(3.0, 4.0, 5.000)
        assert (v1 == v2)
        v3 = Vector(2, 2)
        assert v1 != v3

    def testCross(self):
        """Test v cross v code."""
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        assert v1.cross(v2) == [0, 0, 1]
        assert v1.cross([0, 1, 0]) == Vector(0, 0, 1)

        v3 = Vector(-1, 0, 0)
        assert v2.cross(v3) == [0, 0, 1]

        assert Vector(0, 0, 1).cross(Vector(1, 0, 0)) == Vector(0, 1, 0)
        c = 0.707106781 # Cos 45
        assert Vector(0, 0, 3).cross(Vector(2*c, 0, 2*c)) == Vector(
            0, 6*c, 0)

        c = 0.5 # cos 60deg
        s = 0.866025404 # sin 60deg
        assert Vector(0, 0, 3).cross(Vector(s, 0, c)) == Vector(0, 3*s, 0)
        assert Vector(0, 0, 3).cross([s, 0, c]) == [0, 3*s, 0]

        hitException = False
        try:
            v1 = Vector(1, 2, 3, 4)
            v2 = Vector(5, 6, 7, 8)
            v3 = v1.cross(v2)
        except IndexError:
            hitException = True
        assert hitException

    def testSize(self):
        """Test functionality around vector size code."""
        v1 = Vector(1, 2, 3, size=6)
        assert v1 == [1, 2, 3, 0, 0, 0]
        failed = False
        try:
            Vector(1, 2, 3, size=2)
        except IndexError:
            failed = True
        assert failed

        v3 = Vector(size=7)
        assert v3 == Vector(0, 0, 0, 0, 0, 0, 0)
        assert v3 == (0, 0, 0, 0, 0, 0, 0)

    def testZeros(self):
        """Test the zeros function."""
        v1 = Vector.zeros(3)
        assert v1 == (0, 0, 0)
        hitException = False
        try:
            Vector.zeros(0)
        except IndexError:
            hitException = True
        assert hitException
        hitException = False
        try:
            Vector.ones(-1)
        except IndexError:
            hitException = True
        assert hitException

    def testOnes(self):
        """Test the ones function."""
        v1 = Vector.ones(8)
        assert v1 == [1, 1, 1, 1, 1, 1, 1, 1, ]
        assert v1.norm() == math.sqrt(8)

    def testNormalize(self):
        """Test the normalize and norm functionality."""
        v1 = Vector.ones(4)
        n = v1.norm()
        assert n == 2
        assert v1.normalize() == [ 0.5, 0.5, 0.5, 0.5 ]
        
    def testClone(self):
        'Test the clone function.'
        v1 = Vector(1, 2, 3, 4, 5, 6, 7)
        v2 = v1.clone()
        assert v1 == v2
        v2[3] = -4
        assert v1 != v2
        assert v1.norm() == v2.norm()
