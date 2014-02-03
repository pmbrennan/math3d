#!/usr/bin/python

"""
A simple and easy to use 3d math library.

This module contains reference implementations for :

Vector (variable-length) 
Matrix (variable-dimension)
Quaternion

with appropriate unit tests to ensure correct implementation.

The focus of this project is to provide a reference implementation
of some useful mathematical objects. The goals are:

- Clarity
- Correctness
- Test Coverage

These routines are not intended to replace good, high-performance tools like
NumPy or SciPi, but instead to demonstrate how these objects are supposed to
work and to provide a point of reference. Particularly, these routines have not
been optimized for performance, either in memory or in time. I wrote these
routines to supplement my own understanding of the math demonstrated here, and I
am releasing it as open source to encourage others to achieve the same (or
hopefully a greater!) level of understanding.

"""

from Vector import Vector, VectorTest
from Matrix import Matrix, MatrixTest, MathUtil, MathUtilTest
from CoordinateSys import CoordinateSys, CoordinateSysTest
from Quaternion import Quaternion, QuaternionTest

# import time                                                

# q1 = Quaternion(1, 2, 3, 4)
# q2 = Quaternion(5, 6, 7, 8)

# def useMul1(nTimes):
#     startTime = int(round(time.time() * 1000))
#     i = 0
#     while i < nTimes:
#         q3 = q1.mul1(q2)
#         i = i + 1
#     endTime = int(round(time.time() * 1000))
#     print 'Total time = %s ms' % (endTime - startTime)

# def useMul2(nTimes):
#     startTime = int(round(time.time() * 1000))
#     i = 0
#     while i < nTimes:
#         q3 = q1.mul2(q2)
#         i = i + 1
#     endTime = int(round(time.time() * 1000))
#     print 'Total time = %s ms' % (endTime - startTime)





