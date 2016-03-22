# coding: utf-8

from abstract_operations import AbstractMeshOperations
from mesh_loader import ObjLoader, OffLoader

__author__ = "Michał Ciołczyk, Michał Janczykowski"


class HalfedgeMeshOperations(AbstractMeshOperations):
    """
    Provides basic operations using half-edge as underlying data structure.
    """

    def __init__(self, filename):
        super(HalfedgeMeshOperations, self).__init__(filename)
        if self.filename.endswith('.obj'):
            self.polyhedron = ObjLoader(self.filename).to_polyhedron()
        elif self.filename.endswith('.off'):
            self.polyhedron = OffLoader(self.filename).to_polyhedron()
        else:
            raise AttributeError("Unknown file format")
        self.vertices = self._create_vertices_map()
        self.facets = self._create_facets_map()

    def _create_vertices_map(self):
        vertices = dict()
        i = 1
        for v in self.polyhedron.vertices():
            vertices[i] = v
            i += 1
        return vertices

    def _create_facets_map(self):
        facets = dict()
        i = 1
        for f in self.polyhedron.facets():
            facets[i] = f
            i += 1
        return facets

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

    def find_face_neighbors(self, face_id):
        facet = self.facets[face_id]
        both_levels_neighbours = set()  # actually this set will contain the analysed facet as well

        def find_single_face_neighbors(facet):
            circulator = facet.facet_begin()  # type: Halfedge_around_facet_circulator
            for i in xrange(facet.facet_degree()):
                he = circulator.next()
                he_opp = he.opposite()
                if not he_opp.is_border():
                    yield he.opposite().facet()

        first_level_neighbours = set(find_single_face_neighbors(facet))
        both_levels_neighbours.update(first_level_neighbours)

        for facet_nbr in first_level_neighbours:
            both_levels_neighbours.update(find_single_face_neighbors(facet_nbr))

        both_levels_neighbours.remove(facet)
        return both_levels_neighbours

    def flip_faces(self, face1_id, face2_id):
        pass

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]


def print_triangle_vertices(facet):
    circulator = facet.facet_begin()  # type: Halfedge_around_facet_circulator
    for i in xrange(3):
        he = circulator.next()
        print he.vertex().point(), '  \t',
    print


if __name__ == "__main__":
    operations = HalfedgeMeshOperations('data/test1.obj')
    vertex = operations.get_vertex(3)
    print('chosen vertex:')
    print(vertex.point())
    print('\nneighbours:')
    for v in operations.find_vertex_neighbors(3):
        print v.point()

    print('\nfacets:')
    for f in operations.find_vertex_faces(3):
        print_triangle_vertices(f)  # TODO do sth to be able to set IDs!

    print('\nmesh has border:')
    print operations.has_border()

    print('\nface neighbours:')  # FIXME segfault?
    for f in operations.find_face_neighbors(3):
        print_triangle_vertices(f)

