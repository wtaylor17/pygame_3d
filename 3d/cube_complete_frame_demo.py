from pygame_3d import renderables, viewer

cube = renderables.build_cube_complete_frame(renderables.Vertex(100, 100, 100), 100)
my_viewer = viewer.WireFrameViewer(600, 450)
my_viewer.add_body(cube)
my_viewer.run()
