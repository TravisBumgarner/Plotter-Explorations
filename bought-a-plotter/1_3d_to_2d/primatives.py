from config import CONFIG

def pen_on():
    return f"""
        M3 S1000
        G4 P0.25
    """

def pen_off():
    return f"""
        M3 S0
        G4 P0.25
    """

def line_a(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        {pen_on()}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start} 
        {pen_off()}
    """


def line_b(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start}
        {pen_on()}
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        {pen_off()}
    """


def line_c(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        {pen_on()}
        G0 X{x_start} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        {pen_off()}
    """


def line_d(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        {pen_on()}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        {pen_off()}
    """


def line_e(x_start, y_start):
    return f"""
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + CONFIG["CHARACTER_HEIGHT"]} 
        {pen_on()}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        {pen_off()}
    """


def line_f(x_start, y_start):
    return f"""
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start + 0.5 *  CONFIG["CHARACTER_HEIGHT"]} 
        {pen_on()}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]} Y{y_start}
        {pen_off()}
    """


def line_g(x_start, y_start):
    return f"""
        G0 X{x_start} Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        {pen_on()}
        G0 X{x_start + CONFIG["CHARACTER_WIDTH"]}  Y{y_start + 0.5 * CONFIG["CHARACTER_HEIGHT"]} 
        {pen_off()}
    """