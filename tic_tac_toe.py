import random
import os

BOARD_SIZE = "choose"
USER_MARKER = 'X'
COMPUTER_MARKER = 'O'
MAX_SCORE = 3
FIRST_MOVE = "choose"

def prompt(message):
    """Format interactive messages that prompt the user for input."""
    print(f'==> {message}')

def get_valid_user_input(error_message, valid_options):
    """Keep prompting the user for input until finding a match in the given 
    options. Return bool: True if input is in options, False if not."""
    while True:
        answer = input().strip().lower()
        if answer in valid_options:
            break
        prompt(error_message)
    return answer

def choose_board_size():
    """Prompt the user to choose a BOARD_SIZE if it's set to "choose". Return
    the board size."""
    if BOARD_SIZE == "choose":
        prompt('First, let\'s choose a board size: Enter "3" for 3x3, "5" for '
               '5x5, or "9" for 9x9.')
        options = ['3', '5', '9']
        error_message = 'Invalid input. Please enter "3", "5", or "9".'
        answer = get_valid_user_input(error_message, options)
        match answer:
            case '3':
                return 3
            case '5':
                return 5
            case '9':
                return 9
    return BOARD_SIZE

def get_winning_length(board_size):
    """Return the winning length corresponding to the board size."""
    if board_size == 5:
        return 4
    elif board_size == 9:
        return 5
    else:
        return 3

def determine_first_player():
    """Return the player to make the first move if FIRST_MOVE is set to 
    "choose"."""
    if FIRST_MOVE == "choose":
        prompt('Who will go first? Enter "u" for user, or "c" for computer.')
        options = ['u', 'c', 'user', 'computer']
        error_message = 'Invalid input. Please enter "u" or "c".'
        if get_valid_user_input(error_message, options) in ['u', 'user']:
            return "User"
        else:
            return "Computer"
    return FIRST_MOVE

def initialize_board(board_size):
    """Create the game board and fill the squares with numbers corresponding 
    to the board size."""
    square_nums = [str(num) for num in range(1, board_size ** 2 + 1)]
    board = [square_nums[i:i + board_size] 
            for i in range(0, len(square_nums), board_size)]
    return board

def display_board(board, board_size):
    """Print the game board that dynamically adjusts to the board size."""
    print(f'Your move is marked by "{USER_MARKER}". '
          f'Computer move is marked by "{COMPUTER_MARKER}".\n')
    
    horizontal_separator = '-----' + '+-----' * (board_size - 1)
    vertical_separator = '     |' * (board_size - 1)

    print(vertical_separator)
    if board_size == 3:
        for i in range(board_size):
            print('  ' + '  |  '.join(board[i]))
            if i < board_size - 1:
                print(vertical_separator)
                print(horizontal_separator)
                print(vertical_separator)
    elif board_size == 5:
        for i in range(board_size):
            if i == 0:
                print('  ' + '  |  '.join(board[i]))
            elif i == 1:
                print(
                    '  ' + '  |  '.join(board[i][:-1]) + '  | ' + board[i][-1])
            else:
                print(' ' + '  | '.join(board[i]))
            if i < board_size - 1:
                print(vertical_separator)
                print(horizontal_separator)
                print(vertical_separator)
    else:
        for i in range(board_size):
            if i == 0:
                print('  ' + '  |  '.join(board[i]))
            else:
                print(' ' + '  | '.join(board[i]))
            if i < board_size - 1:
                print(vertical_separator)
                print(horizontal_separator)
                print(vertical_separator)
    print(vertical_separator)
    print('')

def empty_squares(board, board_size):
    """Return a list of numbers displayed on the unoccupied squares."""
    return [board[row][column] for row in range(board_size)
            for column in range(board_size)
            if board[row][column].isdigit()]

def join_or(lst, separator=', ', word="or"):
    """Join a list of elements using the specified separator and word."""
    if len(lst) == 0:
        return ''
    elif len(lst) == 1:
        return str(lst[0])
    elif len(lst) == 2:
        return f'{lst[0]} {word} {lst[1]}'

    leading_items = separator.join(str(el) for el in lst[:-1])
    return f'{leading_items}{separator}{word} {lst[-1]}'

def get_square(num, board_size):
    """Return the indices of the specified square in a 2-D array as a tuple."""
    squares = [(row, column) for row in range(board_size)
                for column in range(board_size)]
    return squares[num - 1]
    
