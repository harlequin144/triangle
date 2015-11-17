import math

from PIL import Image
from PIL import ImageDraw

import triangle

size = (4096*2)

red = (222, 90, 81, 255) #DE5A51
blue = (97, 205, 245, 255) #61CDF5
white = (242, 241, 237, 255) #F2F1ED
black = (5,5,5,255) #555


def make_triangle_and_subtriangle_points(center, radius):
    center_x, center_y = int(center[0]), int(center[1])

    bot_x_off = int(radius/(math.tan(math.radians(36))))
    top_point_y = int(math.tan(math.radians(72)) * bot_x_off) - radius

    top_point = center_x, center_y + top_point_y
    bot_left_point = center_x - bot_x_off, center_y - radius 
    bot_right_point = center_x + bot_x_off, center_y - radius 

    base = bot_x_off * 2
    small_x = bot_left_point[0] + int(math.cos(math.radians(36)) * base)
    small_y = bot_left_point[1] + int(math.sin(math.radians(36)) * base)
    small_point = small_x , small_y 

    big_triangle = top_point, bot_left_point, bot_right_point
    small_triangle = bot_left_point, bot_right_point, small_point 

    return big_triangle, small_triangle 

def draw_concentric_triangles(radii, colors_big, colors_small):
    max_radii = max(radii)

    width = int(2 *(max_radii/(math.tan(math.radians(36)))))
    height = int(math.tan(math.radians(72)) * (width/2)) 
    img_size = width, height

    center = (width/2), max_radii
    triangles = [make_triangle_and_subtriangle_points(center, r) for r in radii]
    #print(triangles)

    triangle_image = Image.new('RGBA', img_size)
    draw_tri = ImageDraw.Draw(triangle_image)

    for points, color in zip([t[0] for t in triangles], colors_big):
        draw_tri.polygon(points, fill = color)

    for points, color in zip([t[1] for t in triangles], colors_small):
        draw_tri.polygon(points, fill = color)

    return triangle_image



size = (4096, triangle.get_height_relative_to_base(4096))


t1 = triangle.fit_triangle_into_rect(size, blue)
t1_image = t1.render_image(size)

t2 = t1.make_right_subtriangle(white)
t2_image = t2.render_image(size)


img = Image.new("RGBA", size, black)
img.paste(t1_image, (0,0), t1_image)
img.paste(t2_image, (0,0), t2_image)


img.save("test.gif", 'gif')

