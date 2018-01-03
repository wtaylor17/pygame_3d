import math


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbors = []

    def as_list(self):
        return [self.x, self.y, self.z]


class Cycle:
    def __init__(self, color, indices):
        self.color = color
        self.indices = indices


def distance_between(start, end):
    return math.sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2)


class WireFrame:
    def __init__(self, display_vertices=True, display_edges=True):
        self.vertices = []
        self.cycles = []
        self.display_vertices = display_vertices
        self.display_edges = display_edges
        self.display_polygons = True
        self.display_nested = True

    # add a vertex to the WireFrame
    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    # add a list of vertices to the WireFrame
    def add_vertices(self, vertex_list):
        self.vertices.extend(vertex_list)

    # add a cycle (rigid side) to the WireFrame
    def add_cycle(self, color, cycle):
        self.cycles.append(Cycle(color, cycle))

    # add a list of cycles to the WireFrame
    def add_cycles(self, cycles):
        self.cycles.extend(cycles)

    # add a list of neighbor vertices to the vertex at the specified index
    def add_neighbors(self, i, vertex_list):
        if i < 0 or i >= len(self.vertices):
            return
        self.vertices[i].neighbors.extend(vertex_list)

    def add_neighbors_by_index(self, v, indices):
        self.add_neighbors(v, [self.vertices[i] for i in indices])

    # translate the WireFrame along the specified axis
    def translate(self, axis, d):
        if axis in ['x', 'y', 'z']:
            for vertex in self.vertices:
                setattr(vertex, axis, getattr(vertex, axis) + d)

    # returns the mean location of the WireFrame
    def center(self):
        center = [0, 0, 0]
        length = len(self.vertices)
        if length == 0:
            return center
        for vertex in self.vertices:
            center[0] += vertex.x
            center[1] += vertex.y
            center[2] += vertex.z
        return [coordinate / length for coordinate in center]

    # scales the WireFrame by the specified factor about it's center
    def scale(self, scale):
        center = self.center()
        cx = center[0]
        cy = center[1]
        cz = center[2]
        for vertex in self.vertices:
            vertex.x = cx + (vertex.x - cx) * scale
            vertex.y = cy + (vertex.y - cy) * scale
            vertex.z = cz + (vertex.z - cz) * scale

    # rotates the WireFrame about the specified axis by the specified angle
    def rotate(self, axis, radians, center=None):
        if axis in ['x', 'y', 'z']:
            if center is None:
                center = self.center()
            for vertex in self.vertices:
                x = vertex.x - center[0]
                y = vertex.y - center[1]
                z = vertex.z - center[2]
                if axis is 'x':
                    r = math.hypot(y, z)
                    theta = math.atan2(y, z) + radians
                    vertex.z = center[2] + r*math.cos(theta)
                    vertex.y = center[1] + r*math.sin(theta)
                elif axis is 'y':
                    r = math.hypot(x, z)
                    theta = math.atan2(x, z) + radians
                    vertex.z = center[2] + r*math.cos(theta)
                    vertex.x = center[0] + r*math.sin(theta)
                elif axis is 'z':
                    r = math.hypot(x, y)
                    theta = math.atan2(y, x) + radians
                    vertex.x = center[0] + r*math.cos(theta)
                    vertex.y = center[1] + r*math.sin(theta)


# returns a WireFrame modelling a cube, with visible frame (neighbors)
def build_cube_complete_frame(location, side_length):
    cube = WireFrame()
    # create vertices
    top_vertices = [Vertex(x, location.y, z)
                    for x in (location.x, location.x + side_length) for z in (location.z, location.z + side_length)]
    bottom_vertices = [Vertex(vertex.x, vertex.y + side_length, vertex.z) for vertex in top_vertices]
    # add vertices to cubes
    cube.add_vertices(top_vertices)
    cube.add_vertices(bottom_vertices)
    # add neighbors (create frame)
    cube.add_neighbors_by_index(0, [1, 2, 4])
    cube.add_neighbors_by_index(1, [3, 5])
    cube.add_neighbors_by_index(2, [3, 6])
    cube.add_neighbors_by_index(3, [7])
    cube.add_neighbors_by_index(4, [5, 6])
    cube.add_neighbors_by_index(5, [7])
    cube.add_neighbors_by_index(6, [7])
    # add cycles (create sides)
    cube.add_cycle((0, 0, 255), [1, 3, 7, 5])
    cube.add_cycle((255, 0, 0), [0, 1, 3, 2])
    cube.add_cycle((255, 255, 0), [4, 5, 7, 6])
    cube.add_cycle((255, 0, 255), [0, 1, 5, 4])
    cube.add_cycle((0, 255, 0), [2, 3, 7, 6])
    cube.add_cycle((0, 255, 255), [0, 2, 6, 4])
    return cube


