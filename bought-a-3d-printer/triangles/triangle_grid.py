from gcode2dplotterart import Plotter3D
import math

X_MIN = 0
X_MAX = 180
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

plotter = Plotter3D(
    title="Triangles",
    x_min=X_MIN,
    x_max=X_MAX,
    y_min=Y_MIN,
    y_max=Y_MAX,
    z_plotting_height=Z_PLOTTING_HEIGHT,
    z_navigation_height=Z_NAVIGATION_HEIGHT,
    feed_rate=10_000,  # Default feed rate
    output_directory="./output",
    handle_out_of_bounds="Warning",  # Warn if points are out of bounds
)

black_pen_layer = "black_pen_layer"
plotter.add_layer(black_pen_layer, color="black", line_width=0.5)
blue_pen_layer = "blue_pen_layer"
plotter.add_layer(blue_pen_layer, color="blue", line_width=0.5)


import math

def rotate_point(point, origin, angle_degrees):
    """Rotate a point around a given origin by an angle in degrees."""
    angle_radians = math.radians(angle_degrees)
    ox, oy = origin
    px, py = point
    
    # Apply 2D rotation formula
    qx = ox + (px - ox) * math.cos(angle_radians) - (py - oy) * math.sin(angle_radians)
    qy = oy + (px - ox) * math.sin(angle_radians) + (py - oy) * math.cos(angle_radians)
    
    return (qx, qy)

def draw_equilateral_triangle(origin, side_length, angle_degrees=0):
    """Generate an equilateral triangle with a given origin as center point, side length, and optional rotation."""
    x, y = origin
    h = (math.sqrt(3) / 2) * side_length  # Height of the triangle
    
    # Calculate vertices relative to center
    # Move back by half the width and down by 1/3 of the height to center the triangle
    v1 = (x - side_length/2, y - h/3)
    v2 = (x + side_length/2, y - h/3)
    v3 = (x, y + 2*h/3)

    # Rotate vertices around the origin
    v1 = rotate_point(v1, origin, angle_degrees)
    v2 = rotate_point(v2, origin, angle_degrees)
    v3 = rotate_point(v3, origin, angle_degrees)

    return [v1, v2, v3, v1]

side_length = 10.0
width = side_length
triangle_height = side_length * math.sqrt(3) / 2  # Full height of a single triangle
row_height = triangle_height  # Row spacing needs to be half the triangle height
print('height', row_height)


COUNT = 15
PADDING = 10
# X_MIN += PADDING
# X_MAX -= PADDING
# Y_MIN += PADDING
# Y_MAX -= PADDING

angle_degrees = 0
for y in range(0, COUNT):
    for x in range(0, COUNT):
        x_transform = 0
        if y % 2 == 0:
            x_transform = side_length / 2

        x_offset = side_length * x + x_transform
        origin = (X_MIN + x_offset, Y_MIN + y * row_height)
        angle_degrees = 0
        path = draw_equilateral_triangle(origin, side_length, angle_degrees)
        plotter.layers[black_pen_layer].add_path(path)
        path = draw_equilateral_triangle(origin, side_length / 2, angle_degrees)
        plotter.layers[blue_pen_layer].add_path(path)

    for x in range(0, COUNT - 1):
        x_transform = 0
        if y % 2 == 1:
            x_transform = side_length / 2

        x_offset = side_length * x + x_transform
        origin = (X_MIN + x_offset + 10, Y_MIN + y * row_height + side_length ** 0.5) 
        angle_degrees = 180
        path = draw_equilateral_triangle(origin, side_length / 2, angle_degrees)
        plotter.layers[blue_pen_layer].add_path(path)



plotter.preview()
plotter.save()

