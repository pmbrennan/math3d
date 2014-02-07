#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0212 : Access to a protected member %s of a client class

"""
Math Utility Methods.
"""

import unittest
import math

########################################################################
# Math utility methods

class MathUtil:

    """General math utilities, for operations which don't belong in
    specialized classes."""

    def __init__(self):
        'Initialization. Not really necessary at this time.'
        pass

    @staticmethod
    def roundsd(f, sigDigits): # returns float
        """
        Round a real number to a given number of significant digits.
        Will raise a ValueError for a non-positive number of significant
        digits or more than 10 significant digits.

        *IMPORTANT NOTE*
        This function is different from the standard Python round() because
        unlike round(), this function preserves the requested number of
        significant digits, rather than a requested number of places
        behind the decimal point. Examples:

        round(3.452, 2) = 3.45
        roundsd(3.452, 2) = 3.5
        roundsd(3.452, 3) = 3.45

        round(0.034, 2) = 0.03
        roundsd(0.034, 2) = 0.034

        round(0.0000000343, 3) = 0.0
        roundsd(0.0000000343, 3) = 3.43e-08
        
        """

        if (f == 0.0):
            return f

        f = float(f)
        negative = (f < 0.0)
        f = math.fabs(f)

        if sigDigits <= 0 or sigDigits > 10:
            raise ValueError('unsupported number of significant digits.')

        power = math.floor(math.log10(f))
        factor = 10 ** (power - sigDigits + 1)
        #print ('power = %s, sigDigits = %s, factor = %s' % 
        #       (power, sigDigits, factor))
        
        retval = (round(float(f) / factor)*factor)

        if negative:
            retval *= -1.0

        return retval

    @staticmethod
    def deg2rad(angle_in_degrees):
        'Convert an angle in degrees to an angle in radians.'
        return (angle_in_degrees * math.pi) / 180.0

    @staticmethod
    def getSinCos(angle_in_degrees):
        'A utility method to compute the trig functions of an angle.'
        angle = MathUtil.deg2rad(angle_in_degrees)
        return (math.sin(angle), math.cos(angle))

########################################################################
# Tests for math utility methods
class MathUtilTest(unittest.TestCase):
    
    """Unit tests for MathUtil."""

    def testCtor(self):
        'Test constructor.'
        mu = MathUtil()

    def testroundsd(self):
        'Test the rounding method.'
        assert MathUtil.roundsd(0.0, 15) == 0.0
        assert MathUtil.roundsd(0.99999, 3) == 1
        assert MathUtil.roundsd(0.00999, 3) == 0.00999
        assert MathUtil.roundsd(0.00999, 2) == 0.01
        
        assert MathUtil.roundsd(-0.00999, 3) == -0.00999

        hitError = False
        try:
            MathUtil.roundsd(0.4567, 17) # Too many sig digits.
        except ValueError:
            hitError = True
        assert hitError

        hitError = False
        try:
            MathUtil.roundsd(0.4567, -4) # Illegal # significant digits
        except ValueError:
            hitError = True
        assert hitError

    def testSinCos(self):
        'Test the sin,cos utility method'
        assert MathUtil.getSinCos(0.0) == (0, 1)
        (s, c) = MathUtil.getSinCos(90)
        assert round(s, 5) == 1.0, round(s, 5)
        assert round(c, 5) == 0.0, round(c, 5)

