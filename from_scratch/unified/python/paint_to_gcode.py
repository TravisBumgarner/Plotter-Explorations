IS_DRAWING = 0
IS_MOVING = 1

# [
#     (
#         [(724, 174), (1067, 174)],
#         [(724, 418), (1067, 418)],
#         [(724, 174), (724, 418)],
#         [(1067, 174), (1067, 418)]
#     )
# ]

# x,y,z

# 724, 174, 0 # 1 is drawing, 0 is moving
# 724, 174, 1
# 1067, 174, 1
# 1067, 174, 0


def convert_rectangles(rectangles):
    commands = []

    for rectangle in rectangles:
        for line in rectangle:
            start, end = line
            x_start, y_start = start
            x_end, y_end = end

            # Move drawing tool to start of line
            commands.append(f"{x_start},{y_start},{IS_MOVING}")
            # Touch drawing tool to surface
            commands.append(f"{x_start},{y_start},{IS_DRAWING}")
            # Move drawing tool to end of line
            commands.append(f"{x_end},{y_end},{IS_DRAWING}")
            # Touch drawing tool to traveling
            commands.append(f"{x_end},{y_end},{IS_MOVING}")
    return commands
