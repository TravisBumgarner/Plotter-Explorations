import cv2
import numpy as np

def convert_image_to_n_grayscale_colors(img, n = 3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bucket_segments = 255 / n
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    return grayscale_buckets

def main():
    img = cv2.imread('test.png')
    grayscale_buckets = convert_image_to_n_grayscale_colors(img)
    print(grayscale_buckets)

    for y, row in enumerate(grayscale_buckets):
        start = [0,y]
        end = None
        value = grayscale_buckets[0][y]

        for x, pixel in enumerate(row):
            if pixel == value:
                continue
            end = [x-1,y]
            print(f'value {value} start {start} end {end}')
            start=[x,y]
            value = pixel
        end = [x,y]
        print(f'value {value} start {start} end {end}')

       

main()