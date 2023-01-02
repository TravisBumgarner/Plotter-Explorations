# The amount of steps a stepper motor can turn to cover the entire width/height of the plotter.
# Calculated by:
# ((length of rail) - (thickness of rail mount) / (pi * motor diameter)) * (stepper steps per rotation)


# Paint Program
PLOTTER_WIDTH = 400  # should be 1800 for me
PLOTTER_HEIGHT = 400  # should be 1800 for me

# Arduino
ARDUINO_BAUD_RATE = 9600
ARDUINO_PORT = "COM4"  # Run utilities/detect_ports.py to get this value.
