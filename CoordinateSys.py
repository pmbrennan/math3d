#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,W0212,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# W0212 : Access to a protected member %s of a client class
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX

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

        self._name = None
        self._parent = None
        self._basis = None
        self._basisTranspose = None
        self._origin = None

        self.setName(name)
        self.setParent(parent)
        self.setBasis(basis)
        self.setOrigin(origin)

    def getName(self):
        """Return the coordinate system's name."""
        return self._name

    def setName(self, name):
        """Set the coordinate system's name."""
        if name is not None:
            self._name = name
        else:
            self._name = ''

    def getParent(self):
        """Return the coordinate system which this is based upon."""
        return self._parent

    def setParent(self, parent):
        """Set the coordinate system this is based on. None will be typically
        used to indicate that this is the global coordinate system."""
        if (parent is not None and parent == self):
            self._parent = None
            raise ValueError('Cannot assign a coordinate system ' +
                             'to be its own parent.')
        else:
            self._parent = parent

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
            self._basis = basis # The basis matrix.
        else:
            self._basis = Matrix.identity(3)

        # We don't assign a value to this until we need it.
        self._basisTranspose = None

    def getBasis(self):
        'Get the basis matrix of this coordinate system.'
        return self._basis

    def setOrigin(self, origin):
        'Set the origin position of this coordinate system.'
        # The position of the origin in terms of the parent.
        # TODO: error out if there is no parent coordinate system!
        # TODO: error out if the origin vector is not length 3.
        if origin is not None:
            self._origin = origin 
        else:
            self._origin = Vector(0.0, 0.0, 0.0)

    def getOrigin(self):
        'Get the origin position of this coordinate system.'
        return self._origin

    def __eq__(self, other):
        'Equality operator'
        return (self._parent == other._parent and
                self._basis == other._basis and
                self._origin == other._origin)

    def transformToParentSystem(self, vec):
        """Transform a vector from this coordinate system into the 
           parent coordinate system."""
        if self._basisTranspose is None:
            self._basisTranspose = self._basis.transpose()
        return self._basisTranspose.multv(vec) + self._origin

    def transformFromParentSystem(self, vec):
        """Transform a vector from the parent coordinate system into this 
           coordinate system."""
        return self._basis.multv(vec - self._origin)

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
        assert c._name == 'Arthur'
        assert c.getName() == 'Arthur'
        assert c._parent is None
        assert c._basis == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        assert c._basisTranspose is None
        assert c._origin == [0, 0, 0]

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
        c1 = CoordinateSys('foo')
        hitError = False
        try:
            c1.setParent(c1)
        except ValueError:
            hitError = True
        assert hitError



