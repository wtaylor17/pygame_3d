from pygame_3d import reading, viewer

my_viewer = viewer.WireFrameViewer(400, 400)
print('Enter file name: ')
p = input()
my_viewer.add_body(reading.make_frame(path=p))
my_viewer.run()
