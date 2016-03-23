# coding=utf-8
from time import time

from halfedge_operations import HalfedgeMeshOperations
from vertices_faces_operations import VerticesFacesOperations

__author__ = "Michał Ciołczyk"


def _test_operations(he_ops, ve_ops):
    """
    :type he_ops HalfedgeMeshOperations
    :type ve_ops VerticesFacesOperations
    """
    # Find vertex neighbors
    he_fvn_start = time()
    he_ops.find_vertex_neighbors(50)
    he_fvn_stop = time()
    ve_fvn_start = time()
    ve_ops.find_vertex_neighbors(50)
    ve_fvn_stop = time()
    print "\tFind vertex neighbors:"
    print "\t\tHalfedge: ", he_fvn_stop - he_fvn_start, "seconds."
    print "\t\tVertices/faces list: ", ve_fvn_stop - ve_fvn_start, "seconds."
    # Find vertex's faces
    he_fvf_start = time()
    he_ops.find_vertex_faces(50)
    he_fvf_stop = time()
    ve_fvf_start = time()
    ve_ops.find_vertex_faces(50)
    ve_fvf_stop = time()
    print "\tFind vertex faces:"
    print "\t\tHalfedge: ", he_fvf_stop - he_fvf_start, "seconds."
    print "\t\tVertices/faces list: ", ve_fvf_stop - ve_fvf_start, "seconds."
    # Find face neighbors
    he_ffn_start = time()
    he_ops.find_face_neighbors(150)
    he_ffn_stop = time()
    ve_ffn_start = time()
    ve_ops.find_face_neighbors(150)
    ve_ffn_stop = time()
    print "\tFind face neighbors:"
    print "\t\tHalfedge: ", he_ffn_stop - he_ffn_start, "seconds."
    print "\t\tVertices/faces list: ", ve_ffn_stop - ve_ffn_start, "seconds."
    # Flip edges
    he_fe_start = time()
    he_ops.flip_faces(150, 151)
    he_fe_stop = time()
    ve_fe_start = time()
    he_ops.flip_faces(150, 151)
    ve_fe_stop = time()
    print "\tFlip edge:"
    print "\t\tHalfedge: ", he_fe_stop - he_fe_start, "seconds."
    print "\t\tVertices/faces list: ", ve_fe_stop - ve_fe_start, "seconds."
    # Has border
    he_hb_start = time()
    has_border = he_ops.has_border()
    he_hb_stop = time()
    ve_hb_start = time()
    he_ops.has_border()
    ve_hb_stop = time()
    print "\tHas border: %s" % has_border
    print "\t\tHalfedge: ", he_hb_stop - he_hb_start, "seconds."
    print "\t\tVertices/faces list: ", ve_hb_stop - ve_hb_start, "seconds."


if __name__ == "__main__":
    tests = ['Armadillo', 'HappyBuddha', 'Bunny']
    for test in tests:
        print test
        he_ops = HalfedgeMeshOperations('data/%s.off' % test)
        ve_ops = VerticesFacesOperations('data/%s.off' % test)
        _test_operations(he_ops, ve_ops)
        del he_ops
        del ve_ops
