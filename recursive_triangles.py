import enum
import random
import math
from PIL import Image
from PIL import ImageDraw

import triangle


red = (222, 90, 81, 255) #DE5A51
blue = (97, 205, 245, 255) #61CDF5
white = (242, 241, 237, 255) #F2F1ED
black = (5,5,5,255) #555

colors = [red, blue, black]


class Direction(enum.Enum):
    Left = 0
    Right = 1
    #Up = 2

class RecursiveTriangles():

    def __init__(self, size, depth = None):
        #point_dir = Direction.Up
        if depth == None:
            depth = random.choice([5,6,7,8,9])

        self.image = Image.new("RGBA", size, white)

        init_triangle = triangle.fit_triangle_into_rect(size, black)

        triangle_list = self.layer_sexy_triangles(init_triangle, depth)

        triangle_list = [init_triangle] +  triangle_list 

        for tri in triangle_list:
            triangle_img = tri.render_image(size)
            self.image.paste(triangle_img, (0,0), triangle_img)

    def get_image(self):
        return self.image


    def layer_sexy_triangles(self, parent, depth):
        if depth <= 0:
            return []

        direction = random.choice(list(Direction))
        color = colors[depth%3]

        #if direction == Direction.Right:
        #    tri = parent.make_right_subtriangle(color)
        #elif direction == Direction.Left:
        #    tri = parent.make_left_subtriangle(color)
        #elif direction == Direction.Up:
        #    tri = parent.make_top_subtriangle(color)

        #return [tri] + self.layer_sexy_triangles(tri, depth - 1)

        #color = random.choice(colors)
        if direction == Direction.Right:
            tri_side = parent.make_right_subtriangle(color)
            tri_side_subtris = self.layer_sexy_triangles(tri_side, depth - 1)
            tri_side_list = [tri_side] + tri_side_subtris 
        else:
            tri_side = parent.make_right_subtriangle(color)
            tri_side_subtris = self.layer_sexy_triangles(tri_side, depth - 1)
            tri_side_list = [tri_side] + tri_side_subtris 

        #color = random.choice(colors)
        tri_up = parent.make_right_subtriangle(color)
        tri_up_subtris = self.layer_sexy_triangles(tri_up, depth - 1)
        tri_up_list = [tri_up] + tri_up_subtris 

        return tri_side_list + tri_up_list 





base = 4096
size = (base, triangle.get_height_relative_to_base(base))


#t1 = triangle.fit_triangle_into_rect(size, blue)
#t1_image = t1.render_image(size)
#
#t2 = t1.make_right_subtriangle(white)
#t2_image = t2.render_image(size)



triangles = RecursiveTriangles(size, 10)

img = triangles.get_image()

base = 500
size = (base, triangle.get_height_relative_to_base(base))

img.thumbnail(size, Image.ANTIALIAS)
img.thumbnail(size)

#img.save("test.gif", 'gif')
img.show()
