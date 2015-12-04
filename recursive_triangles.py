import enum
import random
import math
from PIL import Image
from PIL import ImageDraw

import triangle
import color


class Direction(enum.Enum):
    Left = 0
    Right = 1
    # Up = 2


class RecursiveTriangles():

    def __init__(self, size, depth=None):
        if depth is None:
            depth = random.choice([5, 6, 7, 8, 9])

        self.image = Image.new("RGBA", size)

        _color = color.get_random_contrasting_color(color.black)
        init_triangle = triangle.fit_triangle_into_rect(size, _color)

        triangle_list = self.layer_sexy_triangles(init_triangle, depth)

        triangle_list = [init_triangle] + triangle_list

        for tri in triangle_list:
            triangle_img = tri.render_image(size)
            self.image = Image.alpha_composite(self.image, triangle_img)

    def get_image(self):
        return self.image

    def layer_sexy_triangles(self, parent, depth):
        if depth <= 0:
            return []

        direction = random.choice(list(Direction))
        color_side = color.get_random_contrasting_color(parent.color)
        color_up = color.get_random_contrasting_color(parent.color)

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


# base = int(4096 / 2)
base = int(4096 / 4)
size = (base, triangle.get_height_relative_to_base(base))

triangles = RecursiveTriangles(size, 8)

img = triangles.get_image()

# base = 500
# size = (base, triangle.get_height_relative_to_base(base))

# img.thumbnail(size, Image.ANTIALIAS)
# img.thumbnail(size)

img.save("recursive.gif", 'gif')
# img.show()
