from config import CONFIG

def line_a(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_b(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_c(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_d(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_e(x_start, y_start):
    return f"""
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_f(x_start, y_start):
    return f"""
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + 0.5 *  CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start}
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """


def line_g(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["DRAW_HEIGHT"]}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]}  Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        G0 Z{CONFIG["TRAVEL_HEIGHT"]}
    """