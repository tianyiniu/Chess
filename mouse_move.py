from pynput.mouse import Listener
NUM_TO_COLUMN = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

down_x = down_y = -1

def on_click(x, y, button, pressed):
    global down_x
    global down_y
    if pressed:
        (down_x, down_y) = (x, y)
    else:
        return False

def get_mouse_pos(): 
    with Listener(on_click=on_click) as listener:
        listener.join()

def is_between(num, lower, upper): 
    return lower < num and upper > num

def pos_to_board_coor(num): 
    if is_between(num, 0, 40): 
        return 1
    elif is_between(num, 40, 80): 
        return 2
    elif is_between(num, 80, 120): 
        return 3
    elif is_between(num, 120, 160): 
        return 4
    elif is_between(num, 160, 200): 
        return 5
    elif is_between(num, 200, 240): 
        return 6
    elif is_between(num, 240, 280): 
        return 7
    elif is_between(num, 280, 320): 
        return 8 
    return "INVALID"

def pos_to_square(pos):
    x_pos, y_pos = pos
    rank_num = 9 - pos_to_board_coor(y_pos)
    column = NUM_TO_COLUMN[pos_to_board_coor(x_pos)] 
    return column + str(rank_num)

def pos_to_square_black(pos):
    x_pos, y_pos = pos
    rank_num = 9 - pos_to_board_coor(y_pos)
    rank_num = 8 - (rank_num - 1)
    column_num = pos_to_board_coor(x_pos)
    column_num = (8 - column_num) + 1
    column = NUM_TO_COLUMN[column_num]
    return column + str(rank_num)

def calibrate_window(): 
    global origin_x
    global origin_y
    input("1. Move chess board window into a comfortable position and resize if needed. Press any key to continue ...\n> ")
    print("2. Click once on the top-left corner of the chess board. Do not move board afterwards.")
    # Calibrate coordinate system
    get_mouse_pos()
    origin_x, origin_y = (down_x, down_y)

def mouse_move_white(): 
    print("Your next two clicks will be recorded as selecting squares on the board.")

    # Get from-square and to-square
    get_mouse_pos()
    from_square = (down_x - origin_x, down_y - origin_y)
    print(pos_to_square(from_square))
    get_mouse_pos()
    to_square = (down_x - origin_x, down_y - origin_y)
    print(pos_to_square(to_square))

    # Calculate chess board coordinates and return move string
    return pos_to_square(from_square) + pos_to_square(to_square)

def mouse_move_black(): 
    print("Your next two clicks will be recorded as selecting squares on the board.")

    # Get from-square and to-square, NOTE: Black's board is flipped.
    get_mouse_pos()
    from_square = (down_x - origin_x, down_y - origin_y)
    print(pos_to_square_black(from_square))
    get_mouse_pos()
    to_square = (down_x - origin_x, down_y - origin_y)
    print(pos_to_square_black(to_square))

    # Calculate chess board coordinates and return move string
    return pos_to_square_black(from_square) + pos_to_square_black(to_square)

if __name__ == "__main__":
    print(mouse_move_white())