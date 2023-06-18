import matplotlib.pyplot as plt
from PIL import Image

def gcode_to_image(gcode_file, output_image):
    # Read the G-code file
    with open(gcode_file, 'r') as file:
        gcode = file.readlines()

    # Parse the G-code to extract X and Y coordinates
    x_coords = []
    y_coords = []
    for line in gcode:
        if line.startswith('G1'):
            elements = line.split()
            for element in elements:
                if element.startswith('X'):
                    x_coords.append(float(element[1:]))
                elif element.startswith('Y'):
                    y_coords.append(float(element[1:]))

    # Plot the coordinates
    plt.plot(x_coords, y_coords, 'k-')
    plt.axis('equal')
    plt.axis('off')

    # Save the plot as an image using PIL
    plt.savefig(output_image, bbox_inches='tight', pad_inches=0, transparent=True, dpi=300)
    plt.close()

    print(f"Image saved as {output_image}")

# Example usage
gcode_file = './test.gcode'
output_image = './output_image.png'
gcode_to_image(gcode_file, output_image)