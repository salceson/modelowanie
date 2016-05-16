# coding: utf-8
from __future__ import print_function, generators

from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Facet_handle
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_around_facet_circulator
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_handle

from bucket import get_bucket_for_vertex
from mesh_loader import *
from representative_functions import *

__author__ = "Michał Ciołczyk, Michał Janczykowski"


def cluster(mesh, epsilon, representative_method, filename):
    """
    :type mesh Polyhedron_3
    """
    buckets = {}

    for v in mesh.vertices():
        b = get_bucket_for_vertex(v, epsilon)
        if b not in buckets:
            bucket = Bucket(b, representative_method)
            buckets[b] = bucket
        buckets[b].append(v)

    # build result mesh
    result_vertices = []
    result_faces = []

    bucket_coords_to_ids = {}
    for i, bucket in enumerate(buckets.values()):
        coords = bucket.coordinates
        representative = bucket.representative
        bucket_coords_to_ids[coords] = i
        result_vertices.append(representative)

    faces_set = set()
    for f in mesh.facets():  # type: Polyhedron_3_Facet_handle
        circulator = f.facet_begin()  # type: Polyhedron_3_Halfedge_around_facet_circulator
        edge_list = []
        for i in range(f.facet_degree()):
            he = circulator.next()  # type: Polyhedron_3_Halfedge_handle
            b = he.vertex()
            b = get_bucket_for_vertex(b, epsilon)
            edge_list.append(b)
        edge_set = set(edge_list)
        if len(edge_set) != 3:
            continue
        if len(edge_list) != 3:
            continue

        n = len(edge_list)
        triangle_already_added = False
        for permutation in [[edge_list[i - j] for i in range(n)] for j in range(n)]:
            if tuple(permutation) in faces_set:
                triangle_already_added = True
                break
            faces_set.add(tuple(permutation))

        if triangle_already_added:
            continue

        face = []
        for b in edge_list:
            v = bucket_coords_to_ids[b]
            face.append(v)
        result_faces.append(face)

    with open(filename, 'w') as f:
        print('OFF', file=f)
        print('%d %d 0' % (len(result_vertices), len(result_faces)), file=f)
        print('', file=f)
        for v in result_vertices:
            print('%.10f %.10f %.10f' % (v[0], v[1], v[2]), file=f)
        print('', file=f)
        for face in result_faces:
            print('3 %d %d %d' % (face[0], face[1], face[2]), file=f)
        print('', file=f)


if __name__ == "__main__":
    mesh = OffLoader('data/Bunny.off').to_polyhedron()
    cluster(mesh, 0.01, median_representative, 'out.off')
