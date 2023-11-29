from gcode2dplotterart import Plotter2D
from random import randrange, shuffle, random
import math
from typing import Dict, List, Union
import time

print("hi")
LINE_WIDTH = 2.5

COLORS = [
    {"title": "color1", "color": "#A2FFF8"},
    {"title": "color2", "color": "#FF0096"},
    {"title": "color3", "color": "#AD00FF"},
    {"title": "DONT PLOT", "color": "#FFFFFF"},
    {"title": "color4", "color": "#E9E9E9"},
]

plotter = Plotter2D(
    title="Josef Albers Homage",
    x_min=0,
    x_max=250,
    y_min=0,
    y_max=180,
    feed_rate=10000,
)

for color in COLORS:
    plotter.add_layer(
        title=color["title"],
        color=color["color"],
        line_width=LINE_WIDTH,
    )


def josef_albers(x_min: float, y_min: float, side_length: float):
    shuffle(COLORS)

    side_padding = int(side_length * 0.2)
    x_center = x_min + side_length / 2
    y_center = randrange(
        int(y_min + side_padding), int(y_min + side_length - side_padding)
    )

    vertical_angle = math.degrees(math.atan(int(side_length / 2) / (y_center - y_min)))

    square_side_length_percentages = sorted([random() for i in range(len(COLORS))])
    print(square_side_length_percentages)
    # square_side_length_percentages = [0.2, 0.4, 0.6, 0.8, 1]
    # square_side_length_percentages = [0.2, 0.4, 0.6, 0.8, 1]

    square_side_lengths = [
        int(side_length * percentage) for percentage in square_side_length_percentages
    ]
    sorted(square_side_lengths)
    print(square_side_lengths)

    current_side_length = LINE_WIDTH
    for index, color in enumerate(COLORS):
        threshold_side_length = square_side_lengths[index]

        while current_side_length < threshold_side_length:
            x_left_of_center = current_side_length / 2
            print("xleft", x_left_of_center)
            y_below_center = x_left_of_center / math.tan(math.radians(vertical_angle))
            print("ybelow", y_below_center)
            x_start = x_center - x_left_of_center
            y_start = y_center - y_below_center

            x_end = x_start + current_side_length
            y_end = y_start + current_side_length

            print(
                "side_length",
                current_side_length,
                "x_start",
                x_start,
                "y_start",
                y_start,
                "x_end",
                x_end,
                "y_end",
                y_end,
            )

            plotter.layers[color["title"]].add_rectangle(
                x_start=x_start,
                y_start=y_start,
                x_end=x_end,
                y_end=y_end,
            )

            current_side_length += LINE_WIDTH

        # Give a little bit of spacing between color layers.
        current_side_length += LINE_WIDTH / 2


SIDE_LENGTH = 25

for x in range(0, plotter.width - SIDE_LENGTH, SIDE_LENGTH + 5):
    for y in range(0, plotter.height - SIDE_LENGTH, SIDE_LENGTH + 5):
        josef_albers(x, y, SIDE_LENGTH)

plotter.preview()
plotter.save()
