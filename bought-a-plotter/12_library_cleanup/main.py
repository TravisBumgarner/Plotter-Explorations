import cv2
import numpy as np
import shutil
import os
from math import floor

from Instructions import Instructions
from Image import Image


def horizontal_lines_algorithm(output_filename, processed_image, output_colors, x_offset, y_offset):
    buckets = len(output_colors)
    instruction_sets = [Instructions(units="mm", x_min = 0, x_max = 280, y_min = -200, y_max = 0, feed_rate=10000, should_outline=i==0) for i in range(buckets)]
    
    # Ignore every other row when plotting. 
    PLOT_EVERY_NTH_ROW = 2

    # Y-Axis is upside down.
    INVERT = -1
    
    for y, row in enumerate(processed_image):
        y = INVERT * y

        if y % PLOT_EVERY_NTH_ROW == 0: 
            continue

        x_start = 0
        y_start = y
        x_end = None
        y_end = None
        
        value = processed_image[0][y]
        instruction_sets[int(value)].add_comment(f'row {y}')

        for x, pixel in enumerate(row):
            if pixel == value:
                continue
            
            x_end = x
            y_end = y

            instruction_sets[int(value)].add_line(
                x_offset + x_start,
                y_offset + y_start,
                x_offset + x_end,
                y_offset + y_end
            )

            x_start = x
            y_start = y

            value = pixel
        x_end = x
        y_end = y

        instruction_sets[int(value)].add_line(
            x_offset + x_start,
            y_offset + y_start,
            x_offset + x_end,
            y_offset + y_end
        )

    for i in range(buckets):
        instruction_sets[i].print_to_file(f'./output/{output_filename}_{i}_{output_colors[i]}.gcode')

def folder_setup():
    shutil.rmtree('./output')
    os.mkdir('./output')

def main(filename, output_colors, x_offset, y_offset):
    folder_setup()

    image = Image(filename)
    image.prepare_for_bucket_algorithm(should_resize=False, should_rotate=True)
    image.apply_bucket_algorithm(method='bucket_pixels_evenly_by_output_colors', output_colors=output_colors)

    horizontal_lines_algorithm(output_filename=filename, processed_image=image.image, output_colors=output_colors, x_offset=x_offset, y_offset=y_offset)

main(
    filename='test.png',
    output_colors=[ 'red', 'gold', 'blue'],
    x_offset=75,
    y_offset=0,
)


