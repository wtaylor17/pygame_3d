from pygame_3d import renderables, viewer

'''
cylinder_poly_demo.py
demo to show a cylinder, polygons only
----------------------------------------------
----------------------------------------------
----------------------------------------------
WRITTEN BY WILLIAM TAYLOR-MELANSON
----------------------------------------------
----------------------------------------------
----------------------------------------------
'''


# circular face centered at (250, 250, 100) with radius 50
front_face = renderables.build_circular_face(renderables.Vertex(250, 250, 100), 50)
# circular face centered at (250, 250, 200) with radius 50
back_face = [renderables.Vertex(v.x, v.y, v.z + 100) for v in front_face]
# create WireFrame and add vertices
cylinder = renderables.WireFrame(display_vertices=False)
cylinder.add_vertices(front_face)
cylinder.add_vertices(back_face)

# face creation
i = 1
print(str(len(back_face)))
while i < len(back_face) - 1:
    # front face polygon
    cylinder.add_cycle((0, 255, 0), [i, 0, i + 1])
    # back face polygon
    cylinder.add_cycle((255, 255, 0), [i + len(back_face), len(back_face), i + len(back_face) + 1])
    # middle (body) polygon
    cylinder.add_cycle((255, 0, 0), [i, i + len(back_face), i + len(back_face) + 1, i + 1])
    i += 1
# create viewer, add body to viewer, launch viewer
my_viewer = viewer.WireFrameViewer(500, 500)
my_viewer.add_body(cylinder)
my_viewer.run()
