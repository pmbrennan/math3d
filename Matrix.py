#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,W0212,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# W0212 : Access to a protected member %s of a client class
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX

"""
Matrix definition.
"""

import unittest

from Vector import Vector

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
        self._nrows = 0
        self._ncols = 0
        self._v = []
        self._printSpec = '%f' # String formatter for elements

        # Read the arguments list and add the data
        if (args is not None) and (len(args) > 0) :
            self._nrows = len(args)
            self._ncols = max([len(row) for row in args])
            for row in args:
                newrow = [ float(f) for f in row ]
                if len(newrow) < self._ncols :
                    newrow.extend([0.0]*(self._ncols - len(newrow)))
                self._v.append(newrow)

        # Now read the keyword arguments
        kwrows = None
        kwcols = None
        for (kw, val) in kwargs.iteritems():
            if (kw == 'rows'):
                kwrows = val
                if kwrows < self._nrows:
                    raise IndexError('Cannot specify fewer rows ' +
                                     'than supplied in constructor.')
            elif (kw == 'cols'):
                kwcols = val
                if kwcols < self._ncols:
                    raise IndexError('Cannot specify fewer columns ' +
                                     'than supplied in constructor.')
            else:
                raise KeyError("keyword '%s' not supported here." % kw)

        if (kwrows is None) and (kwcols is not None):
            kwrows = max(self._nrows, 1)

        if (kwrows is not None) and (kwcols is None):
            kwcols = max(self._ncols, 1)

        # Pad out the rows
        if kwrows is not None:
            rownum = self._nrows
            while rownum < kwrows:
                self._v.append([0.0]*self._ncols)
                rownum += 1
            self._nrows = kwrows

        # Pad out the columns
        if kwcols is not None:
            nextra = kwcols - self._ncols
            for row in self._v:
                row.extend([0.0]*nextra)
            self._ncols = kwcols

    def __str__(self):
        """Return the string representation of this matrix."""
        rv = '[ '
        first = True
        for row in self._v:
            if not first:
                rv += '\n  '
            else:
                first = False
            rv += '[' + ','.join([
                (' ' + self._printSpec) % e for e in row]) + ' ]'
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

    def size(self):
        """Return a tuple indicating size in (rows,cols)."""
        return (self._nrows, self._ncols)

    def __getitem__(self, index):
        """Get the item at index."""
        return self._v.__getitem__(index)

    def __setitem__(self, key, value):
        """Set the item at index to value."""
        self._v.__setitem__(key, value)

    def __eq__(self, m):
        """Equality operator"""
        # If it's a list, skip the size check; if it's not
        # the right size, we'll error out on the loop.
        if not(isinstance(m, list)) and (self.size() != m.size()):
            return False
        i = 0
        for row in self._v:
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
                r.append(self._v[i][j] + m._v[i][j])
            v.append(r)
        rv._v = v
        return rv

    def scale(self, scalar):
        """Multiply a matrix by a scale factor."""
        self._v = [ [ e * float(scalar) for e in row ] for row in self._v ]

    def mults(self, scalar):
        'Multiply vector by a scalar, return a new vector'
        r = Matrix(rows = self._nrows, cols = self._ncols)
        r._v = [ [ e * float(scalar) for e in row ] for row in self._v ]
        return r

    def getRow(self, index):
        """Get a copy of a row of the matrix, as a Vector."""
        if (index < 0) or (index >= self._nrows):
            raise IndexError('Index out of bounds : %s' % index)

        return Vector.fromSequence(self._v[index])

    def getColumn(self, index):
        """Get a copy of a column of the matrix, as a Vector."""
        if (index < 0) or (index >= self._ncols):
            raise IndexError('Index out of bounds : %s' % index)

        return Vector.fromSequence([self._v[i][index] 
                                    for i in range(0, self._nrows)])

    def multv(self, v):
        """Multiply a matrix by a vector, returning a Vector:

        V = self * v
        """
        if self._ncols != len(v):
            raise TypeError(
                "Incompatible object sizes: %sx%s matrix and %s vector" % 
                (self._nrows, self._ncols, len(v)))
        V = Vector(size=self._nrows)
        for i in range(0, self._nrows):
            V[i] = sum([ self[i][j] * v[j] for j in range(0, self._ncols) ])
        return V

    def multm(self, m):
        """Multiply a matrix by a matrix, returning a matrix:

        M = self * m
        """
        if self._ncols != m._nrows:
            raise TypeError(
                "Incompatible object sizes: %sx%s matrix and %sx%s matrix" %
                (self._nrows,self._ncols,m._nrows,m._ncols))
        M = Matrix(rows=self._nrows, cols=m._ncols)

        # TODO: This could be optimized.
        for i in range(0, self._nrows):
            for j in range(0, m._ncols):
                d = 0.0
                for k in range(0, self._ncols):
                    d += self._v[i][k] * m._v[k][j]
                M._v[i][j] = d
        
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
        r = Matrix(rows=self._ncols, cols=self._nrows)
        for i in range(self._nrows):
            for j in range(self._ncols):
                r._v[j][i] = self._v[i][j]
        return r

########################################################################
# Matrix tests
class MatrixTest(unittest.TestCase):

    """Unit tests for Matrix."""

    def testCtors(self):
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

    def testGetSet(self):
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
