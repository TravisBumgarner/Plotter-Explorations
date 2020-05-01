from characters import *

character_map = {
    '1': character_1,
    '2': character_2,
    '3': character_3,
}



def main(input_string):
    scale_factor = 20
    travel_height = 4
    draw_height = 2.4
    x_start = 150
    y_start = 20
    x_spacing = scale_factor / 10
    y_spacing = scale_factor / 10

    print('G28')
    print(f'G0 Z{travel_height + 20}') # Tick pen on!
    print(f'G0 Z{travel_height}')
    for char in input_string:
        char_function = character_map[char]
        print(char_function(scale_factor, travel_height, draw_height, x_start, y_start))
        x_start = x_start - (x_spacing + 0.5 * scale_factor)
    print('G28')
    print(f'G0 Z{travel_height + 20}') # Tick pen off!
main('123')