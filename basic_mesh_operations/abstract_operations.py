# coding: utf-8

__author__ = "Michał Ciołczyk"


class AbstractMeshOperations(object):
    """
    Enables users to do basic operations on meshes.
    """

    def __init__(self, filename):
        """
        Loads mesh from filename and creates operations object.

        Current supported formats:

        * OBJ

        * OFF
        :param filename: file to read mesh from
        """
        self.filename = filename

    def find_vertex_neighbors(self, vertex_id):
        """
        Returns vertex which index is vertex_id. Indices starts from 1.
        :param vertex_id: vertex id to get vertex
        """
        raise NotImplementedError()

    def find_vertex_faces(self, vertex_id):
        raise NotImplementedError()

    def find_face_neighbors(self, face_id):
        raise NotImplementedError()

    def flip_faces(self, face1_id, face2_id):
        raise NotImplementedError()

    def has_border(self):
        raise NotImplementedError()

    def get_vertex(self, vertex_id):
        raise NotImplementedError()
