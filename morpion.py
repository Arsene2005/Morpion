import random

def display_grid(grid):
    """
    Displays the game grid with a frame and symbols in red.
    """
    size = len(grid)
    
    # Display the top line of the frame
    print("┌" + "───┬" * (size - 1) + "───┐")

    for i, row in enumerate(grid):
        symbols = []
        for symbol in row:
            if symbol == "X":
                symbols.append("\033[91mX\033[0m")  # Red for symbol X
            elif symbol == "O":
                symbols.append("\033[91mO\033[0m")  # Red for symbol O
            else:
                symbols.append(symbol)
        print("│ " + " | ".join(symbols) + " │")

        # Display intermediate horizontal lines except for the last line
        if i < size - 1:
            print("├" + "───┼" * (size - 1) + "───┤")
    
    # Display the bottom line of the frame
    print("└" + "───┴" * (size - 1) + "───┘")


def create_grid(size):
    """
    Creates a game grid of the specified size.
    """
    return [["-" for _ in range(size)] for _ in range(size)]

def place_piece(grid, row, column, symbol):
    """
    Places a piece at the specified location if it is empty.
    """
    if grid[row][column] == "-":
        grid[row][column] = symbol
        return True
    else:
        return False

def is_winner(grid, symbol):
    """
    Checks if the player with the specified symbol has won.
    """
    size = len(grid)
    for i in range(size):
        if all(grid[i][j] == symbol for j in range(size)) or \
           all(grid[j][i] == symbol for j in range(size)) or \
           all(grid[i][i] == symbol for i in range(size)) or \
           all(grid[i][size - i - 1] == symbol for i in range(size)):
            return True
    return False

def is_draw(grid):
    """
    Checks if the grid is full and no player has won.
    """
    return all(cell != "-" for row in grid for cell in row)

def choose_winning_move(grid, symbol):
    """
    Chooses a winning move if available.
    """
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == "-":
                grid[i][j] = symbol
                if is_winner(grid, symbol):
                    grid[i][j] = "-"
                    return i, j
                grid[i][j] = "-"
    return None

def choose_blocking_move(grid, symbol, opponent):
    """
    Chooses a move to block the opponent if they are about to win.
    """
    return choose_winning_move(grid, opponent)

def choose_random_move(grid):
    """
    Chooses a random move among available moves.
    """
    available_moves = [(i, j) for i in range(len(grid)) for j in range(len(grid)) if grid[i][j] == "-"]
    return random.choice(available_moves)

def play_game(size=3):
    """
    Main function to play the game.
    """
    grid = create_grid(size)
    symbols = ["X", "O"]
    random.shuffle(symbols)
    print("Player", symbols[0], "starts.")

    for turn in range(size * size):
        display_grid(grid)
        symbol = symbols[turn % 2]
        print("It's", symbol, "'s turn")

        if symbol == "X":
            while True:
                try:
                    row = int(input("Enter the row number: "))
                    column = int(input("Enter the column number: "))
                    if 0 <= row < size and 0 <= column < size:
                        if place_piece(grid, row, column, symbol):
                            break
                        else:
                            print("This cell is already occupied, please choose another one.")
                    else:
                        print("The coordinates entered are out of the grid, please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            move = choose_winning_move(grid, symbol)
            if move is None:
                move = choose_blocking_move(grid, symbol, symbols[0])
            if move is None:
                row, column = choose_random_move(grid)
            else:
                row, column = move
            place_piece(grid, row, column, symbol)

        if is_winner(grid, symbol):
            display_grid(grid)
            print("Player", symbol, "wins!")
            return True

        if is_draw(grid):
            display_grid(grid)
            print("Draw!")
            return False

    display_grid(grid)
    print("End of the game.")

if __name__ == "__main__":
    while True:
        size = int(input("Enter the grid size (3 or more): "))
        if size >= 3:
            if play_game(size):
                choice = input("Do you want to play again? (Y/N): ")
                if choice.lower() != 'y':
                    break
            else:
                choice = input("Do you want to play again? (Y/N): ")
                if choice.lower() != 'y':
                    break
        else:
            print("The grid size must be at least 3.")