def get_winning_lines_marks(board, board_size, winning_length):
    """Return a list of marks on each winning line on the current board."""
    winning_lines = []
    for row in range(board_size):
        for col in range (board_size - winning_length + 1):
            winning_lines.append(
                [board[row][col + i] for i in range(winning_length)])

    for col in range(board_size):
        for row in range(board_size - winning_length + 1):
            winning_lines.append(
                [board[row + i][col] for i in range(winning_length)])
    
    for row in range(board_size - winning_length + 1):
        for col in range(board_size - winning_length + 1):
            winning_lines.append([board[row + i][col + i] 
                                  for i in range(winning_length)])
    
    for row in range(board_size - winning_length + 1):
        for col in range(winning_length - 1, board_size):
            winning_lines.append([board[row + i][col - i] 
                                  for i in range(winning_length)])
    
    return winning_lines

def find_square_to_win_or_block(board, board_size, winning_length, mark):
    """Return the number of the first winning or at-risk square found, 
    or None if none is found."""
    winning_lines = get_winning_lines_marks(board, board_size, winning_length)
    for line in winning_lines:
        if line.count(mark) + line.count(' ' + mark) == winning_length - 1:
            for square in line:
                if square.isdigit():
                    return int(square)
    return None

def get_center_square(board, board_size):
    """Return the number of the center square or None if occupied."""
    center_idx = (board_size - 1) // 2
    if board[center_idx][center_idx].isdigit():
        return (board_size ** 2 + 1) // 2
    else:
        return None

def pad_marker_to_display(mark, length):
    """Pad the user/computer marker with a space to the left if the number of 
    its square has two digits."""
    if length == 2:
        return ' ' + mark
    else:
        return mark

def unpad_marker(mark):
    """Return the user/computer marker in the unpadded format."""
    if len(mark) == 2:
        return mark.strip()
    else:
        return mark
    
def computer_move(board, board_size, winning_length):
    """Computer makes a move according to the following strategy: Mark a 
    winning square if one is found; if not, mark an at-risk square if one is
    found; if not, mark the board center if it's unoccupied; if none of the 
    above moves is available, randomly mark an unoccupied square. Return the
    number of the chosen square."""
    if empty_squares(board, board_size) == []:
        return
    square_to_win = find_square_to_win_or_block(
        board, board_size, winning_length, COMPUTER_MARKER)
    square_to_block = find_square_to_win_or_block(
        board, board_size, winning_length, USER_MARKER)
    center_square = get_center_square(board, board_size)

    if square_to_win:
        row, square = get_square(square_to_win, board_size)
        computer_square = square_to_win
        mark_length = len(str(square_to_win))
    elif square_to_block:
        row, square = get_square(square_to_block, board_size)
        computer_square = square_to_block
        mark_length = len(str(square_to_block))
    elif get_center_square(board, board_size):
        row = square = (board_size - 1) // 2
        computer_square = center_square
    else:
        computer_square = random.choice(
            [int(num) for num in empty_squares(board, board_size)])
        row, square = get_square(computer_square, board_size)
         
    mark_length = len(str(computer_square))  
    board[row][square] = pad_marker_to_display(COMPUTER_MARKER, mark_length)
    return computer_square

def user_move(board, board_size):
    """Mark an occupied square chosen by the user. Return the number of the 
    chosen square."""
    valid_choices = empty_squares(board, board_size)
    prompt("Your turn: Choose one of the following empty squares: "
           f'{join_or(valid_choices)}')
    error_message = (f"Invalid input. Please enter one of the following "
                    f"numbers: {join_or(valid_choices)}")
    square_num = get_valid_user_input(error_message, valid_choices)
    user_square = int(square_num)
    mark_length = len(square_num)
    row, column = get_square(user_square, board_size)
    board[row][column] = pad_marker_to_display(USER_MARKER, mark_length)
    return user_square

def take_turn(
        board, board_size, winning_length, current_player, last_computer_move):
    """The current player makes a move. If the current player is the user, 
    display a message about the last computer move. Return a message that 
    documents the current move made by the current player."""
    if current_player == "User":
        print(last_computer_move)
        user_marked = user_move(board, board_size)
        message = f"User has marked square {user_marked}."
    else:
        computer_marked = computer_move(board, board_size, winning_length)
        message = f"Computer has marked square {computer_marked}."
    return message
    
def alternate_player(current_player):
    """Set the current player to the user and the computer alternatively and 
    return the current player."""
    if current_player == "User":
        return "Computer"
    else:
        return "User"

