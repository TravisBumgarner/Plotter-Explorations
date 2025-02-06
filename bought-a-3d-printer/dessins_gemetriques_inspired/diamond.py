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

UNIT_VECTOR_LENGTH = 10


def calculate_slope(start, end):
    return (end[1] - start[1]) / (end[0] - start[0])

def equation_of_a_line(start, end, x):
    return calculate_slope(start, end) * (x - start[0]) + start[1]


def plot_cluster(start):
    end_1 = (start[0] + UNIT_VECTOR_LENGTH, start[1] + UNIT_VECTOR_LENGTH)
    end_2 = (start[0] - UNIT_VECTOR_LENGTH, start[1] + UNIT_VECTOR_LENGTH)

    plotter.layers['blue'].add_line(X_MIN + start[0], start[1], X_MIN + end_1[0], end_1[1])
    plotter.layers['blue'].add_line(X_MIN + start[0], start[1], X_MIN + end_2[0], end_2[1])

    for i in range(0, 11, 2):
        x1 = start[0] + i
        x2 = start[0] - i
        y1 = equation_of_a_line(start, end_1, x1)
        y2 = equation_of_a_line(start, end_2, x2)

        plotter.layers['blue'].add_line(x1, y1, x2, y2)
    return [(x1, y1), (x2, y2)]
        


def main():
    counter = 0
    points_seen = set()
    points = [(X_MIN + X_MAX / 2, 0)]
    while counter < 67:
        start = points.pop(0)
        if start in points_seen:
            continue
        points_seen.add(start)
        new_points = plot_cluster(start)
        points += new_points
        counter += 1

main()

plotter.preview()

plotter.save()