# returns a WireFrame modelling a cube with only cycles(sides)
def build_cube_poly(location, side_length):
    cube = WireFrame(display_edges=False, display_vertices=False)
    # create vertices
    top_vertices = [Vertex(x, location.y, z)
                    for x in (location.x, location.x + side_length) for z in (location.z, location.z + side_length)]
    bottom_vertices = [Vertex(vertex.x, vertex.y + side_length, vertex.z) for vertex in top_vertices]
    # add vertices to cube
    cube.add_vertices(top_vertices)
    cube.add_vertices(bottom_vertices)
    # add cycles (create sides)
    cube.add_cycle((0, 0, 255), [1, 3, 7, 5])
    cube.add_cycle((255, 0, 0), [0, 1, 3, 2])
    cube.add_cycle((255, 255, 0), [4, 5, 7, 6])
    cube.add_cycle((255, 0, 255), [0, 1, 5, 4])
    cube.add_cycle((0, 255, 0), [2, 3, 7, 6])
    cube.add_cycle((0, 255, 255), [0, 2, 6, 4])
    return cube


# returns a WireFrame modelling a pyramid, with visible frame (neighbors)
def build_pyramid_complete_frame(location, base, height):
    pyramid = WireFrame()
    top = Vertex(location.x + base / 2, location.y, location.z + base/2)
    base_vertices = [Vertex(x, top.y + height, z) for x in (location.x, location.x + base)
                     for z in (location.z, location.z + base)]
    mid_point = [0, 0, 0]
    for vertex in base_vertices:
        mid_point[0] += vertex.x / 4
        mid_point[1] += vertex.y / 4
        mid_point[2] += vertex.z / 4
    pyramid.add_vertex(top)
    pyramid.add_vertices(base_vertices)
    pyramid.add_vertex(Vertex(mid_point[0], mid_point[1], mid_point[2]))
    pyramid.add_neighbors(0, base_vertices)
    for i in range(1, 5):
        pyramid.add_neighbors(i, base_vertices)
    pyramid.add_cycle((255, 0, 0), [1, 2, 5])
    pyramid.add_cycle((255, 0, 0), [1, 3, 5])
    pyramid.add_cycle((255, 0, 0), [3, 4, 5])
    pyramid.add_cycle((255, 0, 0), [4, 2, 5])
    pyramid.add_cycle((0, 255, 255), [0, 1, 2])
    pyramid.add_cycle((255, 255, 0), [0, 1, 3])
    pyramid.add_cycle((0, 255, 0), [0, 2, 4])
    pyramid.add_cycle((0, 0, 255), [0, 4, 3])
    return pyramid


# returns a WireFrame modelling a pyramid with only cycles(sides)
def build_pyramid_poly(location, base, height):
    pyramid = WireFrame()
    top = Vertex(location.x + base / 2, location.y, location.z + base / 2)
    base_vertices = [Vertex(x, top.y + height, z) for x in (location.x, location.x + base)
                     for z in (location.z, location.z + base)]
    mid_point = [0, 0, 0]
    for vertex in base_vertices:
        mid_point[0] += vertex.x / 4
        mid_point[1] += vertex.y / 4
        mid_point[2] += vertex.z / 4
    pyramid.add_vertex(top)
    pyramid.add_vertices(base_vertices)
    pyramid.add_vertex(Vertex(mid_point[0], mid_point[1], mid_point[2]))
    pyramid.add_cycle((255, 0, 0), [1, 2, 5])
    pyramid.add_cycle((255, 0, 0), [1, 3, 5])
    pyramid.add_cycle((255, 0, 0), [3, 4, 5])
    pyramid.add_cycle((255, 0, 0), [4, 2, 5])
    pyramid.add_cycle((0, 255, 255), [0, 1, 2])
    pyramid.add_cycle((255, 255, 0), [0, 1, 3])
    pyramid.add_cycle((0, 255, 0), [0, 2, 4])
    pyramid.add_cycle((0, 0, 255), [0, 4, 3])
    return pyramid


# returns a list of vertices modelling a 2D circle
def build_circular_face(center, radius):
    i = 0
    z = center.z
    circle_vertices = list()
    circle_vertices.append(center)
    while i <= 2 * math.pi + 0.1:
        # create face of circle
        circle_vertices.append(Vertex(center.x + radius * math.cos(i), center.y + radius * math.sin(i), z))
        i += 0.1
    return circle_vertices
