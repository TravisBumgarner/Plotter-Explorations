from primatives import line_a, line_b, line_c, line_d, line_e, line_f, line_g

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
    'a': 'abcfeg',
    'b': 'fegcd',
    'c': 'afed',
    'd': 'gedcb',
    'e': 'afged',
    'f': 'afged',
    'g': 'afedc',
    'h': 'fgec',
    'i': 'fe',
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


def draw_character(character_to_draw, scale_factor, travel_height, draw_height, x_start, y_start):
    output = f';{character_to_draw}'
    primatives = character_map[character_to_draw] 
    for primative in primatives: 
        draw_primative = primative_map[primative]
        output += draw_primative(scale_factor, travel_height, draw_height, x_start, y_start)
    return output

def main(input_string):
    sanitized_input = [char.lower() for char in input_string]
    input_character_set = set(sanitized_input)
    valid_character_set = set(character_map.keys())
    if not input_character_set.issubset(valid_character_set):
        invalid_chararacters = input_character_set.difference(valid_character_set)
        raise Exception(f"Invalid character(s) supplied: {(', ').join(invalid_chararacters)}")        


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
    for character_to_draw in sanitized_input:
        print(draw_character(character_to_draw, scale_factor, travel_height, draw_height, x_start, y_start))
        x_start = x_start - (x_spacing + 0.5 * scale_factor)
    print('G28')
    print(f'G0 Z{travel_height + 20}') # Tick pen off!
main('Hello World')