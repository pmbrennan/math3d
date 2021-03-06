#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0212 : Access to a protected member %s of a client class

"""
Matrix definition.
"""

import unittest
import math
from Vector import Vector
from MathUtil import MathUtil

########################################################################
class Matrix:

    """
    Matrix : a two-dimensional array of numbers, or a vector of row vectors.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a matrix with the passed elements. The arguments
        list is assumed to be a number of row objects, which are each
        a sequence composed of items which can be cast as numbers. Any
        other input will raise an exception.

        rows=n and cols=n will be honored as keyword arguments, and
        will pad the data as appropriate. However, inconsistencies
        will raise exceptions. If cols=n is not specified, then
        the passed rows must all be the same size."""
        self.mNRows = 0
        self.mNCols = 0
        self.mV = [] # Matrix row data
        self.mPrintSpec = '%f' # String formatter for elements

        # Read the arguments list and add the data
        if (args is not None) and (len(args) > 0) :
            self.mNRows = len(args)
            self.mNCols = max([len(row) for row in args])
            for row in args:
                newrow = [ float(f) for f in row ]
                if len(newrow) < self.mNCols :
                    newrow.extend([0.0]*(self.mNCols - len(newrow)))
                self.mV.append(newrow)

        # Now read the keyword arguments
        kwrows = None
        kwcols = None
        for (kw, val) in kwargs.iteritems():
            if (kw == 'rows'):
                kwrows = val
                if kwrows < self.mNRows:
                    raise IndexError('Cannot specify fewer rows ' +
                                     'than supplied in constructor.')
            elif (kw == 'cols'):
                kwcols = val
                if kwcols < self.mNCols:
                    raise IndexError('Cannot specify fewer columns ' +
                                     'than supplied in constructor.')
            else:
                raise KeyError("keyword '%s' not supported here." % kw)

        if (kwrows is None) and (kwcols is not None):
            kwrows = max(self.mNRows, 1)

        if (kwrows is not None) and (kwcols is None):
            kwcols = max(self.mNCols, 1)

        # Pad out the rows
        if kwrows is not None:
            rownum = self.mNRows
            while rownum < kwrows:
                self.mV.append([0.0]*self.mNCols)
                rownum += 1
            self.mNRows = kwrows

        # Pad out the columns
        if kwcols is not None:
            nextra = kwcols - self.mNCols
            for row in self.mV:
                row.extend([0.0]*nextra)
            self.mNCols = kwcols

    def __str__(self):
        """Return the string representation of this matrix."""
        rv = '[ '
        first = True
        for row in self.mV:
            if not first:
                rv += '\n  '
            else:
                first = False
            rv += '[' + ','.join([
                (' ' + self.mPrintSpec) % e for e in row]) + ' ]'
        rv += ' ]'
        return rv

    @staticmethod
    def identity(size):
        """Return an square identity matrix of the indicated size, 
        e.g. a 3x3 identity matrix is returned by a call to
        identity(3)."""
        m = Matrix(rows=size, cols=size)
        for i in range(0, size):
            m[i][i] = 1.0
        return m

    def clone(self): 
        """Return a copy of this matrix."""
        v = [ r[:] for r in self.mV ]
        return Matrix(*v)

    def size(self):
        """Return a tuple indicating size in (rows,cols)."""
        return (self.mNRows, self.mNCols)

    def __getitem__(self, index):
        """Get the item at index."""
        return self.mV.__getitem__(index)

    def __setitem__(self, key, value):
        """Set the item at index to value."""
        self.mV.__setitem__(key, value)

    def __eq__(self, m):
        """Equality operator"""
        # If it's a list, skip the size check; if it's not
        # the right size, we'll error out on the loop.
        if not(isinstance(m, list)) and (self.size() != m.size()):
            return False
        i = 0
        for row in self.mV:
            j = 0
            for element in row:
                if element != m[i][j]:
                    return False
                j += 1
            i += 1
        return True

    def __ne__(self, m):
        return not(self.__eq__(m))

    def __add__(self, m):
        """Add matrix m to self, returning a new matrix:

        M = self + m
        """
        if (self.size() != m.size()):
            raise TypeError('Cannot add dissimilar matrices.')
        nrows, ncols = self.size()
        rv = Matrix(rows=nrows, cols=ncols)
        v = []
        for i in range(0, nrows):
            r = []
            for j in range(0, ncols):
                r.append(self.mV[i][j] + m.mV[i][j])
            v.append(r)
        rv.mV = v
        return rv

    def scale(self, scalar):
        """Multiply a matrix by a scale factor."""
        self.mV = [ [ e * float(scalar) for e in row ] for row in self.mV ]

    def mults(self, scalar):
        'Multiply vector by a scalar, return a new vector'
        r = Matrix(rows = self.mNRows, cols = self.mNCols)
        r.mV = [ [ e * float(scalar) for e in row ] for row in self.mV ]
        return r

    def getRow(self, index):
        """Get a copy of a row of the matrix, as a Vector."""
        if (index < 0) or (index >= self.mNRows):
            raise IndexError('Index out of bounds : %s' % index)

        return Vector.fromSequence(self.mV[index])

    def getColumn(self, index):
        """Get a copy of a column of the matrix, as a Vector."""
        if (index < 0) or (index >= self.mNCols):
            raise IndexError('Index out of bounds : %s' % index)

        return Vector.fromSequence([self.mV[i][index] 
                                    for i in range(0, self.mNRows)])

    def multv(self, v):
        """Multiply a matrix by a vector, returning a Vector:

        V = self * v
        """
        if self.mNCols != len(v):
            raise TypeError(
                "Incompatible object sizes: %sx%s matrix and %s vector" % 
                (self.mNRows, self.mNCols, len(v)))
        V = Vector(size=self.mNRows)
        for i in range(0, self.mNRows):
            V[i] = sum([ self[i][j] * v[j] for j in range(0, self.mNCols) ])
        return V

    def multm(self, m):
        """Multiply a matrix by a matrix, returning a matrix:

        M = self * m
        """
        if self.mNCols != m.mNRows:
            raise TypeError(
                "Incompatible object sizes: %sx%s matrix and %sx%s matrix" %
                (self.mNRows,self.mNCols,m.mNRows,m.mNCols))
        M = Matrix(rows=self.mNRows, cols=m.mNCols)

        # TODO: This could be optimized.
        for i in range(0, self.mNRows):
            for j in range(0, m.mNCols):
                d = 0.0
                for k in range(0, self.mNCols):
                    d += self.mV[i][k] * m.mV[k][j]
                M.mV[i][j] = d
        
        return M

    @staticmethod
    def vectorOuterProduct(v1, v2):
        'Compute the vector outer product (or tensor product) of two vectors.'
        rows = len(v1)
        cols = len(v2)
        m = Matrix(rows=rows, cols=cols)
        for i in range(rows):
            for j in range(cols):
                m[i][j] = v1[i] * v2[j]
        return m

    def transpose(self):
        """Return a new matrix which is the transpose of this matrix."""
        r = Matrix(rows=self.mNCols, cols=self.mNRows)
        for i in range(self.mNRows):
            for j in range(self.mNCols):
                r.mV[j][i] = self.mV[i][j]
        return r

    def round(self, places): # Returns reference to self
        """Round all the elements of this matrix to the specified number
        of decimal places."""
        for row in self.mV:
            for i in range(self.mNCols):
                row[i] = round(row[i], places)
        return self

    @staticmethod
    def rotationMatrixForZ(angle_in_degrees):
        """Given an angle in degrees, compute the rotation matrix
        about the Z axis."""
        (s, c) = MathUtil.getSinCos(angle_in_degrees)
        return Matrix([c, -s, 0], [s, c, 0], [0, 0, 1])

    @staticmethod
    def rotationMatrixForX(angle_in_degrees):
        """Given an angle in degrees, compute the rotation matrix
        about the X axis."""
        (s, c) = MathUtil.getSinCos(angle_in_degrees)
        return Matrix([1, 0, 0], [0, c, -s], [0, s, c])

    @staticmethod
    def rotationMatrixForY(angle_in_degrees):
        """Given an angle in degrees, compute the rotation matrix
        about the Y axis."""
        (s, c) = MathUtil.getSinCos(angle_in_degrees)
        return Matrix([c, 0, s], [0, 1, 0], [-s, 0, c])

    @staticmethod
    def azimuthAltitude(azimuth_degrees, altitude_degrees):
        """Given an azimuth and an altitude in degrees, compute the
        corresponding rotation matrix.
        altitude must be in the range -90 to +90.
        """
        if altitude_degrees < -90.0 or altitude_degrees > 90.0:
            raise ValueError(
                'altitude_degrees must be in the range [-90,+90].')
        A = Matrix.rotationMatrixForY(-altitude_degrees)
        B = Matrix.rotationMatrixForZ(azimuth_degrees)
        return B.multm(A)

    def ludecomp(self): # Returns (index[], d)
        """
        Perform a LU decomposition of this matrix.

        LU-decomposition is the process of replacing a matrix [A] with the
        matrices [L] and [U] such that

        [A] = [L][U]

        where [L] has nonzero elements only on the diagonal and below, and [U]
        has nonzero elements only on the diagonal and above.  Furthermore, the
        diagonal elements of [L] are all defined to be 1.  LU-decomposition is a
        popular technique for the solution of matrix equations.

        Upon exit, this matrix will be overwritten such that the elements below
        the diagonal will be the nonzero elements of [L], and the elements on
        the diagonal and above will be the nonzero elements of [U].

        index will be an integer array representing the row interchanges in the
        matrix.

        d will be +1 if the number of row interchanges is even, and -1 if
        the number of row interchanges is odd.

        Algorithm adapted from Press, Teukolsky, Vettering, and Flannery,
        _Numerical Recipes in C, 2nd ed._
        """

        d = 1.0
        n = self.mNRows
        vv = [ 0 ] * n
        index = [ 0 ] * n
        imax = -1
        TINY = 1e-20

        for i in range(n):
            big = 0.0
            for j in range(n):
                temp = abs(self.mV[i][j])
                if temp > big:
                    big = temp
            if big == 0.0:
                raise ValueError('Singular matrix error')
            vv[i] = big

        for j in range(n):
            for i in range(j):
                csum = self.mV[i][j]
                for k in range(i):
                    csum -= self.mV[i][k] * self.mV[k][j]
                self.mV[i][j] = csum
            big = 0.0
            for i in range(j, n):
                csum = self.mV[i][j]
                for k in range(j):
                    csum -= self.mV[i][k] * self.mV[k][j]
                self.mV[i][j] = csum
                dum = vv[i] * abs(csum)
                if dum >= big:
                    big = dum
                    imax = i
            if j != imax:
                for k in range(n):
                    dum = self.mV[imax][k]
                    self.mV[imax][k] = self.mV[j][k]
                    self.mV[j][k] = dum
                d = -d
                vv[imax] = vv[j]
            index[j] = imax
            if self.mV[j][j] == 0:
                self.mV[j][j] = TINY
            if j != n:
                dum = 1.0 / (self.mV[j][j])
                for i in range(j+1, n):
                    self.mV[i][j] *= dum

        return (index, d)

    def lubacksub(self, index, b):
        """
        LU Back-substitution.

        Solves the set of n linear equations [A] * x = b for X.

        self stands not for A, but as the LU decomposition of A, as
        computed by Matrix.ludecomp().

        index is the index array created by ludecomp.

        b will be overwritten with the values of x.

        This function will return the vector x.
        """

        ii = 0
        n = self.mNRows

        for i in range(n):
            ip = index[i]
            sum = b[ip]
            b[ip] = b[i]
            if ii != 0:
                for j in range(ii, i):
                    sum -= self.mV[i][j] * b[j]
            elif sum != 0:
                ii = i
            b[i] = sum
            
        for i in range(n-1, -1, -1):
            sum = b[i]
            for j in range(i+1, n):
                sum -= self.mV[i][j] * b[j]
            b[i] = sum / self.mV[i][i]

        return b

