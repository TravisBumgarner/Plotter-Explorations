import numpy as np
import cv2

def img_to_black_and_white(filename):
    img = cv2.imread(filename)
    print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale_buckets = np.rint(np.divide(img, 255))
    grayscale_buckets.astype(np.uint8)
    # print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets



def find_edges(img):
    # this is square, these might accidentally be flipped. 
    [width,height] = img.shape

    # Create a place where edges will be populated.
    edges = np.array([[0 for i in range(0,width)] for j in range(0,height)])

    for y_pos, row in enumerate(img):
        for x_pos, pixel in enumerate(row):
            if x_pos + 1 == len(row):
                # we're always making a comparison between two pixels and there's comparisons to make at the end of a row
                continue
            if pixel == row[x_pos + 1]:
                # we only care when there's a change from 0 -> 1 or 1 -> 0
                continue
            # this could probably be optimized. Like, maybe if the intersection is at (0,1) and (0,2) the output could be (0, 1.5). 
            # However, then that'd make my idea for the next step of finding the edges a bit more difficult. 
            # For now, we'll just grab whichever position is value of 1 and save that in our edges aray.
            
            if pixel == 1:
                edges[y_pos, x_pos] = 1
            else:
                edges[y_pos, x_pos + 1] = 1
    
    return edges







    return edges


def main():
    black_and_white = img_to_black_and_white('./input.png')
    print("output to bnw\n", black_and_white)
    # print("shape", black_and_white.shape)

    edges = find_edges(black_and_white)
    for row in edges:
        print(row)


main()