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

class CoordinateSys:
    """A coordinate system which may support transformations to and
       from the base coordinate system."""

    def __init__(self, name, base=None, basis=None, pos=None):
        """Constructor:
           name: name of the coordinate system.
           base: the coordinate system that this one is defined in 
                 terms of.
           basis: the basis vectors of this coordinate system,
                  expressed in terms of the base coordinate system.
           pos: the position of the origin of this coordinate system,
                expressed in terms of the base coordinate system."""
        self._name = name
        self._base = base # The coordinate system this is based on.
        self._basis = basis # The basis matrix.
        self._pos = pos # The position of the origin in terms of the base.

    def getName(self):
        """Return the coordinate system's name."""
        return self._name

    def setName(self, name):
        """Set the coordinate system's name."""
        self._name = name

    def getBase(self):
        """Return the coordinate system which this is based upon."""
        return self._base

    def setBase(self, newBase):
        """Set the new base coordinate system for this coordinate system."""
        self._base = newBase

        if (newBase == self):
            self._base = None
            raise ValueError('Cannot assign a coordinate system ' +
                             'to be its own base.')

    def setPos(self, pos):
        self._pos = pos

    def getPos(self):
        return self._pos

    def transformToBase(self, vec):
        """Transform a vector from this coordinate system into the 
           base coordinate system."""
        # TODO: Implement
        pass

    def transformFromBase(self, vec):
        """Transform a vector from the base coordinate system into this 
           coordinate system."""
        # TODO: Implement
        pass
