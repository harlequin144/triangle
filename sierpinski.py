import enum
import random
import math
from collections import deque
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

import polygon
import color
import math_help


class Positions(enum.Enum):
    top = 0
    right = 1
    left = 2


class SierpinskiTriangles():

    def __init__(self, size, palet, depth):
        init_triangle = polygon.fit_triangle_into_rect(size, palet[0])

        self._colors = palet
        self._triangle_list = self.layer_sexy_triangles(
            init_triangle, depth, palet)

        self._triangle_list = [init_triangle] + self._triangle_list

    def make_image(self):
        image = Image.new("RGBA", size)
        compositor = polygon.PolygonCompositor(self._triangle_list)
        compositor.composite_on_to_image(image)
        return image

    def get_triangles(self):
        return self._triangle_list

    def get_layers(self):
        return self._colors

    def layer_sexy_triangles(self, parent, depth, colors):
        if depth <= 0:
            return []

        t1 = parent.make_half_top_subtriangle()
        t2 = parent.make_half_right_subtriangle()
        t3 = parent.make_half_left_subtriangle()
        t4 = parent.make_half_mid_subtriangle()

        first_color = colors[0]
        while colors[0] == first_color:
            random.shuffle(colors)

        t4.color_layer = colors[0]

        subtriangles1 = self.layer_sexy_triangles(t1, depth - 1, colors)
        subtriangles2 = self.layer_sexy_triangles(t2, depth - 1, colors)
        subtriangles3 = self.layer_sexy_triangles(t3, depth - 1, colors)

        return [t4] + subtriangles1 + subtriangles2 + subtriangles3

class SierpinskiDiamond():

    def __init__(self, size, palet, depth):
        init_triangle = math_help.fit_triangle_into_rect(size, palet[0])

        self._colors = palet
        self._triangle_list = self.layer_sexy_triangles(
            init_triangle, depth, palet)

        self._triangle_list = [init_triangle] + self._triangle_list

    def make_image(self):
        image = Image.new("RGBA", size)
        compositor = triangle.TriangleCompositor(self._triangle_list)
        compositor.composite_on_to_image(image)
        return image

    def get_triangles(self):
        return self._triangle_list

    def get_layers(self):
        return self._colors

    def layer_sexy_triangles(self, parent, depth, colors):
        if depth <= 0:
            return []

        t1 = parent.make_half_top_subtriangle()
        t2 = parent.make_half_right_subtriangle()
        t3 = parent.make_half_left_subtriangle()
        t4 = parent.make_half_mid_subtriangle()

        first_color = colors[0]
        while colors[0] == first_color:
            random.shuffle(colors)

        t4.color_layer = colors[0]

        subtriangles1 = self.layer_sexy_triangles(t1, depth - 1, colors)
        subtriangles2 = self.layer_sexy_triangles(t2, depth - 1, colors)
        subtriangles3 = self.layer_sexy_triangles(t3, depth - 1, colors)

        return [t4] + subtriangles1 + subtriangles2 + subtriangles3



if __name__ == "__main__":
    base = int(4096 / 2)
    size = (base, math_help.get_triangle_height_relative_to_base(base))

    selected_colors = color.get_random_sample(3)

    triangles = SierpinskiTriangles(size, selected_colors, depth=7)

    img = triangles.make_image()

    # base = 500
    # size = (base, triangle.get_height_relative_to_base(base))

    # img.thumbnail(size, Image.ANTIALIAS)
    #img = img.filter(ImageFilter.SMOOTH_MORE)
    #img = img.filter(ImageFilter.SHARPEN)
    #img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    img.save("rendered-images/sierpinski.gif", 'gif')
