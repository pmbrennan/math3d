#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103
# disable=C0103,R0201,W0212,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# W0212 : Access to a protected member %s of a client class
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX

"""
Quaternion definition.
"""

#import math
import unittest

from Vector import Vector
#from Matrix import Matrix

########################################################################
# Quaternion
class Quaternion:
    """Representation of a quaternion, defined as:

    s + ai + bj + ck
    or
    [s,v]

    where s,a,b,c are scalars, v is a vector, 

    and i, j, k are defined such that:
    i^2 = j^2 = k^2 = ijk = -1
    ij = k, jk = i, ki = j
    ji = -k, kj = -i, ik = -j
    """

    def __init__(self, s, a, b, c):
        self._printSpec = '%f'
        self._s = s
        self._v = Vector(a, b, c)

    @staticmethod
    def fromScalarVector(s, v):
        """Define a quaternion from a scalar and a vector."""
        # TODO: Refactor for performance.
        return Quaternion(s, v[0], v[1], v[2])

    def __str__(self):
        return '[ %s, %s ]' % (self._printSpec % self._s, self._v)

    def str2(self):
        """Alternate way to represent a Quaternion as a string."""
        signs = [ ('+' if f >= 0 else '-') for f in self._v ]
        vals = [ abs(f) for f in self._v ]

        return '%s %s %si %s %sj %s %sk' % (self._s, 
                                            signs[0],
                                            vals[0],
                                            signs[1],
                                            vals[1],
                                            signs[2],
                                            vals[2])

    def __eq__(self, q):
        'Equality operator.'
        return self._s == q._s and self._v == q._v

    def __ne__(self, q):
        'Not equals'
        return not self.__eq__(q)

    def compare(self, seq):
        """Compare the quaternion to a sequence assumed to be in
        the form [ s, a, b, c ]."""
        return (len(seq) == 4 and 
                self._s == seq[0] and self._v[0] == seq[1] and
                self._v[1] == seq[2] and self._v[2] == seq[3])

    def __add__(self, q):
        'Return self + q'
        return Quaternion(self._s + q._s, self._v[0] + q._v[0],
                          self._v[1] + q._v[1], self._v[2] + q._v[2])

    def __sub__(self, q):
        'Return self - q'
        return Quaternion(self._s - q._s, self._v[0] - q._v[0],
                          self._v[1] - q._v[1], self._v[2] - q._v[2])

    def scale(self, s):
        'Scale this quaternion by scalar s in-place.'
        self._s = self._s * float(s)
        self._v.scale(s)

    def mults(self, s):
        'Return self * scalar as a new Quaternion.'
        r = Quaternion.fromScalarVector(self._s, self._v)
        r.scale(s)
        return r

    def mul1(self, q):
        """Multiplication Algorithm 1:"""
        s = self._s * q._s - self._v.dot(q._v)
        v = q._v.mults(self._s) + self._v.mults(q._s) + self._v.cross(q._v)
        return Quaternion.fromScalarVector(s, v)

    def mul2(self, q):
        """Multiplication Algorithm 2:"""
        s = (self._s * q._s - self._v[0] * q._v[0] - 
             self._v[1] * q._v[1] - self._v[2] * q._v[2])
        a = (self._s * q._v[0] + self._v[0] * q._s + 
             self._v[1] * q._v[2] - self._v[2] * q._v[1])
        b = (self._s * q._v[1] - self._v[0] * q._v[2] + 
             self._v[1] * q._s + self._v[2] * q._v[0])
        c = (self._s * q._v[2] + self._v[0] * q._v[1] - 
             self._v[1] * q._v[0] + self._v[2] * q._s)
        return Quaternion(s, a, b, c)

