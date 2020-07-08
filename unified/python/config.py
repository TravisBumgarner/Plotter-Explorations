# The amount of steps a stepper motor can turn to cover the entire width/height of the plotter.
# Calculated by:
# ((length of rail) - (thickness of rail mount) / (pi * motor diameter)) * (stepper steps per rotation)


# Paint Program
PLOTTER_WIDTH = 1800
PLOTTER_HEIGHT = 1800

# Arduino
ARDUINO_BAUD_RATE = 9600
ARDUINO_PORT = "COM11" # Run utilities/detect_ports.py to get this value.
