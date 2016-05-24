# coding: utf-8
from __future__ import print_function, generators

from functools import reduce
from math import fsum

import numpy as np
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_around_facet_circulator
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_around_vertex_circulator
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_handle
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Vertex_handle
from numpy.linalg import pinv, norm

from bucket import Bucket

__author__ = "Michał Ciołczyk, Michał Janczykowski"


def dummy_representative(bucket):
    """
    Dummy representative function.

    :param bucket: bucket to calculate representative from.
    :type bucket: Bucket
    :return: bucket's representative vertex coordinates
    :rtype: tuple(float, float, float)
    """
    return bucket.coordinates


def mean_representative(bucket):
    """
    Mean representative function.

    :param bucket: bucket to calculate representative from.
    :type bucket: Bucket
    :return: bucket's representative vertex coordinates
    :rtype: tuple(float, float, float)
    """
    n = len(bucket.original_vertices)
    if 0 == n:
        return bucket.coordinates
    xs = []
    ys = []
    zs = []
    for vertex in bucket.original_vertices:  # type: Polyhedron_3_Vertex_handle
        vertex = [float(x) for x in str(vertex.point()).split()]
        xs.append(vertex[0])
        ys.append(vertex[1])
        zs.append(vertex[2])
    return tuple([np.average(xs), np.average(ys), np.average(zs)])


def median_representative(bucket):
    """
    Mean representative function.

    :param bucket: bucket to calculate representative from.
    :type bucket: Bucket
    :return: bucket's representative vertex coordinates
    :rtype: tuple(float, float, float)
    """
    n = len(bucket.original_vertices)
    if 0 == n:
        return bucket.coordinates
    xs = []
    ys = []
    zs = []
    points = []
    for vertex in bucket.original_vertices:  # type: Polyhedron_3_Vertex_handle
        vertex = [float(x) for x in str(vertex.point()).split()]
        points.append(tuple([vertex[0], vertex[1], vertex[2]]))
        xs.append(vertex[0])
        ys.append(vertex[1])
        zs.append(vertex[2])
    mean = tuple([np.median(xs), np.median(ys), np.median(zs)])
    dist_sqr = lambda v1, v2: fsum([(v1[0] - v2[0]) ** 2, (v1[1] - v2[1]) ** 2, (v1[2] - v2[2]) ** 2])
    return reduce(lambda acc, v: acc if dist_sqr(acc, mean) < dist_sqr(v, mean) else v, points)


def quadric_errors_representative(bucket):
    """
    Quadric errors representative function.

    :param bucket: bucket to calculate representative from.
    :type bucket: Bucket
    :return: bucket's representative vertex coordinates
    :rtype: tuple(float, float, float)
    """
    A = np.zeros((3, 3))
    b = np.zeros((3, 1))
    faces_set = set()
    faces = []
    for vertex in bucket.original_vertices:  # type: Polyhedron_3_Vertex_handle
        circulator = vertex.vertex_begin()  # type: Polyhedron_3_Halfedge_around_vertex_circulator
        for i in range(vertex.vertex_degree()):
            he = circulator.next()  # type: Polyhedron_3_Halfedge_handle
            if he.is_border():
                continue

            f = he.facet()
            facet_circulator = f.facet_begin()  # type: Polyhedron_3_Halfedge_around_facet_circulator
            vertices = []
            for j in range(3):
                facet_he = facet_circulator.next()  # type: Polyhedron_3_Halfedge_handle
                vertices.append(tuple([float(x) for x in str(facet_he.vertex().point()).split()]))

            triangle_already_added = False
            n = len(vertices)
            for permutation in [[vertices[i - j] for i in range(n)] for j in range(n)]:
                if tuple(permutation) in faces_set:
                    triangle_already_added = True
                    break
                faces_set.add(tuple(permutation))
            if triangle_already_added:
                continue

            face = []
            for v in vertices:
                face.append(v)
            faces.append(face)
    for face in faces:
        p1 = np.array(face[0])
        p2 = np.array(face[1])
        p3 = np.array(face[2])
        normal = np.reshape(np.cross((p2 - p1), (p3 - p1)), (3, 1))
        normal_norm = norm(normal)
        normal /= normal_norm
        normal_t = normal.transpose()
        dist = np.dot(normal_t, p1)
        A += np.dot(normal, normal_t)
        b += dist * normal
    pinv_A = pinv(A)
    representative = np.dot(pinv_A, b)
    return tuple([representative[0][0], representative[1][0], representative[2][0]])
