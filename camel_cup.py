import copy
import random
import time

NUM_CAMELS = 5
NUM_SQUARES = 20
DIE_MIN = 1
DIE_MAX = 3

VERBOSITY = -1
INTERVAL = None

NUM_TRIALS = 100000

def roll_die():
    # Assume equally weighted
    return random.randint(DIE_MIN, DIE_MAX)

########################################

def get_empty_board():
    return [[] for square_index in range(NUM_SQUARES + DIE_MAX)] # Add buffer for convenience

def do_initial_roll(board):
    camels = list(range(NUM_CAMELS))
    random.shuffle(camels)
    for camel_index in camels:
        board[roll_die()].append(camel_index)

########################################

def public_service(board, camels):
    camel = random.choice(camels)
    die_result = roll_die()
    public_service_deterministic(board, camel, die_result)
    return (camel, die_result)

def public_service_deterministic(board, camel, die_result):
    for square_index in range(NUM_SQUARES):
        if camel in board[square_index]:
            carry_onward_index = board[square_index].index(camel)
            carry_onward = board[square_index][carry_onward_index:]
            remain_behind = board[square_index][:carry_onward_index]
            board[square_index] = remain_behind
            carry_from_square_index = square_index
            break
    carry_to_square_index = carry_from_square_index + die_result
    board[carry_to_square_index] += carry_onward

def play_full_game(board, verbosity = 1, interval = None):
    if verbosity >= 0:
        print_board(board, "Initial:")
    camels = list(range(NUM_CAMELS))
    roll_index = 0
    leg_index = 0
    while True:
        if interval:
            time.sleep(interval)
        if len(camels) == 0:
            # End of leg; put dice back in the pyramid
            camels = list(range(NUM_CAMELS))
            if verbosity >= 1:
                print_board(board, f"After leg {leg_index}:")
                print_standings(board)
            elif verbosity >= 0:
                print_standings(board, f"after leg {leg_index}")
            leg_index += 1
        camel, die_result = public_service(board, camels)
        if verbosity >= 2:
            print(f"~ ~ Picking from {camels}; picked {camel}; rolled {die_result} ~ ~\n")
            print_board(board, f"After roll {roll_index}:")
        camels.remove(camel)
        roll_index += 1
        if is_game_over(board):
            break
    if verbosity >= 1:
        print_board(board, "End:")
        print_standings(board)
    elif verbosity >= 0:
        print_standings(board, "end")
    return standings(board)[-1] # Winner

########################################

def print_board(board, header = None):
    if header:
        print(header)
    [print(f"{square_index:>2} : {board[square_index]}") for square_index in range(NUM_SQUARES)]
    print()

def standings(board):
    return [square_camel for square_camels in board for square_camel in square_camels]

def print_standings(board, title = None):
    if title:
        print(f"Standings {title}: {standings(board)}")
    else:
        print(f"Standings: {standings(board)}\n")

def is_game_over(board):
    for square_index in range(NUM_SQUARES, NUM_SQUARES + DIE_MAX):
        if len(board[square_index]) > 0:
            return True
    return False

########################################

def get_random_initial_board():
    board = get_empty_board()
    do_initial_roll(board)
    return board

def get_totally_random_board():
    board = get_empty_board()
    camels = list(range(NUM_CAMELS))
    random.shuffle(camels)
    for camel_index in camels:
        board[random.randint(1, NUM_SQUARES - 1)].append(camel_index)
    return board

def get_super_specific_board_of_interest():
    board = get_empty_board()
    for camel_index in range(NUM_CAMELS - 3):
        board[0].append(camel_index)
    for camel_index in range(NUM_CAMELS - 3, NUM_CAMELS):
        board[NUM_SQUARES - 3].append(camel_index)
    return board

########################################

def main_play_game_from_board(board):
    play_full_game(board, VERBOSITY, INTERVAL)

def main_get_winner_statistics_from_board(board):
    if VERBOSITY < 0:
        print_board(board, "Initial:")
    winners = dict()
    for camel_index in range(NUM_CAMELS):
        winners[camel_index] = 0
    for trials in range(NUM_TRIALS):
        winners[play_full_game(copy.deepcopy(board), VERBOSITY, INTERVAL)] += 1
    for camel_index in range(NUM_CAMELS):
        print(f"{camel_index}: {winners[camel_index] * 100.0 / NUM_TRIALS:.1f}")

########################################

if __name__ == '__main__':
    # main_play_game_from_start(get_random_initial_board())
    # main_play_game_from_board(get_totally_random_board())
    # main_play_game_from_board(get_super_specific_board_of_interest())
    # main_get_winner_statistics_from_board(get_random_initial_board())
    main_get_winner_statistics_from_board(get_totally_random_board())
    # main_get_winner_statistics_from_board(get_super_specific_board_of_interest())
