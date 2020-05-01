def line_a(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        G0 Z{draw_height}
        G0 X{x_start + 0.5 * scale_factor} Y{y_start} 
        G0 Z{travel_height}
    """


def line_b(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        G0 Z{draw_height}
        G0 X{x_start} Y{y_start + 0.5 * scale_factor} 
        G0 Z{travel_height}
    """


def line_c(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * scale_factor} 
        G0 Z{draw_height}
        G0 X{x_start} Y{y_start + 1 * scale_factor} 
        G0 Z{travel_height}
    """


def line_d(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 1 * scale_factor} 
        G0 Z{draw_height}
        G0 X{x_start + 0.5 * scale_factor} Y{y_start + 1 * scale_factor} 
        G0 Z{travel_height}
    """


def line_e(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start + 0.5 * scale_factor} Y{y_start +  1 * scale_factor} 
        G0 Z{draw_height}
        G0 X{x_start + 0.5 * scale_factor} Y{y_start + 0.5 * scale_factor} 
        G0 Z{travel_height}
    """


def line_f(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start + 0.5 * scale_factor} Y{y_start + 0.5 * scale_factor} 
        G0 Z{draw_height}
        G0 X{x_start + 0.5 * scale_factor} Y{y_start}
        G0 Z{travel_height}
    """


def line_g(scale_factor, travel_height, draw_height, x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * scale_factor} 
        G0 Z{draw_height}
        G0 X{x_start + 0.5 * scale_factor}  Y{y_start + 0.5 * scale_factor} 
        G0 Z{travel_height}
    """