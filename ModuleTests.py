#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,W0212,R0904,W0511,W0611
# C0103 : Invalid name "%s" (should match %s)
# W0212 : Access to a protected member %s of a client class
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0611 : Unused import

"""Quaternions test code

This file performs unit tests for:

Vector (variable-length) 
Matrix (variable-dimension)
Quaternion
"""

import unittest

from Vector import Vector, VectorTest
from Matrix import Matrix, MatrixTest
from MathUtil import MathUtil, MathUtilTest
from Quaternion import Quaternion, QuaternionTest
from CoordinateSys import CoordinateSys, CoordinateSysTest
from TriangleGroup import TriangleGroup, TriangleGroupTest

########################################################################

def main():

    """Main routine for Quaternions, intended to be run if the 
    module is executed on its own."""

    runAllUnitTests()
    #runUnitTestsFromCase(ModelTest)

########################################################################
# Unit Test Executive Logic
def runAllUnitTests():

    'Run all unit tests.'

    print "Running all unit tests:"
    #unittest.main()
    testRunner = unittest.TextTestRunner()
    testCases = [VectorTest, 
                 MatrixTest, 
                 QuaternionTest, 
                 CoordinateSysTest,
                 MathUtilTest,
                 TriangleGroupTest]
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(tc)
        for tc in testCases ]
    suite = suites[0]
    if suite is not None:
        suite.addTests(suites[1:])
        testRunner.run(suite)
    

def runUnitTestsFromCase(caseClass): # pragma: no cover
    
    """Run only the unit tests from the specified class, e.g.
    runUnitTestsFromCase(QuaternionTest)"""

    testRunner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(caseClass)
    if suite != None:
        print "Running test suite: " + caseClass.__name__
        testRunner.run(suite)

def runVectorTests(): # pragma: no cover
    'run vector tests only.'
    runUnitTestsFromCase(VectorTest)

def runMatrixTests(): # pragma: no cover
    'run matrix tests only.'
    runUnitTestsFromCase(MatrixTest)

def runQuaternionTests(): # pragma: no cover
    'run quaternion tests only.'
    runUnitTestsFromCase(QuaternionTest)

########################################################################
# Main Logic
if __name__ == '__main__':
    main()

