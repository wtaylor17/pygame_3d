from pygame_3d import renderables, viewer

sphere = renderables.WireFrame(display_vertices=False)
my_viewer = viewer.WireFrameViewer(500, 500)

r = 1
for z in range(100, 200, 4):
    face = renderables.build_circular_face(renderables.Vertex(250, 250, z), r)
    n = len(sphere.vertices)
    sphere.add_vertices(face)
    sphere.add_cycle((255, 0, 0), [i for i in range(n, n + len(face))])
    if z < 150:
        r += 5
    else:
        r -= 5
my_viewer.add_body(sphere)
my_viewer.run()
