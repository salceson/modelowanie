# coding: utf-8

from abstract_operations import AbstractMeshOperations
from mesh_loader import OffLoader, ObjLoader


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
        shared_edge = face1_set & face2_set
        print face1, face2
        print face1_set, face2_set
        print shared_edge

    def find_face_neighbors(self, face_id):
        pass

    def find_vertex_neighbors(self, vertex_id):
        first_level_neighbours = self._find_vertex_direct_neighbors(vertex_id)
        first_level_neighbours.remove(vertex_id)
        both_levels_neighbours = set()  # actually this set will contain the analysed vertex as well
        both_levels_neighbours.update(first_level_neighbours)

        for vn in first_level_neighbours:
            both_levels_neighbours.update(self._find_vertex_direct_neighbors(vn))

        both_levels_neighbours.remove(vertex_id)
        return list(map(lambda v_id: self.vertices[v_id], both_levels_neighbours))

    def _find_vertex_direct_neighbors(self, vertex_id):
        faces = self.find_vertex_faces(vertex_id)
        neighbors = set()
        for face in faces[1:]:
            for vertex in self.faces[face]:
                neighbors.add(vertex)
        return neighbors

    def has_border(self):
        pass


if __name__ == '__main__':
    operations = VerticesFacesOperations('data/test1.off')
    vertex = operations.get_vertex(3)
    print('chosen vertex:')
    print(vertex)
    # operations.flip_faces(2, 3)
    print('\nneighbours:')
    for neighbor in operations.find_vertex_neighbors(3):
        print neighbor
    print('\nfaces:')
    print operations.find_vertex_faces(3)
