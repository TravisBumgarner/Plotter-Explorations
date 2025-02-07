# This sure pushes my understanding of geometry.

from gcode2dplotterart import Plotter3D
from random import randrange, choice, randint

COLORS = [
    {
        "title": "blue",
        "color": "#0000FF",
        "line_width": 1.0,
    },
    {
        "title": "green",
        "color": "#00FF00",
        "line_width": 1.0,
    },
    {
        "title": "red",
        "color": "#FF0000",
        "line_width": 1.0,
    },
]

X_MIN = 0
X_MAX = 200
Y_MIN = 0
Y_MAX = 200
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

# Initialize the plotter
plotter = Plotter3D(
    title="Generative Triangles",
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

for color in COLORS:
    plotter.add_layer(
        title=color["title"],
        color=color["color"],
        line_width=1.0,
    )

TRIANGLES = 20
UNIT_VECTOR_LENGTH = 10
LINES_PER_TRIANGLE = 5
SPACING_PER_TRIANGLE = 2



def calculate_slope(start, end):
    return (end[1] - start[1]) / (end[0] - start[0])

def equation_of_a_line(start, end, x):
    return calculate_slope(start, end) * (x - start[0]) + start[1]


import math

def rotate_point(x, y, angle, pivot_x=0, pivot_y=0, degrees=True):
    """Rotates a point (x, y) around a pivot (pivot_x, pivot_y) by a given angle."""
    if degrees:
        angle = math.radians(angle)  # Convert to radians if given in degrees
    
    # Translate point to origin
    x -= pivot_x
    y -= pivot_y
    
    # Apply rotation
    x_new = x * math.cos(angle) - y * math.sin(angle)
    y_new = x * math.sin(angle) + y * math.cos(angle)
    
    # Translate back
    x_new += pivot_x
    y_new += pivot_y
    
    return x_new, y_new

def rotate_line(x1, y1, x2, y2, angle, pivot_x=0, pivot_y=0, degrees=True):
    """Rotates a line defined by two points (x1, y1) and (x2, y2) around a pivot."""
    x1_new, y1_new = rotate_point(x1, y1, angle, pivot_x, pivot_y, degrees)
    x2_new, y2_new = rotate_point(x2, y2, angle, pivot_x, pivot_y, degrees)
    
    return (x1_new, y1_new), (x2_new, y2_new)


def plot_triangle(start, angle):
    end_1 = (start[0] + UNIT_VECTOR_LENGTH, start[1] + UNIT_VECTOR_LENGTH)
    end_2 = (start[0] - UNIT_VECTOR_LENGTH, start[1] + UNIT_VECTOR_LENGTH)

    start_rotated, end_1_rotated = rotate_line(start[0], start[1], end_1[0], end_1[1], angle, pivot_x=start[0], pivot_y=start[1])
    start_rotated, end_2_rotated = rotate_line(start[0], start[1], end_2[0], end_2[1], angle, pivot_x=start[0], pivot_y=start[1])

    plotter.layers['blue'].add_line(X_MIN + start_rotated[0], start_rotated[1], X_MIN + end_1_rotated[0], end_1_rotated[1])
    plotter.layers['blue'].add_line(X_MIN + start_rotated[0], start_rotated[1], X_MIN + end_2_rotated[0], end_2_rotated[1])

    for i in range(0, LINES_PER_TRIANGLE * SPACING_PER_TRIANGLE + 1, SPACING_PER_TRIANGLE):
        x1 = start_rotated[0] + i
        x2 = start_rotated[0] - i
        y1 = equation_of_a_line(start_rotated, end_1_rotated, x1)
        y2 = equation_of_a_line(start_rotated, end_2_rotated, x2)

        plotter.layers['blue'].add_line(x1, y1, x2, y2)
    return [(x1, y1)]
        

def main():
    counter = 0
    angle = 5
    points_seen = set()
    points = [(X_MAX / 2, 0)]
    while counter < TRIANGLES:
        start = points.pop(0)
        if start in points_seen:
            continue
        points_seen.add(start)
        new_points = plot_triangle(start, angle)
        points += new_points
        counter += 1
        angle += 3

main()

plotter.preview()

plotter.save()
