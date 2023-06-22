import cv2
import numpy as np
from library import Instructions
from imutils import resize

SCALE = 3

hmmm = Instructions()
IMG_RESIZE_X = int(hmmm.x_max / SCALE)
IMG_RESIZE_Y = int(abs(hmmm.y_max / SCALE))

def convert_image_to_n_grayscale_colors(img, n):
    img = cv2.imread('test5.png')
    img = resize(img, width=IMG_RESIZE_X, height=IMG_RESIZE_Y)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bucket_segments = 255 / (n - 1)
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets



OFFSET_X = 0
OFFSET_Y = 0

BUCKETS = 4

# based on assumptions of outputs being darkest to lightest. 
labels = {
    0: 'grey',
    1: 'blue',
    2: 'yellow',
    3: 'orange',
}

def main():
    instructionSets = [Instructions() for _ in range(BUCKETS)]
    instructionSets[0].add_plotting_outline(2)
    # Works with color PNGs exported from lightroom
    grayscale_buckets = convert_image_to_n_grayscale_colors('test5.png',  BUCKETS)
    print(grayscale_buckets)

    for y, row in enumerate(grayscale_buckets):
        start = [0,y]
        end = None
        value = grayscale_buckets[0][y]
        instructionSets[int(value)].add_comment(f'row {y}')

        for x, pixel in enumerate(row):
            print(x,y)
            if pixel == value:
                continue
            
            if x == 0:
                end = [x,y]
            else:
                end = [x-1,y]
            print(value, int(value))
            print(f'value {value} start {start} end {end}')
            instructionSets[int(value)].add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)
            start=[x,y]
            value = pixel
        end = [x,y]
        print(f'value {value} start {start} end {end}')
        instructionSets[int(value)].add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)

    for i in range(BUCKETS):
        instructionSets[i].print_to_file(f'output_{i}_{labels[i]}.gcode')
main()