from random import random, randint
from math import sin, cos, pi as PI
import pygame.gfxdraw as gfxdraw
from pygame.draw import line, lines, polygon
from pygame import Surface, Color, Rect
import pymunk as pm
from pymunk import Segment, Poly, Body, Space
from lib.math2 import flipy


class Rock(Body):

    def __init__(self, screen: Surface, space: Space, vertices: list, thickness: float, border_color: Color, fill_color: Color):
        super().__init__(body_type=Body.STATIC)
        #self.screen = screen
        self.border_color = border_color
        self.fill_color = fill_color
        self.vertices = vertices
        self.shape = Poly(self, vertices, None, thickness)
        self.shape.collision_type = 8
        space.add(self, self.shape)
        self.points = []
        for vert in self.vertices:
            self.points.append((int(vert[0]), flipy(int(vert[1]))))

    def draw(self, screen: Surface):
        t = int(self.shape.radius)
        #p1 = self.shape.a
        #p2 = self.shape.b
        #x1 = int(p1[0]); y1 = int(p1[1])
        #x2 = int(p2[0]); y2 = int(p2[1])
        #line(screen, self.border_color, (x1, flipy(y1)), (x2, flipy(y2)), t)
        polygon(screen, self.border_color, self.points, 0)
        polygon(screen, Color('gray'), self.points, 3)

    def update(self, dT:float) -> None:
        pass

    def kill(self, space: Space) -> None:
        space.remove(self.shape)
        space.remove(self)