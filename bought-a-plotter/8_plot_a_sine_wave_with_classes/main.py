import math

def generate_gcode_sine_wave(y_offset, amplitude):
    gcode = []
    wavelength = 50
    feed_rate = 40000.0
    min_x = 0
    min_y = -200
    max_x = 280.0
    max_y = 0

    # Scale up to Scale down
    scale_up = 10
    scale_down = 1 / scale_up
    for step in range(20 * scale_up, 260 * scale_up, 1):
        x = step * scale_down
        # Calculate the X and Y coordinates
        y = amplitude * math.sin((2 * math.pi * x) / wavelength)
        y += y_offset

        if x > max_x or y > max_y or x < min_x or y < min_y:
            raise ValueError("too low or high", x, y)          
    
        # Generate the G-code command
        gcode.append(f"G1 X{x:.3f} Y{y:.3f} F{feed_rate}")

        if len(gcode) == 1:
            # Pen down after moving to start
            gcode.append(f"M3 S1000")
  
    # pen up before moving on
    gcode.append(f"M3 S0")
            
    return gcode

# Example usage
y_offset = -30.0
amplitude = 20.0


gcodes = []
for i in range(0,14):
    gcode = generate_gcode_sine_wave(y_offset - (i * 10), i)
    gcodes += gcode
# Write the generated G-code to a file
output_file = "output.gcode"
with open(output_file, "w") as file:
    file.write("\n".join(gcodes))

print(f"G-code written to {output_file}")