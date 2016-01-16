import enum
import random
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

import math_help
import polygon
import color


class PolygonAggregate():

    def __init__(self, container_size, palet=color.ColorLayers, depth=6):
        self.container_size = container_size
        self._palet = palet
        self._depth = depth

        self._polygon_list = None

    def get_palet(self):
        return self._palet

    def get_depth(self):
        return self._depth

    def get_polygon_list(self):
        return self._polygon_list

    def get_image(self):
        compositor = polygon.PolygonCompositor(self)
        return compositor.composite_on_image()

    def get_dxf(self):
        compositor = polygon.PolygonCompositor(self)
        return compositor.composite_on_dxf_using_polygons()


class Direction(enum.Enum):
    Left = 0
    Right = 1


class RecursiveTriangles(PolygonAggregate):

    def __init__(self, container_size, palet=color.ColorLayers, depth=6):
        super(RecursiveTriangles, self).__init__(container_size,
                                                 palet,
                                                 depth)

        _color = color.get_random_contrasting_color(color.ColorLayers.black,
                                                    palet)

        init_triangle = polygon.fit_triangle_into_rect(self.container_size,
                                                       _color)

        self.polygon_list = self.layer_sexy_triangles(init_triangle, depth)

        self.polygon_list = [init_triangle] + self.polygon_list

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


class Positions(enum.Enum):
    top = 0
    right = 1
    left = 2


class SierpinskiTriangles(PolygonAggregate):

    def __init__(self, container_size, palet=color.ColorLayers, depth=6):
        super(SierpinskiTriangles, self).__init__(container_size,
                                                  palet,
                                                  depth)

        init_triangle = polygon.fit_triangle_into_rect(size, palet[0])

        self.polygon_list = self.layer_sexy_triangles(init_triangle,
                                                      depth, palet)

        self.polygon_list = [init_triangle] + self.polygon_list

    # def make_image(self):
    #    image = Image.new("RGBA", size)
    #    compositor = polygon.PolygonCompositor(self._triangle_list)
    #    compositor.composite_on_to_image(image)
    #    return image

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


class SierpinskiDiamonds(PolygonAggregate):

    def __init__(self, container_size, palet=color.ColorLayers, depth=6):
        super(SierpinskiDiamonds, self).__init__(container_size,
                                                 palet,
                                                 depth)

        init_triangle = polygon.make_diamond_fitting_rect(size, palet[0])

        self.polygon_list = [init_triangle] +  \
            self.layer_sexy_diamonds(init_triangle, depth, palet)

    # def make_image(self):
    #    size_x, size_y = size
    #    image = Image.new("RGBA", (int(size_x), int(size_y)))
    #    # , (255, 255, 255, 0))
    #    compositor = polygon.PolygonCompositor(self._diamond_list)
    #    compositor.composite_on_to_image(image)
    #    return image

    def get_diamonds(self):
        return self._diamond_list

    def get_layers(self):
        return self._colors

    def layer_sexy_diamonds(self, parent, depth, colors):
        if depth <= 0:
            return []

        d1 = parent.make_half_top_subdiamond()
        d2 = parent.make_half_right_subdiamond()
        d3 = parent.make_half_left_subdiamond()
        d4 = parent.make_half_bot_subdiamond()

        diamonds = [d1, d2, d3, d4]

        random.shuffle(diamonds)

        first_color = colors[0]
        while colors[0] == first_color:
            random.shuffle(colors)

        diamonds[0].color_layer = colors[0]
        # diamonds[1].color_layer = colors[0]
        # diamonds[2].color_layer = colors[1]
        # diamonds[3].color_layer = colors[2]

        subd1 = self.layer_sexy_diamonds(diamonds[1], depth - 1, colors)
        subd2 = self.layer_sexy_diamonds(diamonds[2], depth - 1, colors)
        subd3 = self.layer_sexy_diamonds(diamonds[3], depth - 1, colors)

        return [diamonds[0]] + subd1 + subd2 + subd3


if __name__ == "__main__":
    base = 4096 / 2
    size = (base, math_help.get_triangle_height_relative_to_base(base))

    sierpinski_colors = color.get_random_sample(3)

    rec_triangles = RecursiveTriangles(size, depth=8)
    sier_triangles = SierpinskiTriangles(size, sierpinski_colors, depth=7)
    sier_diamonds = SierpinskiDiamonds(size, sierpinski_colors, depth=4)

    rec_triangles_img = rec_triangles.get_image()
    sier_triangles_img = sier_triangles.get_image()
    sier_diamonds_img = sier_diamonds.get_image()

    rec_triangles_img.save("rendered-images/recursive_triangle.gif", 'gif')
    sier_triangles_img.save("rendered-images/sierpinski_triangle.gif", 'gif')
    sier_diamonds_img.save("rendered-images/sierpinski_diamond.gif", 'gif')

    rec_triangles_dxf = rec_triangles.get_dxf()
    sier_triangles_dxf = sier_triangles.get_dxf()
    sier_diamonds_dxf = sier_diamonds.get_dxf()

    rec_triangles_dxf.saveas("rendered-images/recursive_triangle.dxf")
    sier_triangles_dxf.saveas("rendered-images/sierpinski_triangle.dxf")
    sier_diamonds_dxf.saveas("rendered-images/sierpinski_diamond.dxf")
