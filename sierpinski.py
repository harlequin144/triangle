import enum
import random
import math
from collections import deque
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

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

    def __init__(self, size, palet=color.ColorLayers, depth=None):
        if depth is None:
            depth = random.choice([5, 6, 7, 8, 9])

        l1 = color.get_random_contrasting_color(color.ColorLayers.black, palet)
        l2 = color.get_random_contrasting_color(l1, palet)
        l3 = color.get_random_contrasting_color(l1, palet)
        selected_colors = [l1, l2, l3]

        init_triangle = triangle.fit_triangle_into_rect(size, l1)

        self._triangle_list = self.layer_sexy_triangles(
            init_triangle, depth, selected_colors)

        self._triangle_list = [init_triangle] + self._triangle_list

    def make_image(self):
        image = Image.new("RGBA", size)
        compositor = triangle.TriangleCompositor(self._triangle_list)
        compositor.composite_on_to_image(image)
        return image

    def get_triangles(self):
        return self._triangle_list

    def layer_sexy_triangles(self, parent, depth, colors):
        if depth <= 0:
            return []

        t1 = parent.make_half_top_subtriangle()
        t2 = parent.make_half_right_subtriangle()
        t3 = parent.make_half_left_subtriangle()

        triangles = list([t1, t2, t3])
        random.shuffle(triangles)

        triangles[0].color_layer = colors[0]
        triangles[1].color_layer = colors[1]
        triangles[2].color_layer = colors[1]

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


if __name__ == "__main__":
    base = int(4096 / 2)
    size = (base, triangle.get_height_relative_to_base(base))

    triangles = SierpinskiTriangles(size, depth=3)

    img = triangles.make_image()

    # base = 500
    # size = (base, triangle.get_height_relative_to_base(base))

    # img.thumbnail(size, Image.ANTIALIAS)
    # img.thumbnail(size)
    #img = img.filter(ImageFilter.SMOOTH_MORE)
    #img = img.filter(ImageFilter.SHARPEN)
    #img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    img.save("rendered-images/sierpinski.gif", 'gif')
