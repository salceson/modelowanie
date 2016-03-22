# coding: utf-8

from CGAL.CGAL_Polyhedron_3 import Polyhedron_3, Polyhedron_3_Halfedge_iterator, Polyhedron_3_Vertex_handle, \
    Polyhedron_3_Halfedge_handle, Polyhedron_3_Halfedge_around_vertex_circulator, Polyhedron_3_Facet_handle

from abstract_operations import AbstractMeshOperations

__author__ = "Michał Ciołczyk, Michał Janczykowski"


class HalfedgeMeshOperations(AbstractMeshOperations):
    def __init__(self, filename):
        super(HalfedgeMeshOperations, self).__init__(filename)
        # TODO: Handle obj files
        self.polyhedron = Polyhedron_3(self.filename)
        self.vertices = self._create_vertices_map()

    def _create_vertices_map(self):
        vertices = dict()
        i = 1
        for v in self.polyhedron.vertices():
            vertices[i] = v
            i += 1
        return vertices

    def find_vertex_neighbors(self, vertex_id):
        vertex = self.vertices[vertex_id]
        first_level_neighbours = set(self._list_vertex_direct_neighbours(vertex))

        both_levels_neighbours = set()  # actually this set will contain the analysed vertex as well
        both_levels_neighbours.update(first_level_neighbours)

        for vn in first_level_neighbours:
            both_levels_neighbours.update(self._list_vertex_direct_neighbours(vn))

        both_levels_neighbours.remove(vertex)
        return both_levels_neighbours

    # noinspection PyMethodMayBeStatic
    def _list_vertex_direct_neighbours(self, vertex):
        circulator = vertex.vertex_begin()  # type: Halfedge_around_vertex_circulator
        for i in xrange(vertex.vertex_degree()):
            he = circulator.next()
            yield he.opposite().vertex()

    def find_vertex_faces(self, vertex_id):
        vertex = self.vertices[vertex_id]
        circulator = vertex.vertex_begin()
        for i in xrange(vertex.vertex_degree()):
            he = circulator.next()
            if not he.is_border():
                yield he.facet()

    def has_border(self):
        for he in self.polyhedron.halfedges():
            if he.is_border():
                return True
        return False

    def find_face_neighbors(self, vertex_id):
        pass

    def flip_faces(self, face1_id, face2_id):
        pass

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]


if __name__ == "__main__":
    operations = HalfedgeMeshOperations('in/test1.off')
    vertex = operations.get_vertex(3)
    print('chosen vertex:')
    print(vertex.point())
    print('\nneighbours:')
    for v in operations.find_vertex_neighbors(3):
        print v.point()

    print('\nfacets:')
    for f in operations.find_vertex_faces(3):
        print f.id()  # TODO do sth to be able to set IDs!

    print('\nmesh has border:')
    print operations.has_border()
