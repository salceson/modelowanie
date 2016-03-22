# coding: utf-8

from CGAL.CGAL_Polyhedron_3 import Polyhedron_3, Polyhedron_modifier
from CGAL.CGAL_Kernel import Point_3

__author__ = "Michał Ciołczyk"


class AbstractMeshLoader(object):
    def __init__(self, filename):
        self.filename = filename

    def to_polyhedron(self):
        """
        Returns CGAL polyhedron representation of the object
        :return CGAL polyhedron
        :rtype Polyhedron_3
        """
        raise NotImplementedError()

    def to_vertices_and_faces(self):
        """
        Returns vertices list and faces list.
        :return vertices list, faces list
        :rtype list, list
        """
        raise NotImplementedError()


class ObjLoader(AbstractMeshLoader):
    # noinspection PyTypeChecker
    def __init__(self, filename):
        super(ObjLoader, self).__init__(filename)
        self.vertices = [None]
        self.faces = [None]
        with open(self.filename) as f:
            for line in f:
                line_contents = line.strip()
                if line_contents.startswith('#'):
                    continue
                line_contents = line_contents.split()
                if not line_contents:
                    continue
                if line_contents[0] == "v":
                    self.vertices.append([float(x) for x in line_contents[1:]])
                if line_contents[0] == "f":
                    self.faces.append([int(x) for x in line_contents[1:]])

    def to_vertices_and_faces(self):
        return self.vertices, self.faces

    def to_polyhedron(self):
        polyhedron_modifier = Polyhedron_modifier()
        polyhedron_modifier.begin_surface(len(self.vertices), len(self.faces))
        for vertex in self.vertices[1:]:
            polyhedron_modifier.add_vertex(Point_3(vertex[0], vertex[1], vertex[2]))
        for face in self.faces[1:]:
            polyhedron_modifier.begin_facet()
            for vertex in face:
                polyhedron_modifier.add_vertex_to_facet(vertex - 1)
            polyhedron_modifier.end_facet()
        polyhedron = Polyhedron_3()
        polyhedron.delegate(polyhedron_modifier)
        return polyhedron


class OffLoader(AbstractMeshLoader):
    def __init__(self, filename):
        super(OffLoader, self).__init__(filename)

    def to_polyhedron(self):
        return Polyhedron_3(self.filename)

    # noinspection PyTypeChecker
    def to_vertices_and_faces(self):
        vertices = [None]
        faces = [None]
        with open(self.filename) as f:
            read_amounts = False
            vertices_amount = 0
            vertices_read = 0
            for line in f:
                line_contents = line.strip()
                if line_contents == 'OFF' or line_contents.startswith('#'):
                    continue
                line_contents = line_contents.split()
                if not line_contents:
                    continue
                if not read_amounts:
                    amounts = [int(x) for x in line_contents]
                    vertices_amount = amounts[0]
                    read_amounts = True
                elif vertices_read < vertices_amount:
                    vertices.append([float(x) for x in line_contents])
                    vertices_read += 1
                else:
                    faces.append([int(x) + 1 for x in line_contents[1:]])
        return vertices, faces


if __name__ == "__main__":
    obj = ObjLoader("data/test1.obj")
    obj_vertices, obj_faces = obj.to_vertices_and_faces()
    obj_polyhedron = obj.to_polyhedron()
    print obj_vertices
    print obj_faces
    print obj_polyhedron
    off = OffLoader("data/test1.off")
    off_vertices, off_faces = off.to_vertices_and_faces()
    off_polyhedron = off.to_polyhedron()
    print off_vertices
    print off_faces
    print off_polyhedron
