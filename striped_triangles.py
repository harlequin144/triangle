import math

from PIL import Image
from PIL import ImageDraw

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



#rads = [450,400, 350, 300, 250, 200, 150]
rads = list(reversed(list(range(50, 1000, 50))))
#print(rads)

t1 = draw_concentric_triangles(rads, 
        [white] +  [black, red] * (len(rads) - 1),
        [white] + [red, black] * (len(rads) - 1))

t2 = draw_concentric_triangles(rads, 
        [white] +  [black, blue] * (len(rads) - 1),
        [white] + [blue, black] * (len(rads) - 1))


t2 = t2.rotate(180, expand = True)

#print(t1.size)

#height_to_width = t2.size[1] / t2.size[0]
#new_size = t1.size[0], int(t1.size[0] * height_to_width )

#t2 = t2.resize(new_size) #.rotate(108)
space = 50

img = Image.new("RGBA", (t1.width, (t1.height * 2) + space), black)

img.paste(t2, (0,0), t2)
img.paste(t1, (0,t1.height+ space), t1)

new_size = t1.size[0] , t1.size[1]

#img = img.resize(new_size, filter=Image.ANTIALIAS) #.rotate(108)

#img.save("my_pic.gif", 'gif')

#= Image.open(infile)

size = 1000, 1000
            
print('here')
#img.thumbnail(size, Image.ANTIALIAS)

img.save("my_pic.gif", 'gif')



# Use gif. This is the format that is most suitable for simple shapes with large
# spanns of one color
