# lib/util.py
# util.py stores the general function for checking validity of an dictionary object

def get_board_info(in_dict, board_map):
    """Check if input dictionary is a board and return board info dictionary.

    Arguments:
    in_dict - Input dictionary
    board_map - Mapping between board model and board info
    """
    if check_board(in_dict):
        BOARD_MODEL = in_dict['board']
        return board_map[BOARD_MODEL]

    return None

def check_board(in_dict):
    """ Check if input dictionary is in board foramt

    Arguments:
    in_dict - Input dictionary
    """
    return 'board' in in_dict