########################################################################
# Matrix tests
class MatrixTest(unittest.TestCase):

    """Unit tests for Matrix."""

    def testConstructors(self):
        'Tests around constructors.'
        m = Matrix()
        assert m.size() == (0, 0)
        m = Matrix(rows=3)
        assert m.size() == (3, 1)
        m = Matrix([1, 0], [0, 1])
        assert m.size() == (2, 2)

        m = Matrix([1], [2, 6], [3])
        assert m == [[1, 0], [2, 6], [3, 0]]

        hitError = False
        try:
            m = Matrix([1], [2, 6], [3], rows=2)
        except IndexError, e:
            assert e.message == \
                'Cannot specify fewer rows than supplied in constructor.'
            hitError = True
        assert hitError

        hitError = False
        try:
            m = Matrix([1], [2, 6], [3], cols=1)
        except IndexError, e:
            assert e.message == \
                'Cannot specify fewer columns than supplied in constructor.'
            hitError = True
        assert hitError

        hitError = False
        try:
            m = Matrix([1], [2, 6], [3], foo=1)
        except KeyError, e:
            assert e.message == "keyword 'foo' not supported here."
            hitError = True
        assert hitError

        m = Matrix(cols=2)
        assert m.size() == (1, 2)

    def testString(self):
        'Test string functions'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        assert ('%s' % m) == """[ [ 1.000000, 2.000000, 3.000000 ]
  [ 4.000000, 5.000000, 6.000000 ]
  [ 7.000000, 8.000000, 9.000000 ] ]"""

    def testGettersAndSetters(self):
        'Tests around get and set operators.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        assert m.size() == (3, 3)
        assert m[1][1] == 5
        m[1][1] = -7
        assert m[1][1] == -7
        assert m[1][2] == 6

    def testEquality(self):
        'Test equality operator.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m2 = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m3 = Matrix([1, 2], [4, 5], [7, 8])
        assert m == m
        assert m == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert m != [[1, 2, 3], [4, 5, 6], [7, 8, -9]]
        assert m == m2
        assert m != m3

    def testScaling(self):
        'Test Matrix scaling.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m.scale(3)
        assert m == [[3, 6, 9], [12, 15, 18], [21, 24, 27]]

    def testMatrixTimesScalar(self):
        'Test matrix-scalar multiplication.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m2 = m.mults(3)
        assert m == [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ] 
        assert m2 == [[3, 6, 9], [12, 15, 18], [21, 24, 27]]

    def testGetRow(self):
        'Test row accessor.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        v = m.getRow(1)
        assert v == [4, 5, 6]
        caughtException = False
        try:
            v = m.getRow(-1)
        except IndexError:
            caughtException = True
        assert caughtException
        caughtException = False
        try:
            v = m.getRow(900)
        except IndexError:
            caughtException = True
        assert caughtException

    def testSetRow(self):
        'test row setter'
        m = Matrix([1, 2], [3, 4], [5, 6])
        m[1] = [0, 0]
        assert m == [[1, 2], [0, 0], [5, 6]]

    def testGetColumn(self):
        'Test column accessor.'
        m = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        v = m.getColumn(1)
        assert v == [2, 5, 8]
        v = m.getColumn(2)
        assert v == [3, 6, 9]
        caughtException = False
        try:
            v = m.getColumn(-1)
        except IndexError:
            caughtException = True
        assert caughtException
        caughtException = False
        try:
            v = m.getColumn(900)
        except IndexError:
            caughtException = True
        assert caughtException

    def testIdentity(self):
        'Test identity ctor.'
        m = Matrix.identity(1)
        assert m == [[1]]
        m = Matrix.identity(3)
        assert m == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        m.scale(-2)
        assert m == [[-2, 0, 0], [0, -2, 0], [0, 0, -2]]

    def testAdd(self):
        'Test matrix addition.'
        m1 = Matrix([1, 2], [3, 4])
        m2 = Matrix([5, 6], [7, 8])

        m3 = m1 + m2
        assert m1 == [[1, 2], [3, 4]]
        assert m2 == [[5, 6], [7, 8]]
        assert m3 == [[6, 8], [10, 12]]

        m1 = Matrix([1, 2, 3], [4, 5, 6])
        m2 = Matrix([7, 8, 9], [10, 11, 12])
        m3 = m1 + m2
        assert m1 == [[1, 2, 3], [4, 5, 6]]
        assert m2 == [[7, 8, 9], [10, 11, 12]]
        assert m3 == [[8, 10, 12], [14, 16, 18]]

        hitError = False
        m1 = Matrix([1, 1], [1, 1])
        m2 = Matrix([1, 1], [1, 1], [1, 1])
        try:
            m3 = m1 + m2
        except TypeError:
            hitError = True
        assert hitError

    def testMatrixVectorMultiplication(self):
        'Test matrix-vector multiplication.'
        m = Matrix.identity(3)
        v1 = [1, 2, 3]
        v2 = m.multv(v1)
        assert v1 == v2
        # Rotation matrix: 90 degrees counterclockwise
        m = Matrix([ 0, -1 ], [1, 0])
        v = Vector(1, 1)
        v = m.multv(v)
        assert v == [-1, 1]
        v = m.multv(v)
        assert v == [-1, -1]
        v = m.multv(v)
        assert v == [1, -1]
        v = m.multv(v)
        assert v == [1, 1]

        hitError = False
        m = Matrix([1, 1], [1, 1])
        v = Vector(1, 2, 3)
        try:
            m.multv(v)
        except TypeError:
            hitError = True
        assert hitError

    def testMatrixMatrixMultiplication(self):
        'Test matrix-matrix multiplication.'
        m1 = Matrix.identity(3)
        m2 = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m3 = m1.multm(m2)
        assert m2 == m3

        m1 = Matrix([1, 2, 3], [4, 5, 6])
        m2 = Matrix([-1, 2, -3, 4], [-5, 6, -7, 8], [-9, 10, -11, 12])
        m3 = m1.multm(m2)
        assert m3.size() == (2, 4)
        assert m3[0][0] == Vector(1, 2, 3).dot(Vector(-1, -5, -9))
        assert m3 == [ [ -38, 44, -50, 56 ], [ -83, 98, -113, 128 ] ]
        
        hitError = False
        try:
            m3 = m2.multm(m1)
        except TypeError:
            hitError = True

        assert hitError

    def testTranspose(self):
        'Test transpose function.'
        m1 = Matrix([1, 2, 3, 4], [5, 6, 7, 8])
        m2 = m1.transpose()
        assert m2 == [[1, 5], [2, 6], [3, 7], [4, 8]]

    def testOuterProduct(self):
        'Test the vector outer product routine.'
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5)
        m = Matrix.vectorOuterProduct(v1, v2)
        assert m == [[4, 5], [8, 10], [12, 15]]

    def testRound(self):
        'Test matrix rounding'
        m = Matrix([-1.00001, 0.99999], [0.000001, -0.000000034])
        m.round(4) == [[-1, 1], [0, 0]], m

    def testBasicRotationMatrices(self):
        'Test the basic rotation matrices.'
        m = Matrix.rotationMatrixForZ(45)

        v = m.multv(Vector(1.0, 0.0, 0.0))
        assert v.round(6) == [ 0.707107, 0.707107, 0.000000 ]
        v = m.multv(m.multv(Vector(1.0, 0.0, 0.0)))
        assert v.round(6) == [ 0.0, 1.0, 0.0 ]

        i = 0
        v = Vector(1.0, 0.0, 0.0)
        while (i < 8):
            v = m.multv(v)
            i += 1

        assert v.norm() == 1.0
        assert v.round(5) == [1.0, 0.0, 0.0], v

        assert m.multv(Vector(0, 0, 1)) == [0, 0, 1]

        m = Matrix.rotationMatrixForX(120)
        
        v = m.multv(Vector(0.0, 1.0, 0.0))
        assert round(v.norm(), 6) == 1.0, v
        assert v.round(6) == [ 0.0, -0.5, 0.866025 ]

        v = m.multv(Vector(0.0, 1.0, 0.0))
        v = m.multv(v)
        v = m.multv(v)

        assert abs(v.norm() - 1.0) < 0.000000000000001, v.norm() 
        assert round(v.norm(), 6) == 1.0, v.norm()
        assert v.round(6) == [ 0.0, 1.0, 0.0 ]

        m = Matrix.rotationMatrixForY(60)
        
        v = m.multv(Vector(0.0, 0.0, 1.0))
        assert abs(v.norm()) == 1.0, v.norm()
        assert v.round(6) == [ 0.866025, 0.0, 0.5 ], v

        v = m.multv(Vector(0.0, 0.0, 1.0))
        v = m.multv(v)
        v = m.multv(v)
        v = m.multv(v)
        v = m.multv(v)
        v = m.multv(v)

        assert abs(v.norm() - 1.0) < 0.000000000000001, v.norm() 
        assert round(v.norm(), 6) == 1.0, v.norm()
        assert v.round(6) == [ 0.0, 0.0, 1.0 ]

    def testAzmAlt(self):
        'Test the azimuth/altitude code.'

        hitError = False
        try:
            m = Matrix.azimuthAltitude(67, -99)
        except ValueError:
            hitError = True
        assert hitError

        hitError = False
        try:
            m = Matrix.azimuthAltitude(67, 187)
        except ValueError:
            hitError = True
        assert hitError

        Azm = 45
        Alt = 60

        m = Matrix.azimuthAltitude(Azm, Alt)

        (sinAzm, cosAzm) = MathUtil.getSinCos(Azm)
        (sinAlt, cosAlt) = MathUtil.getSinCos(Alt)

        ihat = m.multv(Vector(1, 0, 0))

        places = 7
        assert round(ihat[0], places) == round(cosAzm * cosAlt, places), \
            round(ihat[0], places) - round(cosAzm * cosAlt, places)
        assert round(ihat[1], places) == round(sinAzm * cosAlt, places), \
            round(ihat[1], places) - round(sinAzm * cosAlt, places)
        assert round(ihat[2], places) == round(sinAlt, places), \
            round(ihat[2], places) - round(sinAlt, places)

    def testClone(self):
        m1 = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m2 = m1.clone()
        assert m1 == m2
        m2[1][0] = -4
        assert m1 != m2

    def testludecomp(self):
        # TODO: Fix this test and the function under test!
        return
        A = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        m2 = A.clone()
        (index, d) = m2.ludecomp()
        b = Vector(6, -1, 3)
        x = m2.lubacksub(index, b.clone())

        assert(False)
        #print "b = %s" % b
        #print "x = %s" % x
        #print "A * x = %s" % A.multv(x)

