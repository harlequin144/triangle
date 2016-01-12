from PIL import Image
from PIL import ImageDraw

import math

import color
import math_help


class Triangle():

    def __init__(self, top_point, left_point, right_point, color_layer):
        self.top = top_point
        self.left = left_point
        self.right = right_point
        self.color_layer = color_layer

    def get_points(self):
        return (self.top, self.left, self.right)

    def make_right_subtriangle(self, color_layer):
        # top point points right
        top = self.right
        right = self.left

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = math_help.point_dist(self.right, self.left)

        left = math_help.get_subtriangle_point(self.top, self.left, side_len)

        return Triangle(top, left, right, color_layer)

    def make_left_subtriangle(self, color_layer):
        # top point points left
        top = self.left
        left = self.right

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = math_help.point_dist(self.right, self.left)

        right = math_help.get_subtriangle_point(self.top, self.right, side_len)

        return Triangle(top, left, right, color_layer)

    def make_top_subtriangle(self, color_layer):
        # top point points left
        top = self.top

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = math_help.point_dist(self.right, self.left)

        right = math_help.get_subtriangle_point(self.top, self.right, side_len)
        left = math_help.get_subtriangle_point(self.top, self.left, side_len)

        return Triangle(top, left, right, color_layer)

    def make_half_top_subtriangle(self, color_layer=None):
        top = self.top
        left = math_help.mid_point(self.top, self.left)
        right = math_help.mid_point(self.top, self.right)

        return Triangle(top, left, right, color_layer)

    def make_half_left_subtriangle(self, color_layer=None):
        top = math_help.mid_point(self.top, self.left)
        left = self.left
        right = math_help.mid_point(self.left, self.right)

        return Triangle(top, left, right, color_layer)

    def make_half_right_subtriangle(self, color_layer=None):
        top = math_help.mid_point(self.top, self.right)
        left = math_help.mid_point(self.left, self.right)
        right = self.right

        return Triangle(top, left, right, color_layer)

    def make_half_mid_subtriangle(self, color_layer=None):
        top = math_help.mid_point(self.right, self.left)
        left = math_help.mid_point(self.top, self.right)
        right = math_help.mid_point(self.top, self.left)

        return Triangle(top, left, right, color_layer)


def fit_triangle_into_rect(dimensions, color_layer):
    base, height = dimensions

    if (base % 2) != 0:
        base = base - 1

    if math_help.get_triangle_base_relative_to_height(height) > base:
        height = math_help.get_triangle_height_relative_to_base(base)
    else:
        base = math_help.get_triangle_base_relative_to_height(height)

    top = (base // 2, height)
    left = (0, 0)
    right = (base, 0)

    return Triangle(top, left, right, color_layer)


class Diamond():

    def __init__(self, top_point, left_point, right_point, bot_point,
                 color_layer):
        self.top = top_point
        self.left = left_point
        self.right = right_point
        self.bot = bot_point
        self.color_layer = color_layer

    def get_points(self):
        return (self.top, self.left, self.bot, self.right)

    def make_half_top_subdiamond(self, color_layer=None):
        top = self.top
        bot = math_help.mid_point(self.top, self.bot)
        left = math_help.mid_point(self.top, self.left)
        right = math_help.mid_point(self.top, self.right)

        return Diamond(top, left, right, bot, color_layer)

    def make_half_left_subdiamond(self, color_layer=None):
        top = math_help.mid_point(self.top, self.left)
        bot = math_help.mid_point(self.bot, self.left)
        left = self.left
        right = math_help.mid_point(self.left, self.right)

        return Diamond(top, left, right, bot, color_layer)

    def make_half_right_subdiamond(self, color_layer=None):
        top = math_help.mid_point(self.top, self.right)
        bot = math_help.mid_point(self.bot, self.right)
        left = math_help.mid_point(self.left, self.right)
        right = self.right

        return Diamond(top, left, right, bot, color_layer)

    def make_half_bot_subdiamond(self, color_layer=None):
        top = math_help.mid_point(self.top, self.bot)
        bot = self.bot
        left = math_help.mid_point(self.bot, self.left)
        right = math_help.mid_point(self.bot, self.right)

        return Diamond(top, left, right, bot, color_layer)


def make_diamond_fitting_rect(dimensions, color_layer):
    base, height = dimensions

    if (base % 2) != 0:
        base = base - 1

    if math_help.get_diamond_base_relative_to_height(height) > base:
        height = math_help.get_diamond_height_relative_to_base(base)
    else:
        base = math_help.get_diamond_base_relative_to_height(height)

    top = (base // 2, height)
    bot = (base // 2, 0)
    left = (0, height // 2)
    right = (base, height // 2)

    return Diamond(top, left, right, bot, color_layer)


class PolygonCompositor:

    def __init__(self, polygon_list):
        self._polygon_list = polygon_list

    def composite_on_to_image(self, image):
        drawer = ImageDraw.Draw(image)

        for poly in self._polygon_list:
            c = color.get_color_from_color_layer(poly.color_layer)
            # print(c)
            drawer.polygon(poly.get_points(), fill=c)
