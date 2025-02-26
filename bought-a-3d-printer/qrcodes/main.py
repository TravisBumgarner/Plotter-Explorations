from gcode2dplotterart import Plotter3D
from gcode2dplotterart import experimental_photo_utils
import qrcode
import qrcode.image.svg
import xml.etree.ElementTree as ET

X_MIN = 0
X_MAX = 170
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 2
MAX_WIDTH = X_MAX - X_MIN
MAX_HEIGHT = Y_MAX - Y_MIN
MAX_SIDE_LENGTH = min(MAX_WIDTH, MAX_HEIGHT)

plotter = Plotter3D(
    title="qrcode",
    x_min=X_MIN,
    x_max=X_MAX,
    y_min=Y_MIN,
    y_max=Y_MAX,
    z_plotting_height=Z_PLOTTING_HEIGHT,
    z_navigation_height=Z_NAVIGATION_HEIGHT,
    feed_rate=10_000,  # Default feed rate
    output_directory="./output",
    handle_out_of_bounds="Error",  # Warn if points are out of bounds
)

LINE_WIDTH = 1.2
plotter.add_layer('black', 'black', line_width=LINE_WIDTH)

img = qrcode.make(
      'https://travisbumgarner.github.io/gcode2dplotterart/', 
      image_factory=qrcode.image.svg.SvgImage,
      box_size=40,
      border=2,
    )
svg = img.to_string()

# Parse the SVG content
root = ET.fromstring(svg)

# Extract x, y, width, height attributes
elements = []

def draw_filled_rectangle(x_start, y_start, x_end, y_end):
    while True:     
        width = x_end - x_start
        height = y_end - y_start
        if(width < 0 or height < 0):
            break
            
        plotter.layers['black'].add_rectangle(
            x_start=x_start,
            y_start=y_start,
            x_end=x_end,
            y_end=y_end,
        )

        x_start += LINE_WIDTH * 0.5
        y_start += LINE_WIDTH * 0.5
        x_end -= LINE_WIDTH * 0.5
        y_end -= LINE_WIDTH * 0.5
        

for elem in root.iter():
    if 'x' in elem.attrib and 'y' in elem.attrib and 'width' in elem.attrib and 'height' in elem.attrib:
            x_start = X_MIN + float(elem.attrib['x'].replace('mm', ''))
            y_start = Y_MIN + float(elem.attrib['y'].replace('mm', ''))
            x_end = x_start + float(elem.attrib['width'].replace('mm', ''))
            y_end = y_start + float(elem.attrib['height'].replace('mm', ''))
            draw_filled_rectangle(x_start, y_start, x_end, y_end)

# Print the extracted elements
print(elements)

plotter.preview()
plotter.save()
