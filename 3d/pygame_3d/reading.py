from pygame_3d import renderables, viewer


def make_frame(path):
    obj = ObjFile(path)
    wf = renderables.WireFrame()
    wf.add_vertices(obj.vertices)
    wf.add_cycles(obj.faces)
    for cycle in wf.cycles:
        indices = cycle.indices
        wf.add_neighbors(indices[0], [wf.vertices[indices[1]], wf.vertices[indices[2]]])
        wf.add_neighbors(indices[1], [wf.vertices[indices[2]]])
    return wf


class ObjFile:
    def __init__(self, path):
        f = open(path, 'r')
        self.vertices = list()
        self.faces = list()
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.split(' ')
            t = line[0]
            if t == 'v':
                self.vertices.append(renderables.Vertex(float(line[1]), float(line[2]), float(line[3])))
            elif t == 'f':
                self.faces.append(renderables.Cycle(
                    viewer.get_grad_rgb([int(x) - 1 for x in line[1:]], self.vertices),
                    [int(x) - 1 for x in line[1:]]))
