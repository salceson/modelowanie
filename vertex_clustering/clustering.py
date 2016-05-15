# coding: utf-8

__author__ = "Michał Ciołczyk, Michał Janczykowski"

from collections import defaultdict
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3, Polyhedron_modifier, Polyhedron_3_Vertex_handle
from halfedge_operations import HalfedgeMeshOperations
from mesh_loader import ObjLoader, OffLoader


def round_point_no_nearest(point, epsilon):
    """
    :param point: list of coordinates
    """
    return [round(x/epsilon) * epsilon for x in point]


def get_bucket_for_vertex(vertex, epsilon):
    """
    :type vertex Polyhedron_3_Vertex_handle
    :return:
    """
    return tuple(round_point_no_nearest([float(x) for x in str(vertex.point()).split()], epsilon))


def cluster(mesh, epsilon, representative_method):
    """
    :type mesh Polyhedron_3
    """
    buckets = defaultdict(set)

    for v in mesh.vertices():
        b = get_bucket_for_vertex(v, epsilon)
        buckets[b].add(v)

    # find representatives
    buckets_representatives = dict()
    for b in buckets.keys():
        buckets_representatives[b] = representative_method(b, buckets[b])

    # build result mesh
    polyhedron_modifier = Polyhedron_modifier()
    polyhedron_modifier.begin_surface(len(self.vertices), len(self.faces))

    # TODO 1. add indexed bucket_representative vertices
    # TODO 2. for each face in mesh:
    #           a. map vertices to bucket_representatives,
    #           b. check if triangle is legal (all points are different)
    #           c. check if triangle hasn't been already created
    #           d. add triangle to polyhedron_modifier


    polyhedron = Polyhedron_3()
    polyhedron.delegate(polyhedron_modifier)
    return polyhedron


def default_representative(bucket, vertices):
    """
    :type bucket List of coordinates of bucket
    :type vertices List of Polyhedron_3_Vertex_handle
    :return List of coordinates
    """
    return bucket

if __name__ == "__main__":
    mesh = ObjLoader('data/test1.obj').to_polyhedron()
    result = cluster(mesh, 2.0, default_representative)
    print("done")
