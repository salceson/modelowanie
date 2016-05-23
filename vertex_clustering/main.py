# coding: utf-8
from __future__ import print_function

import sys

from clustering import cluster
from mesh_loader import ObjLoader, OffLoader
from representative_functions import *

__author__ = "Michał Ciołczyk, Michał Janczykowski"

_functions = ["center", "mean", "median", "quadric"]
_functions_map = {
    "center": dummy_representative,
    "mean": mean_representative,
    "median": median_representative,
    "quadric": quadric_errors_representative
}


def cluster_mesh(mesh_filename, epsilon, function, output_filename):
    """
    Performs vertex clustering on mesh.

    :param mesh_filename: input mesh filename
    :type mesh_filename: string
    :param epsilon: epsilon used in algorithm (see docs)
    :type epsilon: float
    :param function: representative method used in algorithm (see docs);
     must be one of: ["center", "mean", "median", "quadric"]
    :type function: string
    :param output_filename: output mesh filename
    :type output_filename: string
    """
    if function not in _functions:
        raise ValueError("Function must be in: %s." % str(_functions))
    epsilon = float(epsilon)
    if not mesh_filename.endswith('.obj') and not mesh_filename.endswith('.off'):
        raise ValueError("Supporting only .obj and .off files!")
    method = _functions_map[function]
    if mesh_filename.endswith('.obj'):
        mesh_loader = ObjLoader(mesh_filename)
    else:
        mesh_loader = OffLoader(mesh_filename)
    mesh = mesh_loader.to_polyhedron()
    cluster(mesh, epsilon, method, output_filename)


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 5:
        print("Usage: python %s <mesh_filename> <epsilon> <method> <output_filename>" % argv[0])
        print("\tWhere method is one of: %s" % str(_functions))
        exit(1)
    cluster_mesh(argv[1], argv[2], argv[3], argv[4])
