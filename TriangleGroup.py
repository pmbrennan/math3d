#!/usr/bin/python

# Disable some pylint messages
# pylint: disable=C0103,R0201,R0904,W0511
# C0103 : Invalid name "%s" (should match %s)
# R0201 : Method could be a function
# R0904 : Too many public methods
# W0511 : TODO/FIXME/XXX
# W0212 : Access to a protected member %s of a client class

"""
A simple representation of a set of triangles.
"""

import math
import unittest
from Vector import Vector

########################################################################
class TriangleGroup:

    """TriangleGroup : a representation of a set of triangles and their
    associated vertices and edges."""

    # TODO: Add write to STL
    # TODO: Pyglet display

    def __init__(self):
        # It would be nice to make this a set but I need indices from this.
        self.mVertices = [ ] # list of Vectors
        self.mEdges = [ ] # list of (i,j) tuples of vertex indices
        self.mTriangles = [ ]

    def _addVertex(self, vertex):
        """Add a vertex to the list of vertices. If the vertex has 
        already been added it will be ignored. Return the index
        of the vertex in the list."""
        for i in range(len(self.mVertices)):
            if self.mVertices[i] == vertex:
                return i
        i = len(self.mVertices)
        self.mVertices.append(vertex)
        return i

    def _addEdge(self, edge):
        """Add an edge to the list of edges. An edge is represented as
        a 2-tuple specifying two vertices. (A,B) and (B,A) are considered
        to be equivalent."""
        (i1, i2) = edge
        if i1 == i2:
            raise ValueError('An edge must refer to two different vertices!')
        for i in range(len(self.mEdges)):
            (j1, j2) = self.mEdges[i]
            if i1 == j1 and i2 == j2:
                return i
            elif i1 == j2 and i2 == j1:
                return i
        i = len(self.mEdges)
        self.mEdges.append(edge)

    def _addTriangle(self, triangle):
        """Add a triangle to the list of triangles. A triangle is represented
        as a 3-tuple specifying three vertices, in counteclockwise order
        as viewed from the direction pointed to by the triangle's surface
        normal. Therefore (A,B,C) is not considered to be equivalent to
        (A,C,B), even though they contain the same vertices."""
        (a1, b1, c1) = triangle
        if a1 == b1 or a1 == c1 or b1 == c1:
            raise ValueError(
                'A triangle must refer to three different vertices!')
        for i in range(len(self.mTriangles)):
            (a2, b2, c2) = self.mTriangles[i]
            if a1 == a2 and b1 == b2 and c1 == c2:
                return i
            elif a1 == b2 and b1 == c2 and c1 == a2:
                return i
            elif a1 == c2 and b1 == a2 and c1 == b2:
                return i
        i = len(self.mTriangles)
        self.mTriangles.append(triangle)

    def addTriangle(self, vertex1, vertex2, vertex3):
        """Add a triangle to the group. The vertices should be specified in
        counter-clockwise order as viewed from the positive direction of 
        the triangle's surface normal."""
        index1 = self._addVertex(vertex1)
        index2 = self._addVertex(vertex2)
        index3 = self._addVertex(vertex3)

        self._addEdge((index1, index2))
        self._addEdge((index2, index3))
        self._addEdge((index3, index1))

        self._addTriangle((index1, index2, index3))

    def nVertices(self):
        """Return the number of vertices."""
        return len(self.mVertices)

    def nEdges(self):
        """Return the number of edges."""
        return len(self.mEdges)

    def nFaces(self):
        """Return the number of faces."""
        return len(self.mTriangles)

    def edgeLength(self, i):
        """Return the length of edge i."""
        (m, n) = self.mEdges[i]
        return (self.mVertices[n] - self.mVertices[m]).norm()

    def clone(self):
        """Make a copy of this object."""
        rv = TriangleGroup()
        rv.mEdges = self.mEdges[:]
        rv.mVertices = self.mVertices[:]
        rv.mTriangles = self.mTriangles[:]
        return rv

    def sphericalSubdivide(self):
        """Given a polygon group which is assumed to be built only from
        vertices which lie on the surface of a unit sphere, subdivide 
        each triangle into 4 triangles. Assume the triangle has
        points A, B, and C. Cut each of the lines AB, BC, and CA
        in half, generating points D, E, and F, respectively. Each
        point will then be normalized so that it, too, is on the surface
        of the unit sphere. Then replace triangle ABC with triangles:
        ADF, DBE, ECF, and DEF."""

        # TODO: This isn't working right. All edges from icosahedron
        # should be the same length, but they're not, why??

        self.mEdges = [ ] # remove the existing edges.
        triangles = self.mTriangles[:]
        self.mTriangles = [ ] # remove the existing triangles
        vertices = self.mVertices[:]
        
        for triangle in triangles:
            (A, B, C) = [vertices[idx] for idx in triangle]
            D = ((A + B).mults(0.5)).normalize()
            E = ((B + C).mults(0.5)).normalize()
            F = ((C + A).mults(0.5)).normalize()
            self.addTriangle(A, D, F)
            self.addTriangle(D, B, E)
            self.addTriangle(E, C, F)
            self.addTriangle(D, E, F)

    def maxSphericalDeviation(self):
        """Given a polygon group which is assumed to be built only from
        vertices which lie on the surface of a unit sphere, determine
        the maximum amount by which a point on the surface may differ from
        a point on the polygon mesh. This value is a proxy for how well
        the polygon mesh approximates a sphere."""
        maxDifference = 0.0

        for triangle in self.mTriangles:
            (A, B, C) = [self.mVertices[idx] for idx in triangle]
            
            # Determine the diameter of the circumcircle, the circle
            # which includes triangle ABC (points A, B, and C are all
            # on the circle):
            LAC = (A - C).norm() # length of A-C
            BA = (A - B).normalize()
            BC = (C - B).normalize()
            ABC = math.acos(BA.dot(BC)) # Angle opposite
            diameter = LAC / math.sin(ABC)

            # Determine the angle with includes that circle, from the 
            # origin
            angle = math.asin(diameter * 0.5)
            deviation = 1.0 - math.cos(angle)

            if (deviation > maxDifference):
                maxDifference = deviation

        return maxDifference

    def toStl(self, name='TriangleGroup'):
        """Write the triangle group out to STL."""
        out = 'solid %s\n' % name
        for triangle in self.mTriangles:
            # Compute the surface normal
            (A, B, C) = [self.mVertices[i] for i in triangle]
            AB = B - A
            AC = C - A
            surfaceNormal = AB.cross(AC).normalize()
            out += 'facet normal {0:.6e} {1:.6e} {2:.6e}\n'.format(
                surfaceNormal[0], surfaceNormal[1], surfaceNormal[2])
            out += 'outer loop\n'
            out += A.toStl() + '\n'
            out += B.toStl() + '\n'
            out += C.toStl() + '\n'
            out += 'endloop\nendfacet\n'
        out += 'endsolid %s' % name
        return out

    @staticmethod
    def tetrahedron():
        """Return a tetrahedron, a regular solid comprised of four triangular
        faces such that each triangle is the same size and are equilateral.
        The vertices are inscribed in a sphere of radius 1.

        DETAILS OF CONSTRUCTION:
        The tetrahedron has 4 points. Call these A, B, C, and D. Furthermore,
        Let O be the origin, i.e. [0,0,0].

        Each of these points can be described by a parametric function
        of theta and alpha, thus:
        Point = f(theta, alpha) = 
        [ x = sin(theta) * cos(alpha), 
          y = sin(theta) * sin(alpha),
          z = cos(theta) ]
        theta is the angle from the Z-axis to the vector representing 
        the vertex (i.e. OP), and alpha is the angle from the X-axis
        to the projection of OP on to the XY plane. Alpha is 0, 120, 
        or 240 degrees for points B, C, and D respectively.

        Point | alpha    | theta 
        ------+----------+-------
          A   |   N/A    |   0
          B   |   0 deg  | theta
          C   | 120 deg  | theta
          D   | 240 deg  | theta

        So the question to be resolved is, what is the correct value for
        theta? And we can derive that by observing that |AB| == |BD|, 
        i.e. the line from A to B must be the same length as the line from
        B to D. We use the law of cosines to write the length and we 
        will see that:
        
        2 * sin^2(theta) * (1 - cos(120deg)) = 2 * (1 - cos(theta))

        which is then readily solved for theta, yielding
        
        cos(theta) = -1/3
        theta = 109.4712206 degrees = 1.9106332362490186 radians
        """
        theta = math.acos(-1.0/3.0)
        alpha0 = 0.0
        alpha1 = math.pi * 2.0 / 3.0
        alpha2 = 2 * alpha1

        A = Vector( 0.0, 0.0, 1.0 )
        B = Vector( math.sin(theta) * math.cos(alpha0),
                    math.sin(theta) * math.sin(alpha0),
                    math.cos(theta) )
        C = Vector( math.sin(theta) * math.cos(alpha1),
                    math.sin(theta) * math.sin(alpha1),
                    math.cos(theta) )
        D = Vector( math.sin(theta) * math.cos(alpha2),
                    math.sin(theta) * math.sin(alpha2),
                    math.cos(theta) )

        g = TriangleGroup()
        g.addTriangle(A, B, D)
        g.addTriangle(A, D, C)
        g.addTriangle(A, C, B)
        g.addTriangle(B, C, D)

        return g
    
    @staticmethod
    def icosahedron():
        """Return an icosahedron, a regular solid comprised of 20 triangular
        faces of the same size, all equilateral. The vertices are inscribed
        in a sphere of radius 1."""

        g = TriangleGroup()

        vertex_indices = [ (0, 4, 1), (0, 9, 4), (9, 5, 4), (4, 5, 8), 
                           (4, 8, 1), (8, 10, 1), (8, 3, 10), (5, 3, 8), 
                           (5, 2, 3), (2, 7, 3), (7, 10, 3), (7, 6, 10), 
                           (7, 11, 6), (11, 0, 6), (0, 1, 6), (6, 1, 10), 
                           (9, 0, 11), (9, 11, 2), (9, 2, 5), (7, 2, 11) ]

        X = 0.525731112119133606
        Z = 0.850650808352039932

        points = [ ]

        for i in range(12):
            if i <= 3:
                if i & 1:
                    px = X
                else:
                    px = -X
                py = 0.0
                if i & 2:
                    pz = -Z
                else:
                    pz = Z
            elif i <= 7:
                px = 0.0
                if i & 2:
                    py = -Z
                else:
                    py = Z
                if i & 1:
                    pz = -X
                else:
                    pz = X
            else:
                if i & 1:
                    px = -Z
                else:
                    px = Z

                if i & 2:
                    py = -X
                else:
                    py = X

                pz = 0.0

            points.append(Vector(px,py,pz))

        for i in range(20):
            (p1, p2, p3) = vertex_indices[i]
            g.addTriangle(points[p1], points[p2], points[p3])

        return g

