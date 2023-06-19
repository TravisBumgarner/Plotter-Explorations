import math

def generate_gcode_sine_wave(x_offset, y_offset, amplitude, wavelength, feed_rate, resolution, max_x, max_y):
    gcode = []

    # Calculate the number of points based on the wavelength and resolution
    num_points = int(wavelength / resolution)

    for i in range(num_points):
        # Calculate the X and Y coordinates
        x = i * resolution
        y = amplitude * math.sin((2 * math.pi * x) / wavelength)

        # Apply the offsets
        x += x_offset
        y += y_offset

        # Check if the X or Y coordinates exceed the maximum values
        if x > max_x:
            x = max_x
        if y > max_y:
            y = max_y

        # Generate the G-code command
        gcode.append(f"G1 X{x:.3f} Y{y:.3f} F{feed_rate}")

    return gcode

# Example usage
x_offset = 10.0
y_offset = 20.0
amplitude = 5.0
wavelength = 100.0
feed_rate = 100.0
resolution = 1.0
max_x = 150.0
max_y = 100.0

gcode = generate_gcode_sine_wave(x_offset, y_offset, amplitude, wavelength, feed_rate, resolution, max_x, max_y)

# Write the generated G-code to a file
output_file = "output.gcode"
with open(output_file, "w") as file:
    file.write("\n".join(gcode))

print(f"G-code written to {output_file}")