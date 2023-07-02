import cv2 
from imutils import rotate

class Image:
    def __init__(self, filename):
        self.image = cv2.imread(filename)

    def prepare(self, should_resize=True, should_rotate=True):
        
        print('General Preparation:')
        
        [original_height, original_width, original_channels] = self.image.shape
        print(f'\t - Original size: {original_height}h by {original_width}w by {original_channels}channels')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(f'\t - Converted to Grayscale')
        
        [grayscale_height, grayscale_width] = self.image.shape
        print(f'\t - Grayscale size: {grayscale_height}h by {grayscale_width}w by 1channels')

        if should_rotate:
            self.image = rotate(self.image, 90)
            [rotated_height, rotated_width] = self.image.shape
            print(f'\t - Rotated size: {rotated_height}h by {rotated_width}w')

        if should_resize:
            self.image = should_resize(self.image, height=abs(self.y_min))
            [resized_height, resized_width] = self.image.shape
            print(f'\t - Resized size: {resized_height}h by {resized_width}w')

        return self.image
    