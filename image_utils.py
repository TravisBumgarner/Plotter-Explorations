from PIL import Image
from dxfwrite import DXFEngine as dxf


class RasterImage():
    """"
    Description: Foo
    """

    def __init__(self, img_src):
        """Creates a new RasterImage"""
        try:
            self.img = Image.open(img_src).convert('L') # Convert to grayscale
        except IOError:
            print('[-] Not a valid image')
            return

        self.input_width, self.input_height = self.img.size
        #
        # self.output_units = ''
        # while self.output_units not in ['in', 'cm']:
        #     self.output_units = raw_input('[>] Select project units(in or cm): ')
        #
        # self.output_width = float(raw_input('[>] Output width: '))
        # self.output_height = float(raw_input('[>] Output height: '))
        #
        # if(self.input_width / self.output_width - self.input_height / self.output_height > 0.1):
        #     print('[!] The ratio of size from input image to output image is quite different. Consider editing first')
        #
        # self.output_density = float(raw_input('[>] Output density (circles per {}: ').format(self.output_units))
        # spacing = float(raw_input('[>] Spacing between circles:'))
        # self.output_max_diameter = 1 / self.output_density - spacing / 2
        #
        self.output_units = 'in'
        self.output_width = 10
        self.output_height = 10
        self.output_density = 0.1
        self.output_max_diameter = 0.9

        self.test_img = Image.new('RGB', (5000, 5000))

        self.dxf_drawing = dxf.drawing('/Users/tbumgarner/Documents/Programming/raster_cutter/foo.dxf')

    def sample_image(self):
        """
        Sample entire area of image based on inputs.
        """

        x_sample_count = self.output_width / self.output_density
        y_sample_count = self.output_height / self.output_density

        # pps = pixels per sample
        x_pps = int(round(self.input_width / x_sample_count))
        y_pps = int(round(self.input_height / y_sample_count))

        x_start = 0
        y_start = 0

        test_img_x = 0
        test_img_y = 0

        while x_start + x_pps <= self.input_width:
            while y_start + y_pps <= self.input_height:
                luminance = self.sample_image_area(x_start, x_pps, y_start, y_pps)
                y_start += y_pps
                self.test_img.putpixel((test_img_x, test_img_y), (luminance, luminance, luminance))
                self.dxf_drawing.add(dxf.circle(radius=luminance / 2, center=(test_img_x * 255, test_img_y * 255)))
                test_img_y += 1
            y_start = 0
            x_start += x_pps
            test_img_y = 0
            test_img_x += 1

    def sample_image_area(self, x_start, x_delta, y_start, y_delta, sample_method='luminance'):
        luminance_total = 0
        for x in range(x_start, x_start + x_delta):
            for y in range(y_start, y_start + y_delta):
                luminance_total += self.img.getpixel((x, y))

        sample_area = x_delta * y_delta
        luminance_average = luminance_total / sample_area
        # print("sampling - ({}, {}) -> {}".format(x_start, y_start, luminance_average))
        return luminance_average

    def save_test_image(self, filename):
        self.test_img.save(filename)

    def save_dxf(self, filename):
        self.dxf_drawing.save()


if __name__ == '__main__':
    r = RasterImage('./src/img.jpg')
    r.sample_image()
    r.save_dxf('/Users/tbumgarner/Documents/Programming/raster_cutter/foo.dxf')

