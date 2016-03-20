from CGAL.CGAL_Polyhedron_3 import Polyhedron_3, Polyhedron_3_Halfedge_iterator

polyhedron = Polyhedron_3('in/test1.off')
n = 0
for h in polyhedron.vertices():
    print(h)
    n += 1
print(n)