########################################################################
# TriangleGroup Tests
class TriangleGroupTest(unittest.TestCase):
    """Unit tests for TriangleGroup class."""

    def testClone(self):
        """Test the clone function."""
        g1 = TriangleGroup.tetrahedron()
        g2 = g1.clone()
        assert(g2.nFaces() == 4)
        assert(g2.nVertices() == 4)
        assert(g2.nEdges() == 6)
        assert g2.mVertices[0] == [ 0.0, 0.0, 1.0 ]

    def testIcosahedron(self):
        """Test the icosahedron generation method."""
        g = TriangleGroup.icosahedron()

        # Test basic topological properties
        assert(g.nFaces() == 20)
        assert(g.nVertices() == 12)
        assert(g.nEdges() == 30)

    def testTetrahedron(self):
        """Test the tetrahedron generation method."""
        g = TriangleGroup.tetrahedron()

        # Test basic topological properties
        assert(g.nFaces() == 4)
        assert(g.nVertices() == 4)
        assert(g.nEdges() == 6)

        # Test the unit-ness of the vertices
        assert(g.mVertices[0].norm() == 1.0)
        assert(g.mVertices[1].norm() == 1.0)
        assert(g.mVertices[2].norm() == 1.0)
        assert(round(g.mVertices[3].norm(), 12) == 1.0)

        # Test the equivalence of the sides (to 12 places)
        LAB = round((g.mVertices[0] - g.mVertices[1]).norm(), 12)
        LBC = round((g.mVertices[1] - g.mVertices[2]).norm(), 12)
        LCD = round((g.mVertices[2] - g.mVertices[3]).norm(), 12)
        LDB = round((g.mVertices[3] - g.mVertices[1]).norm(), 12)
        LAC = round((g.mVertices[0] - g.mVertices[2]).norm(), 12)
        LAD = round((g.mVertices[0] - g.mVertices[3]).norm(), 12)

        assert LAB == LBC
        assert LAB == LCD
        assert LAB == LDB
        assert LAB == LAC
        assert LAB == LAD
        
        # Test the interior angles (to 12 places)
        AAB = round(g.mVertices[0].dot(g.mVertices[1]), 12)
        AAC = round(g.mVertices[0].dot(g.mVertices[2]), 12)
        AAD = round(g.mVertices[0].dot(g.mVertices[3]), 12)
        ABC = round(g.mVertices[1].dot(g.mVertices[2]), 12)
        ABD = round(g.mVertices[1].dot(g.mVertices[3]), 12)
        ACD = round(g.mVertices[2].dot(g.mVertices[3]), 12)

        assert AAB == AAC
        assert AAB == AAD
        assert AAB == ABC
        assert AAB == ABD
        assert AAB == ACD


        


