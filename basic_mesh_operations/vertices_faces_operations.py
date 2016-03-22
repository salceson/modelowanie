# coding: utf-8

from abstract_operations import AbstractMeshOperations
from mesh_loader import OffLoader, ObjLoader


class VerticesFacesOperations(AbstractMeshOperations):
    def __init__(self, filename):
        super(VerticesFacesOperations, self).__init__(filename)
        if self.filename.endswith('.obj'):
            self.vertices, self.faces = ObjLoader(self.filename).to_vertices_and_faces()
        elif self.filename.endswith('.off'):
            self.vertices, self.faces = OffLoader(self.filename).to_vertices_and_faces()
        else:
            raise AttributeError("Unknown file format")

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]

    def find_vertex_faces(self, vertex_id):
        i = 0
        found_faces = []
        for face in self.faces:
            if vertex_id in face:
                found_faces.append(i)
            i += 1
        return found_faces

    def flip_faces(self, face1_id, face2_id):
        face1 = self.faces[face1_id]
        face1_set = set(face1)
        face2 = self.faces[face2_id]
        face2_set = set(face2)
        shared_edge = face1_set & face2_set
        print face1, face2
        print face1_set, face2_set
        print shared_edge

    def find_face_neighbors(self, face_id):
        pass

    def find_vertex_neighbors(self, vertex_id):
        pass

    def has_border(self):
        pass

if __name__ == '__main__':
    operations = VerticesFacesOperations('data/test1.obj')
    print operations.find_vertex_faces(0)
    operations.flip_faces(0, 1)
