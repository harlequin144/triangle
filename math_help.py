import math


def get_triangle_base_relative_to_height(height):
    return 2 * height * math.tan(math.radians(18))


def get_triangle_height_relative_to_base(base):
    return (base / 2) / math.tan(math.radians(18))


def get_diamond_base_relative_to_height(height):
    return get_triangle_base_relative_to_height(height / 2)


def get_diamond_height_relative_to_base(base):
    return 2 * get_triangle_height_relative_to_base(base)


def point_dist(p1, p2):
    x_1, y_1 = p1
    x_2, y_2 = p2
    return math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)


def mid_point(p1, p2):
    x_1, y_1 = p1
    x_2, y_2 = p2
    m_x = (x_1 + x_2) / 2
    m_y = (y_1 + y_2) / 2

    return (m_x, m_y)


def get_subtriangle_point(tip_point, verticie_point, subtri_side_len):
    x_t, y_t = tip_point
    x_v, y_v = verticie_point

    x = x_v - x_t
    y = y_v - y_t

    magnitude = math.sqrt(x**2 + y**2)
    x = x / magnitude
    y = y / magnitude

    x = x * subtri_side_len
    y = y * subtri_side_len

    return tip_point[0] + int(x), tip_point[1] + int(y)
