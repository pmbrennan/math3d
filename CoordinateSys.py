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
        if name is not None:
            self._name = name
        else:
            self._name = ''

        # The coordinate system this is based on. None will be typically
        # used to indicate that this is the global coordinate system.
        self._parent = parent

        # The basis matrix should be 3x3. The rows should be:
        # 
        # | Row # | Description                                         |
        # +-------+-----------------------------------------------------+
        # | 0     | x basis vector (row vector, in parent coordinates.) |
        # | 1     | y basis vector (row vector, in parent coordinates.) |
        # | 2     | z basis vector (row vector, in parent coordinates.) |
        # 
        # Therefore M * (x - O) = x' where:
        # M = the basis vector
        # O = origin of this coordinate system, in parent coordinate system.
        # x = vector in parent coordinate system
        # x' = vector in this coordinate system
        # TODO: error out if this matrix is not 3x3 and orthonormal.
        # TODO: error out if there is no parent coordinate system!
        if basis is not None:
            self._basis = basis # The basis matrix.
        else:
            self._basis = Matrix.identity(3)

        # We don't assign a value to this until we need it.
        self._basisTranspose = None

        # The position of the origin in terms of the parent.
        # TODO: error out if there is no parent coordinate system!
        if origin is not None:
            self._origin = origin 
        else:
            self._origin = Vector(0.0, 0.0, 0.0)

    def getName(self):
        """Return the coordinate system's name."""
        return self._name

    def setName(self, name):
        """Set the coordinate system's name."""
        self._name = name

    def getParent(self):
        """Return the coordinate system which this is based upon."""
        return self._parent

    def setParent(self, newParent):
        """Set the new parent coordinate system for this coordinate system."""
        self._parent = newParent

        if (newParent == self):
            self._parent = None
            raise ValueError('Cannot assign a coordinate system ' +
                             'to be its own parent.')

    def setOrigin(self, origin):
        'Set the origin position of this coordinate system.'
        self._origin = origin

    def getOrigin(self):
        'Get the origin position of this coordinate system.'
        return self._origin

    def transformToParentSystem(self, vec):
        """Transform a vector from this coordinate system into the 
           parent coordinate system."""
        if self._basisTranspose is None:
            self._basisTranspose = self._basis.transpose()
        return self._basisTranspos.multv(vec) + self._origin

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

