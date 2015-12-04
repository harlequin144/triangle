import enum
import random
import math
from collections import deque
from PIL import Image
from PIL import ImageDraw

import triangle
import color


class TriangleTypes(enum.Enum):
    Solid = 0
    Sierpinski = 1


class Positions(enum.Enum):
    top = 0
    right = 1
    left = 2


class SierpinskiTriangles():

    def __init__(self, size, depth=None):
        if depth is None:
            depth = random.choice([5, 6, 7, 8, 9])

        self.image = Image.new("RGBA", size)

        _color1 = color.get_random_contrasting_color(color.black)
        _color2 = color.get_random_contrasting_color(_color1)
        _color3 = color.get_random_contrasting_color(_color1)
        colors = [_color1, _color2, _color3]

        init_triangle = triangle.fit_triangle_into_rect(size, _color1)

        triangle_list = self.layer_sexy_triangles(init_triangle, depth, colors)

        triangle_list = [init_triangle] + triangle_list

        for tri in triangle_list:
            triangle_img = tri.render_image(size)
            self.image = Image.alpha_composite(self.image, triangle_img)

    def get_image(self):
        return self.image

    def layer_sexy_triangles(self, parent, depth, colors):
        if depth <= 0:
            return []

        t1 = parent.make_half_top_subtriangle()
        t2 = parent.make_half_right_subtriangle()
        t3 = parent.make_half_left_subtriangle()

        triangles = list([t1, t2, t3])
        random.shuffle(triangles)

        triangles[0].color = colors[0]
        triangles[1].color = colors[1]
        triangles[2].color = colors[1]

        #triangles[0].color = color.get_random_contrasting_color(colors[0])
        #triangles[1].color = color.get_random_contrasting_color(colors[0])
        #triangles[2].color = color.get_random_contrasting_color(colors[0])

        c = deque(colors)
        c.rotate(1)
        colors = list(c)

        subtriangles1 = self.layer_sexy_triangles(triangles[0], depth - 1,
                                                  colors)
        subtriangles2 = self.layer_sexy_triangles(triangles[1], depth - 1,
                                                  colors)
        subtriangles3 = self.layer_sexy_triangles(triangles[2], depth - 1,
                                                  colors)

        return triangles + subtriangles1 + subtriangles2 + subtriangles3


base = int(4096 / 4)
size = (base, triangle.get_height_relative_to_base(base))

triangles = SierpinskiTriangles(size, 7)

img = triangles.get_image()

# base = 500
# size = (base, triangle.get_height_relative_to_base(base))

# img.thumbnail(size, Image.ANTIALIAS)
# img.thumbnail(size)

img.save("sierpinski.gif", 'gif')