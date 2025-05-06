# 1) create the board, plant the bombs randomly
# 2) display the board, ask user where they want to dig
# 3) if location is a bomb, end game/ show game over
# 4) if location is safe, reveal number underneath
# 5) repeat steps 2-4 until either
#   a) there are no more squares that aren't bombs
#   b) user hits a bomb
# 6) if a), display you win

import random

class Minesweeper:
    def __init__(self, size=8, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        # 2D list, where ' ' is a placeholder for either a bomb or a number
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        # another 2D list, this time to track what user has revealed. False = not revealed. Cells are automatically false unless the player chooses to reveal, in which case they are true
        self.mines = set()
        # a set is like a list, but has no duplicates
        self._place_mines()
        # mine setting function
        self._calculate_hints()
        # numerical hint setting function

    def _place_mines(self):
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.board[row][col] = '*'

    def _calculate_hints(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == '*':
                    continue
                count = sum((r, c) in self.mines
                    for r in range(row - 1, row + 2)
                    for c in range(col - 1, col + 2)
                    if 0 <= r < self.size and 0 <= c < self.size)
                self.board[row][col] = str(count) if count > 0 else ' '

    def display(self):
        print("   " + " ".join(map(str, range(self.size))))
        # prints the numbers for the columns on top
        for idx, row in enumerate(self.revealed):
            row_display = [self.board[idx][j] if row[j] else '#' for j in range(self.size)]
            print(f"{idx:2} " + " ".join(row_display))

    def reveal(self, row, col):
        # row and col are substitued for user input values (see 'def play_game()')
        if self.revealed[row][col]:
            return True
        # if it's already revealed, do nothing
        self.revealed[row][col] = True
        # reveal the cell
        if self.board[row][col] == '*':
            return False
        # returning False means the game ends (see 'def play_game():')
        if self.board[row][col] == ' ':
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.size and 0 <= c < self.size:
                        if not self.revealed[r][c]:
                            self.reveal(r, c)
                            # this last line triggers recursive reveal
        return True

    def is_won(self):
        for row in range(self.size):
            for col in range(self.size):
                if not self.revealed[row][col] and (row, col) not in self.mines:
                    return False
        return True

def play_game():
    game = Minesweeper()
    while True:
        game.display()
        try:
            # try statement will run something, unless there is an exception
            row = int(input("Enter row: "))
            col = int(input("Enter column: "))
        except ValueError:
            # here's the first exception
            print("Invalid input - Please enter numbers")
            continue
        if not (0 <= row < game.size and 0 <= col < game.size):
            # here's the second exception. 
            print("Out of bounds")
            continue
        if not game.reveal(row, col):
            # essentially says "if game.reveal(row, col) == false"
            print("Game over")
            game.revealed = [[True for _ in range(game.size)] for _ in range(game.size)]
            game.display()
            break
        if game.is_won():
            game.display()
            print("You win")
            break

play_game()