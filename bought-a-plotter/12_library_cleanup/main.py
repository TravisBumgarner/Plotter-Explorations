import cv2
import numpy as np
import shutil
import os
from math import floor

from Instructions import Instructions
from Image import Image

def bucket_pixels_evenly_by_output_colors(image, number_of_colors):
    """
    Say we have an image we want to plot with n `number_of_colors`.
    We want to ensure that each color takes up `1/n`th of the plotted image.
    This method will do that.

    Notes (Gained with plotting experience)
        - If a single color, such as white or black, takes up a large portion of the image, this algorithm won't achieve `1/n`th of the plotted image for a given color.
    

    Parameters
    ----------
    image : Mat
        Image to process
    number_of_colors : int
        

    Returns
    -------
    Mat
        Image mapped to new colors
    """

    total_pixels = image.size
    pixel_bins = [0]
    histogram,bins = np.histogram(image.ravel(),256,[0,256])
    count = 0
    for pixel_value, pixel_count in enumerate(histogram):
        if count >= total_pixels / (number_of_colors):
            count = 0
            pixel_bins.append(pixel_value)
        count += pixel_count
    # No idea why this function returns starting at value of 1 indexed. 
    # Example code shows it starting at 0 indexed.
    return np.subtract(np.digitize(image, pixel_bins), 1)


def bucket_pixels_evenly_by_grayscale_range(img, number_of_colors):
    """
    Say we have an image we want to plot with n `number_of_colors`.
    We want to ensure that each color takes up `1/n`th of the grayscale range (0 -> 255).

    Notes (Gained with plotting experience)
        - If there are 3 colors, resulting in buckets `0 -> 85`, `86 -> 170`, `171 -> 255`. If no pixels exist in a color, it won't be used to plot.

    Parameters
    ----------
    image : Mat
        Image to process
    number_of_colors : int
        

    Returns
    -------
    Mat
        Image mapped to new colors
    """

    """
    Take the range of grayscale (0 -> 255) and bucket it such that pixels/number_of_colors of the range is a bucket.
    Note - I don't prefer this method because if a color is really dark, it might end up not having
    the colors I want for highlights / whites.

    :param img: Image to process
    :param n: Number of buckets to distribute grayscale colors into
    :return: image mapped
    """
    bucket_segments = 255 / (number_of_colors - 1)
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets


def process_image(image, method, output_colors):
    if method == 'bucket_pixels_evenly_by_output_colors':
        return bucket_pixels_evenly_by_output_colors(image, number_of_colors=len(output_colors))

    if method == 'bucket_pixels_evenly_by_grayscale_range':
        return bucket_pixels_evenly_by_grayscale_range(image, number_of_colors=len(output_colors))
    
    raise ValueError("Algorithm does not exist")


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

    processed_image = process_image(image=image.prepare(should_resize=False, should_rotate=True), method='bucket_pixels_evenly_by_output_colors', output_colors=output_colors)

    horizontal_lines_algorithm(output_filename=filename, processed_image=processed_image, output_colors=output_colors, x_offset=x_offset, y_offset=y_offset)

main(
    filename='test.png',
    output_colors=[ 'red', 'gold', 'blue'],
    x_offset=50,
    y_offset=0,
)


