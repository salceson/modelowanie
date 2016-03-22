# coding: utf-8

__author__ = "Michał Ciołczyk"


class AbstractMeshOperations(object):
    def __init__(self, filename):
        self.filename = filename

    def find_vertex_neighbors(self, vertex_id):
        raise NotImplementedError()

    def find_vertex_faces(self, vertex_id):
        raise NotImplementedError()

    def find_face_neighbors(self, vertex_id):
        raise NotImplementedError()

    def flip_faces(self, face1_id, face2_id):
        raise NotImplementedError()

    def has_border(self):
        raise NotImplementedError()

    def get_vertex(self, vertex_id):
        raise NotImplementedError()
