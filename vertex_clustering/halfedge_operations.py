# coding: utf-8

from abstract_operations import AbstractMeshOperations
from mesh_loader import ObjLoader, OffLoader
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3_Halfedge_around_vertex_circulator, Polyhedron_3_Facet_handle, \
    Polyhedron_3_Halfedge_around_facet_circulator, Polyhedron_3_Halfedge_handle

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
        return list(map(lambda x: self._vertex(x), both_levels_neighbours))

    # noinspection PyMethodMayBeStatic
    def _list_vertex_direct_neighbours(self, vertex):
        circulator = vertex.vertex_begin()  # type: Polyhedron_3_Halfedge_around_vertex_circulator
        for i in xrange(vertex.vertex_degree()):
            he = circulator.next()
            yield he.opposite().vertex()

    def find_vertex_faces(self, vertex_id):
        vertex = self.vertices[vertex_id]
        circulator = vertex.vertex_begin()
        facets = []
        for i in xrange(vertex.vertex_degree()):
            he = circulator.next()
            if not he.is_border():
                facets.append(self._facet(he.facet()))
        return facets

    def has_border(self):
        for he in self.polyhedron.halfedges():
            if he.is_border():
                return True
        return False

    def find_face_neighbors(self, face_id):
        facet = self.facets[face_id]
        both_levels_neighbours = set()  # actually this set will contain the analysed facet as well

        def find_single_face_neighbors(facet):
            circulator = facet.facet_begin()  # type: Polyhedron_3_Halfedge_around_facet_circulator
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
        return list(map(lambda x: self._facet(x), both_levels_neighbours))

    def flip_faces(self, face1_id, face2_id):
        face1 = self.facets[face1_id]  # type: Polyhedron_3_Facet_handle
        face2 = self.facets[face2_id]  # type: Polyhedron_3_Facet_handle
        diagonal = face1.halfedge()  # type: Polyhedron_3_Halfedge_handle
        for i in xrange(3):
            if not diagonal.is_border():
                opposite = diagonal.opposite()  # type: Polyhedron_3_Halfedge_handle
                if opposite.facet() == face2:
                    break
            diagonal = diagonal.next()
        joined = self.polyhedron.join_facet(diagonal)
        he1 = joined.next()  # type: Polyhedron_3_Halfedge_handle
        he2 = he1.next().next()  # type: Polyhedron_3_Halfedge_handle
        he2 = self.polyhedron.split_facet(he1, he2).opposite()  # type: Polyhedron_3_Halfedge_handle
        new_face1 = he1.facet()  # type: Polyhedron_3_Facet_handle
        new_face2 = he2.facet()  # type: Polyhedron_3_Facet_handle
        self.facets[face1_id] = new_face1
        self.facets[face2_id] = new_face2
        return self._facet(new_face1), self._facet(new_face2)

    def get_vertex(self, vertex_id):
        return self._vertex(self.vertices[vertex_id])

    def get_face(self, face_id):
        return self._facet(self.facets[face_id])

    def _vertex(self, vertex):
        return [float(x) for x in str(vertex.point()).split()]

    def _facet(self, facet):
        def dict_key(dict, value):
            for key in dict:
                if dict[key] == value:
                    return key

        he = facet.halfedge()  # type: Polyhedron_3_Halfedge_handle
        vertices = [he.vertex(), he.next().vertex(), he.next().next().vertex()]
        return list(map(lambda x: dict_key(self.vertices, x), vertices))


def print_triangle_vertices(facet):
    circulator = facet.facet_begin()  # type: Polyhedron_3_Halfedge_around_facet_circulator
    for i in xrange(3):
        he = circulator.next()
        print he.vertex().point(), '  \t',
    print


if __name__ == "__main__":
    operations = HalfedgeMeshOperations('data/test1.obj')
    vertex = operations.get_vertex(3)
    print('chosen vertex:')
    print(vertex)
    print('\nneighbours:')
    for v in operations.find_vertex_neighbors(3):
        print(v)

    print('\nfacets:')
    print(operations.find_vertex_faces(3))

    print('\nmesh has border:')
    print operations.has_border()

    print('\nface neighbours:')
    print(operations.find_face_neighbors(3))

    print('\n\nFlipping faces 2 and 3:')
    print(operations.get_face(2))
    print(operations.get_face(3))
    new_f1, new_f2 = operations.flip_faces(2, 3)
    print('\n---\n')
    print(new_f1)
    print(new_f2)
