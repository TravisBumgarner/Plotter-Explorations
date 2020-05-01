from primatives import *


def character_1(scale_factor, travel_height, draw_height, x_start, y_start):
    output = ";1"
    output += line_b(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_c(scale_factor, travel_height, draw_height, x_start, y_start)
    return output

def character_2(scale_factor, travel_height, draw_height, x_start, y_start):
    output = ";2"
    output += line_a(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_b(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_g(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_e(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_d(scale_factor, travel_height, draw_height, x_start, y_start)
    return output

def character_3(scale_factor, travel_height, draw_height, x_start, y_start):
    output = ";3"
    output += line_a(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_b(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_g(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_c(scale_factor, travel_height, draw_height, x_start, y_start)
    output += line_d(scale_factor, travel_height, draw_height, x_start, y_start)
    return output

