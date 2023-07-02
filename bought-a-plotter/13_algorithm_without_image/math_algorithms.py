"""
Algorithms more heavily based in plotting points, lines, curves, etc. with mathematical equations.
"""
from Instructions import Instructions
from Plotter import Plotter
from random import random, randint

def wander(plotter: Plotter, filename_prefix, output_colors, x_offset, y_offset):
    border_preview = Instructions(plotter, use_for_preview_only=True)
    """
    Take in 4 colors, wander outward from the center. Each color will wander towards a different quadrant of the X and Y axis.
    """

    if len(output_colors) != 4:
        raise Exception('wander algorithm requires 4 colors')

    
    quadrants_polarity = [
        [1, 1],
        [-1, 1],
        [-1, -1],
        [1, -1],
    ]

    for i in range(len(output_colors)):
        instructions = Instructions(plotter)

        current_point_x = plotter.x_max / 2
        current_point_y = plotter.y_min / 2
        
        while True:
            previous_point_x = current_point_x
            previous_point_y = current_point_y

            # Pick whether to walk in the positive / negative direction. Prefer walking towards the quadrant limit.
            # For example, Quadrant I will prefer to walk in the positive X and positive Y direction.
            x_polarity = quadrants_polarity[i][0] if random() < 0.6 else -1 * quadrants_polarity[i][0]
            y_polarity = quadrants_polarity[i][1] if random() < 0.6 else -1 * quadrants_polarity[i][1]
            
            current_point_x = randint(0, 10) * x_polarity + previous_point_x
            current_point_y = randint(0, 10) * y_polarity + previous_point_y

            # Keep walking until collision with the wall.
            if (
                current_point_x > plotter.x_max
                or current_point_x < plotter.x_min
                or current_point_y > plotter.y_max
                or current_point_y < plotter.y_min
            ):
                break
            
            instructions.add_line(previous_point_x, previous_point_y, current_point_x, current_point_y)
            border_preview.add_line(previous_point_x, previous_point_y, current_point_x, current_point_y)

        instructions.print_to_file(f'./output/{filename_prefix}_{i}_{output_colors[i]}.gcode')
    border_preview.print_to_file(f'./output/preview.gcode')