########################################################################
# Unit tests for Quaternions
class QuaternionTest(unittest.TestCase):

    'Unit tests for Quaternions'

    def setUp(self):
        ''
        pass

    def tearDown(self):
        ''
        pass

    def testEquals(self):
        'Test equality operator.'
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(1, 2, 3, 4)
        assert q1 == q2
        assert not (q1 != q2)
        q3 = Quaternion.fromScalarVector(1, Vector(2, 3, 4))
        assert q2 == q3

    def testCompare(self):
        'Test comparison.'
        q = Quaternion(1, 2, 3, 4)
        assert q.compare([1, 2, 3, 4])
        assert not q.compare([1, 2, 3, 4, 5])
        assert not q.compare([0, 2, 3, 4])

    def testAdd(self):
        'Test quaternion addition'
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        assert q1 + q2 == Quaternion(6, 8, 10, 12)
        
    def testSub(self):
        'Test quaternion subtraction.'
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        assert (q2 - q1).compare([4, 4, 4, 4])

    def testScale(self):
        'Test quaternion scaling.'
        q1 = Quaternion(1, 2, 3, 4)
        q2 = q1.mults(3)
        assert q1.compare([1, 2, 3, 4])
        assert q2.compare([3, 6, 9, 12])

        q2.scale(5)
        assert q2.compare([15, 30, 45, 60])

    def testMul(self):
        'Test Quaternion multiplication'
        q1 = Quaternion(-2, 0, 0, 0)
        q2 = Quaternion(5, 0, 0, 0)

        assert(q1.mul1(q2).compare([-10, 0, 0, 0]))
        assert(q1.mul1(q2) == q1.mul2(q2))

        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(4, 3, 2, 1)
        
        assert(q1.mul1(q2) == Quaternion(-12, 6, 24, 12))
        assert(q1.mul1(q2) == q1.mul2(q2))

        qa = Quaternion(1, 2, 3, 4)
        qb = Quaternion(2, 3, 4, 5)
        assert qa.mul1(qb).compare([-36, 6, 12, 12])
        assert qa.mul2(qb).compare([-36, 6, 12, 12])

    def testMul2(self):
        'Verify that Quaternion obeys the basic laws of quaternions.'
        neg1 = Quaternion(-1, 0, 0, 0)
        i = Quaternion(0, 1, 0, 0)
        j = Quaternion(0, 0, 1, 0)
        k = Quaternion(0, 0, 0, 1)
        negi = i.mults(-1)
        negj = j.mults(-1)
        negk = k.mults(-1)


        assert(i.mul1(i) == neg1)          # i^2 == -1
        assert(j.mul1(j) == neg1)          # j^2 == -1
        assert(k.mul1(k) == neg1)          # k^2 == -1
        assert(i.mul1(j).mul1(k) == neg1)  # ijk == -1

        assert(i.mul1(j) == k)             # ij == k
        assert(j.mul1(k) == i)             # jk == i
        assert(k.mul1(i) == j)             # ki == j

        assert(j.mul1(i) == negk)          # ji == -k
        assert(k.mul1(j) == negi)          # kj == -i
        assert(i.mul1(k) == negj)          # ik == -j

    def testMul3(self):
        'Verify that Quaternion obeys the basic laws of quaternions.'
        neg1 = Quaternion(-1, 0, 0, 0)
        i = Quaternion(0, 1, 0, 0)
        j = Quaternion(0, 0, 1, 0)
        k = Quaternion(0, 0, 0, 1)
        negi = i.mults(-1)
        negj = j.mults(-1)
        negk = k.mults(-1)


        assert(i.mul2(i) == neg1)          # i^2 == -1
        assert(j.mul2(j) == neg1)          # j^2 == -1
        assert(k.mul2(k) == neg1)          # k^2 == -1
        assert(i.mul2(j).mul2(k) == neg1)  # ijk == -1

        assert(i.mul2(j) == k)             # ij == k
        assert(j.mul2(k) == i)             # jk == i
        assert(k.mul2(i) == j)             # ki == j

        assert(j.mul2(i) == negk)          # ji == -k
        assert(k.mul2(j) == negi)          # kj == -i
        assert(i.mul2(k) == negj)          # ik == -j

    def testPrint(self):
        'Test printing functionality'
        q = Quaternion(1, 2, 3, 4)
        assert q.__str__() == '[ 1.000000, [ 2.000000, 3.000000, 4.000000 ] ]'
    