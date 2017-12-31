from pygame_3d import renderables, viewer

pyramid = renderables.build_pyramid_complete_frame(renderables.Vertex(100, 100, 100), 200, 100)
my_viewer = viewer.WireFrameViewer(600, 450)
my_viewer.add_body(pyramid)
my_viewer.run()
