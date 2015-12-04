import math

from PIL import Image
from PIL import ImageDraw


def fit_triangle_into_rect(dimensions, color):
    base, height = dimensions

    if (base % 2) != 0:
        base = base - 1

    if get_base_relative_to_height(height) > base:
        height = get_height_relative_to_base(base)
    else:
        base = get_base_relative_to_height(height)

    top = (base // 2, height)
    left = (0, 0)
    right = (base, 0)

    return Triangle(top, left, right, color)


def get_base_relative_to_height(height):
    return int(2 * height * math.tan(math.radians(18)))


def get_height_relative_to_base(base):
    return int((base / 2) / math.tan(math.radians(18)))


def point_dist(p1, p2):
    x_1, y_1 = p1
    x_2, y_2 = p2
    return math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)


def mid_point(p1, p2):
    x_1, y_1 = p1
    x_2, y_2 = p2
    m_x = int((x_1 + x_2) / 2)
    m_y = int((y_1 + y_2) / 2)

    return (m_x, m_y)


def get_subtriangle_point(tip_point, verticie_point, subtri_side_len):
    x_t, y_t = tip_point
    x_v, y_v = verticie_point

    x = x_v - x_t
    y = y_v - y_t

    magnitude = math.sqrt(x**2 + y**2)
    #print('subtri_side_len: ' + str(subtri_side_len))
    #print('magnitude: ' + str(magnitude))
    x = x / magnitude
    y = y / magnitude

    x = x * subtri_side_len
    y = y * subtri_side_len

    return tip_point[0] + int(x), tip_point[1] + int(y)


class Triangle():

    def __init__(self, top_point, left_point, right_point, color=None):
        self.top = top_point
        self.left = left_point
        self.right = right_point
        self.color = color

    def get_points(self):
        return (self.top, self.left, self.right)

    def render_image(self, container_size):
        img = Image.new('RGBA', container_size)
        img_draw = ImageDraw.Draw(img)
        img_draw.polygon(self.get_points(), fill=self.color)

        return img

    def make_right_subtriangle(self, color):
        # top point points right
        top = self.right
        right = self.left

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = point_dist(self.right, self.left)

        left = get_subtriangle_point(self.top, self.left, side_len)

        return Triangle(top, left, right, color)

    def make_left_subtriangle(self, color):
        # top point points left
        top = self.left
        left = self.right

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = point_dist(self.right, self.left)

        right = get_subtriangle_point(self.top, self.right, side_len)

        return Triangle(top, left, right, color)

    def make_top_subtriangle(self, color):
        # top point points left
        top = self.top

        x_1 = self.left[0]
        x_2 = self.right[0]
        side_len = point_dist(self.right, self.left)

        right = get_subtriangle_point(self.top, self.right, side_len)
        left = get_subtriangle_point(self.top, self.left, side_len)

        return Triangle(top, left, right, color)

    def make_half_top_subtriangle(self, color=None):
        top = self.top
        left = mid_point(self.top, self.left)
        right = mid_point(self.top, self.right)

        return Triangle(top, left, right, color)

    def make_half_left_subtriangle(self, color=None):
        top = mid_point(self.top, self.left)
        left = self.left
        right = mid_point(self.left, self.right)

        return Triangle(top, left, right, color)

    def make_half_right_subtriangle(self, color=None):
        top = mid_point(self.top, self.right)
        left = mid_point(self.left, self.right)
        right = self.right

        return Triangle(top, left, right, color)
