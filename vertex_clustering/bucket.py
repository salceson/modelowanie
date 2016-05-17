# coding: utf-8
import numpy as np

__author__ = "Michał Ciołczyk, Michał Janczykowski"


def _round_point_no_nearest(point, epsilon):
    """
    :param point: list of coordinates
    """
    return [round(x / epsilon) * epsilon for x in point]


def get_bucket_for_vertex(vertex, epsilon):
    """
    :type vertex Polyhedron_3_Vertex_handle
    :return:
    """
    return tuple(_round_point_no_nearest([float(x) for x in str(vertex.point()).split()], epsilon))


class Bucket(object):
    def __init__(self, coordinates, representative_function, epsilon):
        self.coordinates = coordinates
        self.representative_function = representative_function
        self.original_vertices = []
        self._representative = None
        self.epsilon = epsilon

    def append(self, vertex):
        self.original_vertices.append(vertex)

    @property
    def representative(self):
        if not self._representative:
            self._representative = self.representative_function(self)
            if tuple(_round_point_no_nearest(self._representative, self.epsilon)) != self.coordinates:
                representative_np = np.array(list(self._representative))
                coordinates_np = np.array(list(self.coordinates))
                norm = np.linalg.norm(representative_np - coordinates_np)
                if norm > 10 * self.epsilon:
                    self._representative = self.coordinates
        return self._representative
