from CGAL.CGAL_Polyhedron_3 import Polyhedron_3, Polyhedron_3_Halfedge_iterator, Polyhedron_3_Vertex_handle, \
    Polyhedron_3_Halfedge_handle, Polyhedron_3_Halfedge_around_vertex_circulator, Polyhedron_3_Facet_handle


def create_vertices_map(polyhedron):
    vertices = dict()
    i = 1
    for v in polyhedron.vertices():
        vertices[i] = v
        i += 1
    return vertices


def list_vertex_direct_neighbours(vertex):
    circulator = vertex.vertex_begin()  # type: Halfedge_around_vertex_circulator
    for i in xrange(vertex.vertex_degree()):
        he = circulator.next()
        yield he.opposite().vertex()


def list_vertex_sec_level_neighbours(vertex):
    first_level_neighbours = set(list_vertex_direct_neighbours(vertex))

    both_levels_neighbours = set()  # actually this set will contain the analysed vertex as well
    both_levels_neighbours.update(first_level_neighbours)

    for vn in first_level_neighbours:
        both_levels_neighbours.update(list_vertex_direct_neighbours(vn))

    both_levels_neighbours.remove(vertex)
    return both_levels_neighbours.difference(first_level_neighbours)


def list_faces_vertex_belongs_to(vertex):
    circulator = vertex.vertex_begin()
    for i in xrange(vertex.vertex_degree()):
        he = circulator.next()
        if not he.is_border():
            yield he.facet()


def mesh_has_border(polyhedron):
    for he in polyhedron.halfedges():
        if he.is_border():
            return True
    return False

if __name__ == "__main__":
    polyhedron = Polyhedron_3('in/test1.off')
    vertices = create_vertices_map(polyhedron)
    print('chosen vertex:')
    print(vertices[3].point())
    print('\ndirect neighbours:')
    for v in list_vertex_direct_neighbours(vertices[3]):
        print v.point()
    print('\n2nd level neighbours:')
    for v in list_vertex_sec_level_neighbours(vertices[3]):
        print v.point()

    print('\nfacets:')
    for f in list_faces_vertex_belongs_to(vertices[3]):
        print f.id() # TODO do sth to be able to set IDs!

    print('\nmesh has border:')
    print mesh_has_border(polyhedron)

