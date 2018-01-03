from pygame_3d import renderables, viewer

'''
cube_complete_frame_demo.py
demo to show a cube, complete with visible
wire frame.
----------------------------------------------
----------------------------------------------
----------------------------------------------
WRITTEN BY WILLIAM TAYLOR-MELANSON
----------------------------------------------
----------------------------------------------
----------------------------------------------
'''

# create a cube with front-top-left corner at (100, 100, 100) with side length 100
cube = renderables.build_cube_complete_frame(renderables.Vertex(100, 100, 100), 100)
# create a viewer with window size (600, 450)
my_viewer = viewer.WireFrameViewer(600, 450)
# add cube to viewer
my_viewer.add_body(cube)
# launch viewer
my_viewer.run()
