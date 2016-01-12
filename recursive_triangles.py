import enum
import random
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

import math_help
import polygon
import color


class Direction(enum.Enum):
    Left = 0
    Right = 1
    # Up = 2


class RecursiveTriangles():

    def __init__(self, size, palet=color.ColorLayers, depth=None):
        if depth is None:
            depth = random.choice([5, 6, 7, 8, 9, 10])

        self.palet = palet
        self.image = Image.new("RGBA", size)

        _color = color.get_random_contrasting_color(
            color.ColorLayers.black, palet)
        init_triangle = polygon.fit_triangle_into_rect(size, _color)

        triangle_list = self.layer_sexy_triangles(init_triangle, depth)

        triangle_list = [init_triangle] + triangle_list

        compositor = polygon.PolygonCompositor(triangle_list)
        compositor.composite_on_to_image(self.image)

    def get_image(self):
        return self.image

    def layer_sexy_triangles(self, parent, depth):
        if depth <= 0:
            return []

        direction = random.choice(list(Direction))
        color_side = color.get_random_contrasting_color(parent.color_layer)
        color_up = color.get_random_contrasting_color(parent.color_layer)

        if direction == Direction.Right:
            side_tri = parent.make_right_subtriangle(color_side)
        else:
            side_tri = parent.make_left_subtriangle(color_side)
        tri_up = parent.make_top_subtriangle(color_up)

        tri_side_subtris = self.layer_sexy_triangles(side_tri, depth - 1)
        tri_up_subtris = self.layer_sexy_triangles(tri_up, depth - 1)

        tri_side_list = [side_tri] + tri_side_subtris
        tri_up_list = [tri_up] + tri_up_subtris

        return tri_side_list + tri_up_list


if __name__ == "__main__":
    base = int(4096 / 2)
    size = (base, math_help.get_triangle_base_relative_to_height(base))

    triangles = RecursiveTriangles(size, depth=10)

    img = triangles.get_image()

    # base = 500
    # size = (base, polygon.get_height_relative_to_base(base))
    # img.thumbnail(size, Image.ANTIALIAS)
    # img.thumbnail(size)

    img = img.filter(ImageFilter.SMOOTH_MORE)
    #img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    #img = img.filter(ImageFilter.FIND_EDGES)
    img = img.filter(ImageFilter.SHARPEN)

    img.save("rendered-images/recursive.gif", 'gif')
