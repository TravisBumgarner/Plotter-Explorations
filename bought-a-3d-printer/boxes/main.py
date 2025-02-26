from gcode2dplotterart import Plotter3D
import random

X_MIN = 0
X_MAX = 170
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 2

plotter = Plotter3D(
    title="boxes",
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

LINE_WIDTH = 1.2
plotter.add_layer("black", "black", line_width=LINE_WIDTH)
# plotter.add_layer("cyan", "cyan", line_width=LINE_WIDTH)
# plotter.add_layer("magenta", "magenta", line_width=LINE_WIDTH)
# plotter.add_layer("yellow", "yellow", line_width=LINE_WIDTH)


def draw_box(start, width, height, enable_sides, layer):
    end = (start[0] + width, start[1] + height)

    if "top" in enable_sides:
        plotter.layers[layer].add_line(start[0], start[1], end[0], start[1])
    if "right" in enable_sides:
        plotter.layers[layer].add_line(end[0], start[1], end[0], end[1])
    if "bottom" in enable_sides:
        plotter.layers[layer].add_line(end[0], end[1], start[0], end[1])
    if "left" in enable_sides:
        plotter.layers[layer].add_line(start[0], end[1], start[0], start[1])


def get_random_sides():
    sides = [random.choice([True, False]) for _ in range(4)]
    return [
        "top" if sides[0] else None,
        "right" if sides[1] else None,
        "bottom" if sides[2] else None,
        "left" if sides[3] else None,
    ]


def draw_nested_boxes(x_start, y_start, width, height, spacing_per_line):
    layer = random.choice([layer for layer in plotter.layers])
    random_sides = get_random_sides()
    for i in range(0, width, spacing_per_line):
        draw_box(
            (x_start + i / 2, y_start + i / 2),
            width - i,
            height - i,
            random_sides,
            layer,
        )


def draw_grid():
    WIDTH = 10
    HEIGHT = 10
    spacing_per_line = 2
    for i in range(0, X_MAX - WIDTH, WIDTH):
        for j in range(0, Y_MAX - HEIGHT, HEIGHT):
            draw_nested_boxes(i, j, WIDTH, HEIGHT, spacing_per_line)


draw_grid()

plotter.preview()
plotter.save()
