# coding: utf-8
import itertools

from abstract_operations import AbstractMeshOperations
from mesh_loader import OffLoader, ObjLoader

__author__ = "Michał Ciołczyk"


class VerticesFacesOperations(AbstractMeshOperations):
    """
    Provides basic operations using vertices list and faces list as underlying data structure.
    """

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

    def get_face(self, face_id):
        return self.faces[face_id]

    def find_vertex_faces(self, vertex_id):
        i = 1
        found_faces = []
        for face in self.faces[1:]:
            if vertex_id in face:
                found_faces.append(i)
            i += 1
        return found_faces

    def flip_faces(self, face1_id, face2_id):
        face1 = self.faces[face1_id]
        face1_set = set(face1)
        face2 = self.faces[face2_id]
        face2_set = set(face2)
        shared_vertices = face1_set & face2_set
        remaining_vertices = (face1_set | face2_set).difference(shared_vertices)
        new_faces = []
        for sv in shared_vertices:
            new_faces.append(list({sv} | remaining_vertices))
        self.faces[face1_id] = new_faces[0]
        self.faces[face2_id] = new_faces[1]
        return new_faces

    def find_face_neighbors(self, face_id):
        first_level_neighbours = self._find_face_direct_neighbors(face_id)
        first_level_neighbours.remove(face_id)
        both_levels_neighbours = set()  # actually this set will contain the analysed vertex as well
        both_levels_neighbours.update(first_level_neighbours)

        for vn in first_level_neighbours:
            both_levels_neighbours.update(self._find_face_direct_neighbors(vn))

        both_levels_neighbours.remove(face_id)
        return list(map(lambda f_id: self.faces[f_id], both_levels_neighbours))

    def _find_face_direct_neighbors(self, f_id):
        face = self.faces[f_id]
        faces = set()
        combinations = list(itertools.combinations(face, 2))
        for vertices_pair in combinations:
            i = 1
            for f in self.faces[1:]:
                if vertices_pair[0] in f and vertices_pair[1] in f:
                    faces.add(i)
                i += 1
        return faces

    def find_vertex_neighbors(self, vertex_id):
        def find_vertex_direct_neighbors(v_id):
            faces = self.find_vertex_faces(v_id)
            neighbors = set()
            for face in faces[1:]:
                for v in self.faces[face]:
                    neighbors.add(v)
            return neighbors

        first_level_neighbours = find_vertex_direct_neighbors(vertex_id)
        first_level_neighbours.remove(vertex_id)
        both_levels_neighbours = set()  # actually this set will contain the analysed vertex as well
        both_levels_neighbours.update(first_level_neighbours)

        for vn in first_level_neighbours:
            both_levels_neighbours.update(find_vertex_direct_neighbors(vn))

        both_levels_neighbours.remove(vertex_id)
        return list(map(lambda v_id: self.vertices[v_id], both_levels_neighbours))

    def has_border(self):
        i = 1
        for f in self.faces[1:]:
            direct_neighbours = self._find_face_direct_neighbors(i)
            direct_neighbours.remove(i)
            if len(direct_neighbours) < len(f):
                return True
            i += 1
        return False


if __name__ == '__main__':
    operations = VerticesFacesOperations('data/test1.off')
    vertex = operations.get_vertex(3)
    print('chosen vertex:')
    print(vertex)
    print('\nneighbours:')
    for neighbor in operations.find_vertex_neighbors(3):
        print neighbor
    print('\nfaces:')
    print(operations.find_vertex_faces(3))
    print('\nhas border:')
    print(operations.has_border())
    print('\n\nchosen face:')
    face = operations.get_face(3)
    print(face)
    print('\nneighbours:')
    print(operations.find_face_neighbors(3))
    print('\n\nFlipping faces 2 and 3:')
    print([operations.get_face(2), operations.get_face(3)])
    print(operations.flip_faces(2, 3))
