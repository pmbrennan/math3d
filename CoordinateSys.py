#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0212 : Access to a protected member %s of a client class

"""
Coordinate System definition.
"""

import unittest
from Matrix import Matrix
from Vector import Vector

class CoordinateSys:
    """A coordinate system which may support transformations to and
       from the parent coordinate system."""

    def __init__(self, name, parent=None, basis=None, origin=None):
        """Constructor:
           name: name of the coordinate system.
           parent: the coordinate system that this one is defined in 
                 terms of.
           basis: the basis vectors of this coordinate system,
                  expressed in terms of the parent coordinate system.
           origin: the position of the origin of this coordinate system,
                expressed in terms of the parent coordinate system."""

        self.mName = None
        self.mParent = None
        self.mBasis = None
        self.mBasisTranspose = None
        self.mOrigin = None

        self.setName(name)
        self.setParent(parent)
        self.setBasis(basis)
        self.setOrigin(origin)

    def getName(self):
        """Return the coordinate system's name."""
        return self.mName

    def setName(self, name):
        """Set the coordinate system's name."""
        if name is not None:
            self.mName = name
        else:
            self.mName = ''

    def getParent(self):
        """Return the coordinate system which this is based upon."""
        return self.mParent

    def setParent(self, parent):
        """Set the coordinate system this is based on. None will be typically
        used to indicate that this is the global coordinate system."""
        if (parent is not None and parent == self):
            self.mParent = None
            raise ValueError('Cannot assign a coordinate system ' +
                             'to be its own parent.')
        else:
            self.mParent = parent

    def setBasis(self, basis):
        """Set the basis matrix for this coordinate system.  The basis matrix
        should be 3x3. The rows should be:
        
        | Row # | Description                                         |
        +-------+-----------------------------------------------------+
        | 0     | x basis vector (row vector, in parent coordinates.) |
        | 1     | y basis vector (row vector, in parent coordinates.) |
        | 2     | z basis vector (row vector, in parent coordinates.) |
        
        Therefore M * (x - O) = x' where:
        M = the basis vector
        O = origin of this coordinate system, in parent coordinate system.
        x = vector in parent coordinate system
        x' = vector in this coordinate system."""
        # TODO: error out if this matrix is not 3x3 and orthonormal.
        # TODO: error out if there is no parent coordinate system!
        if basis is not None:
            self.mBasis = basis # The basis matrix.
        else:
            self.mBasis = Matrix.identity(3)

        # We don't assign a value to this until we need it.
        self.mBasisTranspose = None

    def getBasis(self):
        'Get the basis matrix of this coordinate system.'
        return self.mBasis

    def setOrigin(self, origin):
        'Set the origin position of this coordinate system.'
        # The position of the origin in terms of the parent.
        # TODO: error out if there is no parent coordinate system!
        # TODO: error out if the origin vector is not length 3.
        if origin is not None:
            self.mOrigin = origin 
        else:
            self.mOrigin = Vector(0.0, 0.0, 0.0)

    def getOrigin(self):
        'Get the origin position of this coordinate system.'
        return self.mOrigin

    @staticmethod
    def compare(a, b):
        'Perform a comparison operation between two Coordinate Systems.'
        if (a is None and b is None):
            return True
        elif (a is None or b is None):
            return False
        else:
            return(a == b)

    def __eq__(self, other):
        'Equality operator'
        return (CoordinateSys.compare(self.mParent, other.mParent) and
                CoordinateSys.compare(self.mBasis, other.mBasis) and
                CoordinateSys.compare(self.mOrigin, other.mOrigin))

    def transformToParentSystem(self, vec):
        """Transform a vector from this coordinate system into the 
           parent coordinate system."""
        if self.mBasisTranspose is None:
            self.mBasisTranspose = self.mBasis.transpose()
        return self.mBasisTranspose.multv(vec) + self.mOrigin

    def transformFromParentSystem(self, vec):
        """Transform a vector from the parent coordinate system into this 
           coordinate system."""
        return self.mBasis.multv(vec - self.mOrigin)

class CoordinateSysTest(unittest.TestCase):

    """Unit tests for CoordinateSys."""

    def setUp(self):
        'Set up'
        pass

    def tearDown(self):
        'Tear down'
        pass

    def testConstructors(self):
        'Test constructors'
        c = CoordinateSys('Arthur')
        assert c.mName == 'Arthur'
        assert c.getName() == 'Arthur'
        assert c.mParent is None
        assert c.mBasis == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        assert c.mBasisTranspose is None
        assert c.mOrigin == [0, 0, 0]

        c = CoordinateSys(None)
        assert c.getName() == ''

        basis1 = Matrix([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
        basis2 = Matrix([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])

        c1 = CoordinateSys('foo', basis=basis1)
        assert c1.getBasis() == basis2

        c2 = CoordinateSys('bar', origin=Vector(4, 5, 6))
        assert c2.getOrigin() == [4, 5, 6]

        c2.setParent(c1)
        assert c2.getParent() == c1

    def testSetParent(self):
        'Test setParent method'
        c1 = CoordinateSys('foo')
        hitError = False
        try:
            c1.setParent(c1)
        except ValueError:
            hitError = True
        assert hitError

    def testTransforms(self):
        'Test Transformation methods.'
        # TODO: test non-identity basis matrices.
        c1 = CoordinateSys('Global')
        c2 = CoordinateSys('Local', parent=c1, origin=Vector(1, 2, 3))

        v1 = Vector(0, 0, 0)
        v2 = c2.transformToParentSystem(v1)
        assert v2 == [1, 2, 3]
        v3 = c2.transformFromParentSystem(v2)
        assert v3 == v1

