from PIL import Image

class RasterImage():
    """
    Description: Foo
    """

    def __init__(self, img_src):
        """Creates a new RasterImage"""
        try:
            self.img = Image.open(img_src)
        except IOError:
            print("[-] Not a valid image")
            return

        self.input_width, self.input_height = self.img.size

        self.units = ""
        while self.units not in ["in", "cm"]:
            self.units = raw_input("[+] Select project units(in or cm): ")
        self.output_width = int(raw_input('[+] Output width: '))
        self.output_height = int(raw_input('[+] Output height: '))

        if(self.input_width / self.output_width - self.input_height / self.output_height > 0.1):
            print("[!] The ratio of size from input image to output image is quite different. Consider editing first")


r = RasterImage('./src/img.jpg')