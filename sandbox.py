from dxfwrite import DXFEngine as dxf
from PIL import Image


def create_dxf(filename):
    dxf_drawing = dxf.drawing(filename)

    for y in range(0,5):
        x = 0
        dxf_drawing.add(dxf.circle(radius= y, center=(x, y * 2)))
    dxf_drawing.save()

if __name__ == "__main__":
    create_dxf('./foo1.dxf')