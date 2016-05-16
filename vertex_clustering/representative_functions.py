# coding: utf-8
import numpy as np
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Vertex_handle

from bucket import Bucket

__author__ = "Michał Ciołczyk, Michał Janczykowski"


def dummy_representative(bucket):
    """
    Dummy representative function.
    :param bucket: bucket to calculate representative from.
    :type bucket Bucket
    :return: bucket's representative vertex coordinates
    :rtype tuple(float, float, float)
    """
    return bucket.coordinates


def mean_representative(bucket):
    """
    Mean representative function.
    :param bucket: bucket to calculate representative from.
    :type bucket Bucket
    :return: bucket's representative vertex coordinates
    :rtype tuple(float, float, float)
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
    :type bucket Bucket
    :return: bucket's representative vertex coordinates
    :rtype tuple(float, float, float)
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
    return tuple([np.median(xs), np.median(ys), np.median(zs)])
