import numpy as np
import cv2

X_MARKS_THE_SPOT = 'X'

def img_to_black_and_white(filename):
    img = cv2.imread(filename)
    print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale_buckets = np.rint(np.divide(img, 255))
    grayscale_buckets.astype(np.uint8)
    # print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets



def find_point(img):
    # this is square, these might accidentally be flipped. 
    [width,height] = img.shape

    # Create a place where edges will be populated.
    edges = np.array([[" " for i in range(0,width)] for j in range(0,height)])

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
            # For now, we'll just grab whichever position is value of 1 and save that in our edges array.
            
            if pixel == 1:
                edges[y_pos, x_pos] = X_MARKS_THE_SPOT
            else:
                edges[y_pos, x_pos + 1] = X_MARKS_THE_SPOT

    # Copying the code above, and transposing edges and image. Because I'm lazy.

    edges = np.transpose(edges)

    for y_pos, row in enumerate(np.transpose(img)):
        for x_pos, pixel in enumerate(row):
            if x_pos + 1 == len(row):
                # we're always making a comparison between two pixels and there's comparisons to make at the end of a row
                continue
            if pixel == row[x_pos + 1]:
                # we only care when there's a change from 0 -> 1 or 1 -> 0
                continue
            # this could probably be optimized. Like, maybe if the intersection is at (0,1) and (0,2) the output could be (0, 1.5). 
            # However, then that'd make my idea for the next step of finding the edges a bit more difficult. 
            # For now, we'll just grab whichever position is value of 1 and save that in our edges array.
            
            if pixel == 1:
                edges[y_pos, x_pos] = X_MARKS_THE_SPOT
            else:
                edges[y_pos, x_pos + 1] = X_MARKS_THE_SPOT
    
    edges = np.transpose(edges)
    for row in edges:
        print(row)

    output = []
    for y_pos, row in enumerate(edges):
        for x_pos, pixel in enumerate(row):
            if pixel == X_MARKS_THE_SPOT:
                output.append((x_pos,y_pos))
    return output

class LinkedListItem:
    def __init__(self, value):
        self.value = value
        self.next = []

    def add_next(self, value):
        self.next.append(value)

    def get_next(self):
        return self.next

def make_window(x,y):
    return [
        (x-1, y-1),
        (x-1, y),
        (x-1, y+1),
        (x, y-1),
        (x, y+1),
        (x+1, y-1),
        (x+1, y),
        (x+1, y+1)
    ]

def find_path(points):
    remaining_points = points.copy()
    
    current_point = LinkedListItem(points[0])
    points.remove(points[0])

    [x,y] = current_point.value
    window = make_window(x,y)

    for point in window:
        if point in remaining_points:
            remaining_points.remove(point)
            current_point.add_next(LinkedListItem(point))

    # I need to make this recursive -_-

    print(current_point.value)
    print([item.value for item in current_point.get_next()])

    return



def main():
    black_and_white = img_to_black_and_white('./input.png')
    print("output to bnw\n", black_and_white)
    # print("shape", black_and_white.shape)

    points = find_point(black_and_white)
    for row in points:
        print(row)

    # Eventually we'll need a find_paths function. 
    path = find_path(points)
    print(path)

main()
