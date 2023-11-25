from gcode2dplotterart import Plotter2D
from random import randrange, choice, randint, shuffle, random
import math

LINE_WIDTH = 1.0

COLORS = [
    {"title": "1_red1", "color": "#FF4141"},
    {"title": "2_orange1", "color": "#FF7700"},
    {"title": "3_yellow1", "color": "#FFDB11"},
    {"title": "4_green1", "color": "#A9FF00"},
    {"title": "5_green2", "color": "#00E350"},
    {"title": "6_blue1", "color": "#A2FFF8"},
    {"title": "7_blue2", "color": "#0024FF"},
    {"title": "8_blue3", "color": "#5D9DB4"},
    {"title": "9_pink1", "color": "#FF91D2"},
    {"title": "a_pink2", "color": "#FF0096"},
    {"title": "b_purple1", "color": "#EABEFF"},
    {"title": "c_purple2", "color": "#AD00FF"},
    {"title": "d_grey1", "color": "#E9E9E9"},
    {"title": "e_grey2", "color": "#B1B1B1"},
    {"title": "f_grey3", "color": "#1E1E1E"},
]

# Create a plotter object
plotter = Plotter2D(
    title="Josef Albers Homage",
    x_min=0,
    x_max=200,
    y_min=0,
    y_max=200,
    feed_rate=10000,
)

shuffle(COLORS)
color_choices = COLORS[0:3]

for color in color_choices:
    plotter.add_layer(
        title=color["title"],
        color=color["color"],
        line_width=LINE_WIDTH,
    )

x_center = (plotter.x_max - plotter.x_min) / 2
y_center = randrange(int(plotter.y_min), int(plotter.y_max))

print("center", x_center, y_center)
print("dims", plotter.width, plotter.height)

vertical_angle = math.degrees(
    math.atan(int(plotter.width / 2) / (plotter.height - y_center))
)

for color in color_choices:
    # box_side_length = randrange(1, int(plotter.width))
    box_side_length = randrange(20, 100)

    x_left_of_center = box_side_length / 2
    y_below_center = x_left_of_center / math.tan(math.radians(vertical_angle))

    x_start = x_center - x_left_of_center
    y_start = y_center - y_below_center

    x_end = x_start + box_side_length
    y_end = y_start + box_side_length

    print(x_start, x_end, y_start, y_end)

    plotter.layers[color["title"]].add_circle(x_center, y_center, radius=2)

    plotter.layers[color["title"]].add_rectangle(
        x_start=x_start, y_start=y_start, x_end=x_end, y_end=y_end
    )


plotter.preview()

plotter.save()