def update_scores(user_score, computer_score, winner):
    """Increment the score of the round winner by one and return the updated 
    user score and computer score."""
    if winner == "User":
        user_score += 1
    elif winner == "Computer":
        computer_score += 1
    return user_score, computer_score

def board_full(board, board_size):
    """Check if the current board is full. Return bool: True if the board is 
    full, False if not."""
    return empty_squares(board, board_size) == []

def detect_game_winner(board, board_size, winning_length):
    """Check if a winner occurs. Return the winner or None."""
    for line in get_winning_lines_marks(board, board_size, winning_length):
        if all([unpad_marker(mark) == USER_MARKER for mark in line]):
            return "User"
        elif all([unpad_marker(mark) == COMPUTER_MARKER for mark in line]):
            return "Computer"
    return None

def play_a_round(round, board_size, winning_length, current_player, 
                 user_score, computer_score, last_computer_move=''):
    """Play a round of the game until a winner occurs or the board is full. 
    Return the current round number, user score, and computer score."""
    winner = None
    board = initialize_board(board_size)
    round += 1

    while (not detect_game_winner(board, board_size, winning_length) and 
           not board_full(board, board_size)):
        os.system('clear')
        print(f'========== Round {round} ==========\n')
        display_board(board, board_size)
        message = take_turn(board, board_size, winning_length, current_player, 
                            last_computer_move)
        if current_player == "Computer":
            last_computer_move = message
        current_player = alternate_player(current_player)

    os.system('clear')
    print(f'========== Round {round} ==========\n')
    display_board(board, board_size)

    winner = detect_game_winner(board, board_size, winning_length)
    if winner:
        prompt(f"{winner} won!")
        user_score, computer_score = update_scores(
            user_score, computer_score, winner)
    else:
        prompt("It's a tie!")
    return round, user_score, computer_score

def display_game_score(user_score, computer_score):
    """Display the updated match score after each round."""
    if user_score > computer_score:
        prompt(f"User leads {user_score} - {computer_score}.")
    elif user_score < computer_score:
        prompt(f"Computer leads {computer_score} - {user_score}.")
    else:
        prompt(f"{user_score} - {computer_score} draw.")

def detect_match_winner(user_score, computer_score):
    """Check if a match winner occurs. Return the match winner or None."""
    if user_score == MAX_SCORE:
        return "User"
    elif computer_score == MAX_SCORE:
        return "Computer"
    else:
        return None

def play_again():
    """Check if the user wants to play another match and validate the user 
    input. Return bool: True if 'yes' to another match, False if 'no'."""
    prompt("Would you like to play again? (y/n)")
    options = ['y', 'n', 'yes', 'no']
    error_message = 'Invalid input. Please enter "y" or "n".'
    if get_valid_user_input(error_message, options) == 'y':
        return True
    else:
        return False

def play_tic_tac_toe():
    """Main program to play the Tic Tac Toe."""
    os.system('clear')
    print("========== Welcome to Tic Tac Toe! ==========\n")
    print("Play Tic Tac Toe against the computer on different board sizes.\n\n"
          "The first player to mark a winning length of squares in a row -- "
          "horizontally, vertically, or diagonally -- wins. The winning "
          "length is 3 for the 3x3 board, 4 for the 5x5 board, and 5 for the "
          "9x9 board.\n\nIf all squares are marked and neither player has "
          "reached the winning length in a row, the game ends in a tie. The "
          "first player who wins three rounds will become the grand winner.\n")
    prompt('Press "Enter" to continue.')
    input()

    keep_playing = True
    while keep_playing:
        os.system('clear')
        round, user_score, computer_score = 0, 0, 0
        board_size = choose_board_size()
        winning_length = get_winning_length(board_size)
        current_player = determine_first_player()

        while not detect_match_winner(user_score, computer_score):
            round, user_score, computer_score = play_a_round(
                round, board_size, winning_length, current_player, 
                user_score, computer_score, last_computer_move='')
            
            if user_score < MAX_SCORE and computer_score < MAX_SCORE:
                display_game_score(user_score, computer_score)
                prompt('Press "Enter" to start the next round.')
                input()

        if detect_match_winner(user_score, computer_score) == "User":
            print("Congratulations! You won this match!")
        else:
            print("The match is over. Computer won.")

        if not play_again():
            keep_playing = False
    
    print("Thank you for playing Tic Tac Toe!")

play_tic_tac_toe()