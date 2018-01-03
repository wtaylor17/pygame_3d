from pygame_3d import renderables, viewer

front_face = renderables.build_circular_face(renderables.Vertex(250, 250, 100), 50)
back_face = [renderables.Vertex(v.x, v.y, v.z + 100) for v in front_face]
cylinder = renderables.WireFrame()
cylinder.add_vertices(front_face)
cylinder.add_vertices(back_face)
for i in range(len(back_face) - 1):
    if i > 0:
        cylinder.add_cycle((0, 255, 0), [i, 0, i + 1])
        cylinder.add_cycle((255, 255, 0), [i + len(back_face), len(back_face), i + len(back_face) + 1])
        cylinder.add_cycle((255, 0, 0), [i, i + len(back_face), i + len(back_face) + 1, i + 1])
my_viewer = viewer.WireFrameViewer(500, 500)
my_viewer.add_body(cylinder)
my_viewer.run()
