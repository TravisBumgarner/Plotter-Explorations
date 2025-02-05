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
plotter.add_layer(black_pen_layer, color="black", line_width=1.0)


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

def equilateral_triangle(origin, side_length, angle_degrees=0):
    """Generate an equilateral triangle with a given origin, side length, and optional rotation."""
    x, y = origin
    h = (math.sqrt(3) / 2) * side_length  # Height of the triangle

    # Define initial unrotated vertices
    v1 = (x, y)
    v2 = (x + side_length, y)
    v3 = (x + side_length / 2, y + h)

    # Rotate vertices around the origin
    v1 = rotate_point(v1, origin, angle_degrees)
    v2 = rotate_point(v2, origin, angle_degrees)
    v3 = rotate_point(v3, origin, angle_degrees)

    return [v1, v2, v3, v1]

# Example usage
origin = (X_MIN + 50, Y_MIN + 50)
side_length = 10
angle_degrees = 180  # Rotate counterclockwise

triangle_vertices = equilateral_triangle(origin, side_length, angle_degrees)
print(triangle_vertices)

plotter.layers[black_pen_layer].add_path(triangle_vertices)

plotter.preview()

plotter.save()