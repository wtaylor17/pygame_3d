from pygame_3d import renderables, viewer

'''
pyramid_complete_frame_demo.py
demo to show a pyramid, complete with visible
wire frame.
----------------------------------------------
----------------------------------------------
----------------------------------------------
WRITTEN BY WILLIAM TAYLOR-MELANSON
----------------------------------------------
----------------------------------------------
----------------------------------------------
'''

# create a pyramid with top vertex at (100, 100, 100) with base 200 and height 100
pyramid = renderables.build_pyramid_complete_frame(renderables.Vertex(100, 100, 100), 200, 100)
# create a viewer with window size (600, 450)
my_viewer = viewer.WireFrameViewer(600, 450)
# add pyramid to viewer
my_viewer.add_body(pyramid)
# launch viewer
my_viewer.run()
