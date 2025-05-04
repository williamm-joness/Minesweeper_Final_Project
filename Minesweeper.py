# def play():
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
        self._calculate_hints()

    def _place_mines(self):
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.board[row][col] = '*'

    def _calculate_hints(self):
        for row in range(self.size):
            if self.board[row][col] == '*':
                continue
            count = sum((r, c) in self.mines
                for r in range(row - 1, row + 2)
                for c in range(col - 1, col + 2)
                if 0 <= r < self.size and 0 <= c < self.size)
            self.board[row][col] = str(count) if count > 0 else ' '

    