#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,W0212,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# W0212 : Access to a protected member %s of a client class
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX

"""
Quaternion definitions and useful utilities.
"""

import math
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
    def fromScalarVector(scalar, vector):
        """Define a quaternion from a scalar and a vector."""
        # TODO: Refactor for performance.
        return Quaternion(scalar, vector[0], vector[1], vector[2])

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
        """Multiplication Algorithm 1:
        This is a very nice definition of the quaternion multiplication
        operator, but it is terribly inefficient."""
        s = self._s * q._s - self._v.dot(q._v)
        v = q._v.mults(self._s) + self._v.mults(q._s) + self._v.cross(q._v)
        return Quaternion.fromScalarVector(s, v)

    def mul2(self, q):
        """Multiplication Algorithm 2: This is a much more efficient
        implementation of quaternion multiplication. It isover 3x faster than
        mul1."""
        s = (self._s * q._s - self._v[0] * q._v[0] - 
             self._v[1] * q._v[1] - self._v[2] * q._v[2])
        a = (self._s * q._v[0] + self._v[0] * q._s + 
             self._v[1] * q._v[2] - self._v[2] * q._v[1])
        b = (self._s * q._v[1] - self._v[0] * q._v[2] + 
             self._v[1] * q._s + self._v[2] * q._v[0])
        c = (self._s * q._v[2] + self._v[0] * q._v[1] - 
             self._v[1] * q._v[0] + self._v[2] * q._s)
        return Quaternion(s, a, b, c)

    def mulq(self, q):
        "Multiply two quaternions and return a new quaternion product."
        s = (self._s * q._s - self._v[0] * q._v[0] - 
             self._v[1] * q._v[1] - self._v[2] * q._v[2])
        a = (self._s * q._v[0] + self._v[0] * q._s + 
             self._v[1] * q._v[2] - self._v[2] * q._v[1])
        b = (self._s * q._v[1] - self._v[0] * q._v[2] + 
             self._v[1] * q._s + self._v[2] * q._v[0])
        c = (self._s * q._v[2] + self._v[0] * q._v[1] - 
             self._v[1] * q._v[0] + self._v[2] * q._s)
        return Quaternion(s, a, b, c)

    def conj(self):
        'return the conjugate of a quaternion.'
        return Quaternion(self._s, -self._v[0], -self._v[1], -self._v[2])

    def norm(self):
        'return the norm of a quaternion.'
        return math.sqrt(sum([x*x for x in self._v]) + self._s * self._s)

    def normalize(self):
        'reset the quaternion so that it has norm = 1'
        n_reciprocal = 1.0 / self.norm()
        self._s = self._s * n_reciprocal
        self._v.scale(n_reciprocal)

    def inverse(self):
        """Invert the quaternion and return the inverse.
        inverse = conjugate / (norm^2)
        """
        n = self.norm()
        c = self.conj()
        d = 1.0 / (n * n)
        c.scale(d)
        return c

    def invert(self):
        'Invert in place.'
        n = self.norm()
        d = 1.0 / (n * n)
        for i in range(0,3) : 
            self._v[i] *= -d
        self._s *= d

    @staticmethod
    def forRotation(axis, angle):
        """
        Return the quaternion which represents a rotation about
        the provided axis (vector) by angle (in radians).
        """
        # TODO enforce requirement that axis must be a unit vector.
        half_angle = angle * 0.5
        c = math.cos(half_angle)
        s = math.sin(half_angle)
        return Quaternion.fromScalarVector(c, axis.mults(s))

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

        qa = Quaternion(2, -2, 3, -4)
        qb = Quaternion(1, -2, 5, -6)
        
        assert qa + qb == Quaternion(3, -4, 8, -10)
        assert qa - qb == Quaternion(1, 0, -2, 2)
        
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

        qa = Quaternion(2, -2, 3, -4)
        qb = Quaternion(1, -2, 5, -6)

        assert qb.mulq(qa).compare([-41, -8, 17, -12])
        assert qa.mulq(qb).compare([-41, -4, 9, -20])

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

    def testMulq4(self):
        'Test Quaternion multiplication'
        q1 = Quaternion(-2, 0, 0, 0)
        q2 = Quaternion(5, 0, 0, 0)

        assert(q1.mulq(q2).compare([-10, 0, 0, 0]))

        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(4, 3, 2, 1)
        
        assert(q1.mulq(q2) == Quaternion(-12, 6, 24, 12))

        qa = Quaternion(1, 2, 3, 4)
        qb = Quaternion(2, 3, 4, 5)
        assert qa.mulq(qb).compare([-36, 6, 12, 12])

        neg1 = Quaternion(-1, 0, 0, 0)
        i = Quaternion(0, 1, 0, 0)
        j = Quaternion(0, 0, 1, 0)
        k = Quaternion(0, 0, 0, 1)
        negi = i.mults(-1)
        negj = j.mults(-1)
        negk = k.mults(-1)

        assert(i.mulq(i) == neg1)          # i^2 == -1
        assert(j.mulq(j) == neg1)          # j^2 == -1
        assert(k.mulq(k) == neg1)          # k^2 == -1
        assert(i.mulq(j).mulq(k) == neg1)  # ijk == -1

        assert(i.mulq(j) == k)             # ij == k
        assert(j.mulq(k) == i)             # jk == i
        assert(k.mulq(i) == j)             # ki == j

        assert(j.mulq(i) == negk)          # ji == -k
        assert(k.mulq(j) == negi)          # kj == -i
        assert(i.mulq(k) == negj)          # ik == -j

    def testPrint(self):
        'Test printing functionality'
        q = Quaternion(1, 2, 3, 4)
        assert q.__str__() == '[ 1.000000, [ 2.000000, 3.000000, 4.000000 ] ]'

    def testConjugate(self):
        'Test conjugate operation.'
        q1 = Quaternion(1, 2, 3, 4)
        assert q1.conj().compare([1, -2, -3, -4])
        q2 = q1.conj()
        assert q1.mulq(q2).compare([30, 0, 0, 0])

    def testNorm(self):
        'Test norm function'
        q1 = Quaternion(1, 4, 4, -4)
        assert q1.norm() == 7

        q2 = Quaternion(1, 4, 4, -4)
        q2.normalize()
        assert q2.norm() == 1

    def testInvert(self):
        'Test Quaternion inversion.'
        q1 = Quaternion(1, 2, 3, 4)
        q2 = q1.inverse()
        assert q1 != q2
        q1.invert()
        assert q1 == q2
        assert q1.compare([1.0/30.0, -2.0/30.0, -3.0/30.0, -4.0/30.0])

    def testAlternateRepresentation(self):
        'Test the alternate representation of the quaternion.'
        q = Quaternion(3, -4, 5, -7)
        s = q.str2()
        assert s == '3 - 4.0i + 5.0j - 7.0k', s

    def testRotationalQuaternion(self):
        'Test the quaternion representation of a rotation.'
        axis = Vector(1, 1, 1).normalize()
        angle = 2.0 # radians!
        q1 = Quaternion.forRotation(axis, angle)
        
        vv = math.sin(1.0) / (math.sqrt(3.0))
        cc = math.cos(1.0)
        q2 = Quaternion(cc, vv, vv, vv)
        assert q1.__str__() == q2.__str__(), '%s %s'%(q1,q2)

    
