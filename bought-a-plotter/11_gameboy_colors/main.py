import cv2
import numpy as np
from library import Instructions
from imutils import resize
from math import floor

# I could probably not have me hit the bounds of the plotter with some better math.
# Oh well. For now, this mess.
# need to some point account for offsets better with large prints.
SCALE = 3
magic_number = 5
hmmm = Instructions()
OFFSET_X = 0
OFFSET_Y = 0
IMG_RESIZE_X = floor(hmmm.x_max / SCALE) - OFFSET_X - magic_number
IMG_RESIZE_Y = floor(abs(hmmm.y_min / SCALE)) - OFFSET_Y - magic_number

print("??", IMG_RESIZE_X, IMG_RESIZE_Y)



BUCKETS = 4

labels = {
    0: 'grey',
    1: 'pink',
    2: 'purple',
    3: 'blue',
}


def evenly_distribute_pixels_per_color(img, n):
    """
    Ensures that each color has the same number of pixels.

    :param img: Image to process
    :param n: Number of buckets to distribute pixels into
    :return: image mapped
    """
    total_pixels = img.size
    pixel_bins = [0]
    histogram,bins = np.histogram(img.ravel(),256,[0,256])
    count = 0
    for pixel_value, pixel_count in enumerate(histogram):
        if count >= total_pixels / (n):
            count = 0
            pixel_bins.append(pixel_value)
        count += pixel_count
    # No idea why this function returns starting at value of 1 indexed. 
    # Example code shows it starting at 0 indexed.
    return np.subtract(np.digitize(img, pixel_bins), 1)

def evenly_distribute_pixels_per_nth_percent_of_grayscale_range(img, n):
    """
    Take the range of grayscale (0 -> 255) and bucket it such that n% of the range is a bucket.
    Note - I don't prefer this method because if a color is really dark, it might end up not having
    the colors I want for highlights / whites.

    :param img: Image to process
    :param n: Number of buckets to distribute grayscale colors into
    :return: image mapped
    """
    bucket_segments = 255 / (n - 1)
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets

   
def convert_image_to_n_grayscale_colors(filename, n):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    [width, height] = img.shape

    # Not sure if the next lines are actually correct for all aspect ratios.
    if width > height:
        img = resize(img, width=IMG_RESIZE_X)
    if width <= height:
        img = resize(img, width=IMG_RESIZE_X)

    print('resized to ', img.shape)
    img = evenly_distribute_pixels_per_color(img, BUCKETS)
    return img


def main():
    filename="otter2.png"
    instructionSets = [Instructions() for _ in range(BUCKETS)]
    instructionSets[0].add_plotting_outline(2)
    # Works with color PNGs exported from lightroom
    grayscale_buckets = convert_image_to_n_grayscale_colors(filename,  BUCKETS)
    print(grayscale_buckets)
    print(grayscale_buckets.shape)
    for y, row in enumerate(grayscale_buckets):
        start = [0,y]
        end = None
        value = grayscale_buckets[0][y]
        instructionSets[int(value)].add_comment(f'row {y}')

        for x, pixel in enumerate(row):
            if pixel == value:
                continue
            
            end = [x,y]
            # print(start, end)
            instructionSets[int(value)].add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)
            start=[x,y]
            value = pixel
        end = [x,y]
        instructionSets[int(value)].add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)

    for i in range(BUCKETS):
        instructionSets[i].print_to_file(f'./output/output_{filename}_{i}_{labels[i]}.gcode')

main()