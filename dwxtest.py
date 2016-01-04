import triangle
import color
import sierpinski

from dxfwrite import DXFEngine as dxf

# if __name__ == "__main__":


base = int(4096 / 2)
size = (base, triangle.get_height_relative_to_base(base))
palet = color.get_random_sample(3)

sierpinski_triangles = sierpinski.SierpinskiTriangles(size, palet, 5)

drawing = dxf.drawing("sierpinski.dxf")

for c in palet:
    drawing.add_layer(c.name, color=c.value)
    print(c.name)

for tri in sierpinski_triangles.get_triangles():
    polyline = dxf.polyline(linetype='DOT', layer=tri.color_layer.name)
    polyline.add_vertices(tri.get_points())
    polyline.close()
    drawing.add(polyline)


drawing.save()
