from gcode2dplotterart import Plotter2D
from random import randrange, randint

NUMBER_OF_LINES = 20
LINE_WIDTH = 0.5
LAYER_1 = {"title": "pink", "color": "pink", "line_width": LINE_WIDTH}
LAYER_2 = {"title": "blue", "color": "blue", "line_width": LINE_WIDTH}
LAYER_3 = {"title": "purple", "color": "purple", "line_width": LINE_WIDTH}
LAYER_0 = {"title": "black", "color": "black", "line_width": LINE_WIDTH}

layers = [
    LAYER_0,
    LAYER_1,
    LAYER_2,
    LAYER_3,
]

plotter = Plotter2D(
    title="Lines Connecting Wandering Points",
    x_min=0,
    x_max=250,
    y_min=0,
    y_max=180,
    feed_rate=10000,
    include_comments=False,
)

for layer in layers:
    plotter.add_layer(**layer)


def generate_points():
    x_current = plotter.x_min
    # y_current = randint(plotter.y_min, plotter.y_max)
    y_current = (plotter.y_min + plotter.y_max) / 2
    points = [(x_current, y_current)]
    while True:
        # x_current = x_current + randrange(10, 40)
        x_current = x_current + plotter.width / 4
        y_current = y_current + randrange(-20, 20)

        if x_current <= plotter.x_min:
            x_current = plotter.x_min
        elif x_current >= plotter.x_max:
            x_current = plotter.x_max
        if y_current <= plotter.y_min:
            y_current = plotter.y_min
        elif y_current >= plotter.y_max:
            y_current = plotter.y_max
        points.append((x_current, y_current))

        if x_current == plotter.x_max:
            break
    return points


def do_magic(points, layer):
    plotter.layers[layer].add_path(points)

    cloned_points = points.copy()

    for _ in range(NUMBER_OF_LINES):
        new_points = []
        for index, point in enumerate(cloned_points):
            direction = 1 if randint(0, 1) == 1 else -1
            x_current = point[0]
            # if index == 0:
            #     y_current = point[1]
            # elif index == len(cloned_points) - 1:
            #     y_current = point[1]
            # else:
            y_current = point[1] + direction * 6

            if y_current <= plotter.y_min:
                y_current = plotter.y_min
            elif y_current >= plotter.y_max:
                y_current = plotter.y_max
            new_points.append((x_current, y_current))
        plotter.layers[layer].add_path(new_points)
        cloned_points = new_points


do_magic(generate_points(), "black")
do_magic(generate_points(), "pink")
do_magic(generate_points(), "blue")
do_magic(generate_points(), "purple")


# for layer in layers:


plotter.preview()
plotter.save()
