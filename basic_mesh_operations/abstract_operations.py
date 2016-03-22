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
        Returns vertex neighbors (two layers).
        :param vertex_id: vertex id to get neighbors
        :return list of vertices that are neighbors to vertex vertex_id (vertex is a list of coordinates)
        :rtype list
        """
        raise NotImplementedError()

    def find_vertex_faces(self, vertex_id):
        """
        Returns faces which vertex vertex_id belongs to.
        :param vertex_id: vertex id to get faces it belongs to
        :return list of faces that the vertex vertex_id belongs to (face is a list of vertices ids)
        :rtype list
        """
        raise NotImplementedError()

    def find_face_neighbors(self, face_id):
        """
        Returns face neighbors (two layers).
        :param face_id: face id to get neighbors
        :return list of faces that are neighbors to face face_id (face is a list of vertices ids)
        :rtype list
        """
        raise NotImplementedError()

    def flip_faces(self, face1_id, face2_id):
        """
        Flips the diagonal between the two faces. Returns the new facets.
        :param face1_id: first face id to flip
        :param face2_id: second face id to flip
        :return New faces (after flip; face is a list of vertices ids)
        :rtype list, list
        """
        raise NotImplementedError()

    def has_border(self):
        """
        Checks if mesh has border.
        :return True if mesh has border, False otherwise
        :rtype bool
        """
        raise NotImplementedError()

    def get_vertex(self, vertex_id):
        """
        Returns vertex which index is vertex_id. Indices starts from 1.
        :param vertex_id: vertex id to get vertex
        :return list of coordinates
        :rtype list
        """
        raise NotImplementedError()

    def get_face(self, face_id):
        """
        Returns facet which index is face_id. Indices starts from 1.
        :param face_id: face id to get facet
        :return list of vertices ids
        :rtype list
        """
        raise NotImplementedError()
