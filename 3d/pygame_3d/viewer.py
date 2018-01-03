import pygame
from pygame import time as time


class WireFrameViewer:
    def __init__(self, w, h, caption="Demo", background=(255, 255, 255)):
        self.bodies = []
        self.screen = pygame.display.set_mode((w, h))
        self.width = w
        self.height = h
        pygame.display.set_caption(caption)
        self.background = background
        self.vertex_color = (255, 0, 0)
        self.edge_color = (0, 255, 0)
        self.clock = time.Clock()
        self.frame_count = 0
        self.flag_frame = 0

    # add a body to the viewer
    def add_body(self, body):
        self.bodies.append(body)

    # displays the specified WireFrame
    def display(self, frame):
        for vertex in frame.vertices:
            if frame.display_edges:
                for neighbor in vertex.neighbors:
                    pygame.draw.aaline(self.screen, self.edge_color,
                                       (vertex.x, vertex.y),
                                       (neighbor.x, neighbor.y))
            if frame.display_vertices:
                pygame.draw.circle(self.screen, self.vertex_color, (int(vertex.x), int(vertex.y)), 8)
        if frame.display_polygons:
            frame.cycles.sort(key=lambda c: sum([frame.vertices[i].z / len(c.indices) for i in c.indices]))
            for cycle in frame.cycles:
                pygame.draw.polygon(self.screen, cycle.color,
                                    [[frame.vertices[i].x, frame.vertices[i].y]
                                     for i in cycle.indices])

    # game loop
    def run(self):
        running = True
        while running:
            # empty the event queue
            if len([event for event in pygame.event.get() if event.type is pygame.QUIT]):
                running = False

            keys = pygame.key.get_pressed()
            theta = 0  # z rotation
            phi = 0  # x rotation
            zeta = 0  # y rotation
            scale = 1
            translation = {'x':  0, 'y': 0, 'z': 0}
            origin = None
            # key event handling
            if keys[pygame.K_w]:
                phi = -0.1
            elif keys[pygame.K_s]:
                phi = 0.1
            if keys[pygame.K_a]:
                zeta = -0.1
            elif keys[pygame.K_d]:
                zeta = 0.1
            if keys[pygame.K_q]:
                theta = -0.1
            elif keys[pygame.K_e]:
                theta = 0.1
            if keys[pygame.K_MINUS]:
                scale = 0.85
            elif keys[pygame.K_EQUALS]:
                scale = 1.25
            if keys[pygame.K_UP]:
                translation['y'] = -3
            if keys[pygame.K_DOWN]:
                translation['y'] = 3
            if keys[pygame.K_LEFT]:
                translation['x'] = -3
            if keys[pygame.K_RIGHT]:
                translation['x'] = 3
            # vertex/edge visibility flags
            vertex_flag = False
            edge_flag = False
            cycle_flag = False
            if keys[pygame.K_n]:
                vertex_flag = True
            if keys[pygame.K_m]:
                edge_flag = True
            if keys[pygame.K_k]:
                cycle_flag = True
            change_flag = False
            self.screen.fill(self.background)
            for body in self.bodies:
                body.rotate('z', theta, origin)
                body.rotate('x', phi, origin)
                body.rotate('y', zeta, origin)
                for key in translation.keys():
                    body.translate(key, translation[key])
                body.scale(scale)
                if vertex_flag and self.frame_count - self.flag_frame > 5:
                    body.display_vertices = not body.display_vertices
                    change_flag = True
                if edge_flag and self.frame_count - self.flag_frame > 5:
                    body.display_edges = not body.display_edges
                    change_flag = True
                if cycle_flag and self.frame_count - self.flag_frame > 5:
                    body.display_polygons = not body.display_polygons
                    change_flag = True
                self.display(body)
            # visibility change occurred, update frame variables
            if change_flag:
                self.flag_frame = self.frame_count
            pygame.display.flip()
            self.clock.tick(35)
            self.frame_count += 1
