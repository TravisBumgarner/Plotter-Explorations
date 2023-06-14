from datetime import datetime
import os

from primatives import line_a, line_b, line_c, line_d, line_e, line_f, line_g, pen_off, pen_on
from config import CONFIG

character_map = {
    '1': 'bc',
    '2': 'abged',
    '3': 'abgcd',
    '4': 'fgbc',
    '5': 'afgcd',
    '6': 'afgedc',
    '7': 'abc',
    '8': 'abcdefg',
    '9': 'abcdfg',
    '0': 'abcdef',
    'a': 'abgedc',
    'b': 'fegcd',
    'c': 'afed',
    'd': 'gedcb',
    'e': 'afged',
    'f': 'afge',
    'g': 'afedc',
    'h': 'fgec',
    'i': 'ea',
    'j': 'bcde',
    'k': 'afegc',
    'l': 'fed',
    'm': 'aec',
    'n': 'feabc',
    'o': 'abcdef',
    'p': 'abgfe',
    'q': 'afbgc',
    'r': 'bafe',
    's': 'afgcd',
    't': 'fegd',
    'u': 'fedcb',
    'v': 'fbcd',
    'w': 'fbd',
    'x': 'fgbec',
    'y': 'fgbcd',
    'z': 'abgd',
    '-': 'g',
    '_': 'd',
    ' ': ''
}

primative_map = {
    'a': line_a,
    'b': line_b,
    'c': line_c,
    'd': line_d,
    'e': line_e,
    'f': line_f,
    'g': line_g
}


def draw_character(character_to_draw, x_start, y_start):
    output = f';{character_to_draw}'
    primatives = character_map[character_to_draw] 
    for primative in primatives: 
        draw_primative = primative_map[primative]
        output += draw_primative(x_start, y_start)
    return output

def validate_input(sanitized_input):
    input_character_set = set(sanitized_input)
    valid_character_set = set(character_map.keys())
    if not input_character_set.issubset(valid_character_set):
        invalid_chararacters = input_character_set.difference(valid_character_set)
        raise Exception(f"Invalid character(s) supplied: {(', ').join(invalid_chararacters)}") 



def main(input_string):
    sanitized_input = [char.lower() for char in input_string]    
    validate_input(sanitized_input)

    x_start = CONFIG["X_MIN"]
    y_start = CONFIG["Y_MIN"]
    x_period = (CONFIG["X_SPACING"] + CONFIG["CHARACTER_WIDTH"])
    y_period = (CONFIG["Y_SPACING"] + CONFIG["CHARACTER_HEIGHT"])

    output = ''

    output += '        F10000\n' # Set Feed rate
    output += '        G90\n' # Set unites absolute
    output += '        G28\n' # Set units mm
    output += pen_off()
    output += '        G21\n' # Go Home
    
    for character_to_draw in sanitized_input:
        if(x_start - x_period) < CONFIG["X_MAX"]:
            x_start = CONFIG["X_MIN"]
            y_start += y_period

        if y_start > CONFIG["Y_MAX"]:
            raise Exception('Exceeded printing bed')
        
        output += draw_character(character_to_draw, x_start, y_start)
        output += '\n'
        x_start = x_start - x_period
    output += pen_off()
    output += 'G28\n'
    
    filename = f'{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.gcode'
    filepath = os.path.join(os.path.abspath(""), "output") 
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(os.path.join(filepath, filename), 'w') as f:
        f.write(output)
main('hi sam')