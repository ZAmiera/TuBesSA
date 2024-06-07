import math
from datetime import datetime

class Sudoku:
    def __init__(self):
        self.n = 0
        self.b = 0
        self.puzzle = []
        self.num_guesses = 0
        self.known_indices = []

    def load_puzzle(self, puzzle):
        self.puzzle = []
        self.known_indices = []
        self.n = len(puzzle)
        self.b = int(math.sqrt(self.n))
        for row_index, row in enumerate(puzzle):
            for col_index, c in enumerate(row):
                self.puzzle.append(c)
                if c != 0:
                    self.known_indices.append((row_index * self.n) + col_index)

    def to_string(self, pretty=True):
        lines = []
        for i in range(self.n):
            line = ' '.join(str(self.puzzle[i * self.n + j]) for j in range(self.n))
            lines.append(line)
        return "\n".join(lines)

    def __repr__(self):
        return self.to_string(pretty=False)

    def __str__(self):
        return self.to_string()

    def solve(self):
        start_time = datetime.now()
        self.num_guesses = 0
        r = self.solve_from(0, 1)
        while r is not None:
            r = self.solve_from(r[0], r[1])
        return datetime.now() - start_time

    def solve_from(self, index, starting_guess):
        if index < 0 or index >= len(self.puzzle):
            raise Exception("Invalid puzzle index %s after %s guesses" % (index, self.num_guesses))

        last_valid_guess_index = None
        found_valid_guess = False
        for i in range(index, len(self.puzzle)):
            if i not in self.known_indices:
                found_valid_guess = False
                for guess in range(starting_guess, self.n + 1):
                    self.num_guesses += 1
                    if self.valid(i, guess):
                        found_valid_guess = True
                        last_valid_guess_index = i
                        self.puzzle[i] = guess
                        break

                starting_guess = 1
                if not found_valid_guess:
                    break

        if not found_valid_guess:
            new_index = last_valid_guess_index if last_valid_guess_index is not None else index - 1
            new_starting_guess = self.puzzle[new_index] + 1
            self.reset_puzzle_at(new_index)

            while new_starting_guess > self.n or new_index in self.known_indices:
                new_index -= 1
                new_starting_guess = self.puzzle[new_index] + 1
                self.reset_puzzle_at(new_index)

            return (new_index, new_starting_guess)
        else:
            return None

    def reset_puzzle_at(self, index):
        for i in range(index, len(self.puzzle)):
            if i not in self.known_indices:
                self.puzzle[i] = 0

    def valid_for_row(self, index, guess):
        row_index = index // self.n
        start = self.n * row_index
        finish = start + self.n
        for c_index in range(start, finish):
            if c_index != index and self.puzzle[c_index] == guess:
                return False
        return True

    def valid_for_column(self, index, guess):
        col_index = index % self.n
        for r in range(self.n):
            r_index = col_index + (self.n * r)
            if r_index != index and self.puzzle[r_index] == guess:
                return False
        return True

    def valid_for_block(self, index, guess):
        row_index = index // self.n
        col_index = index % self.n

        block_row = row_index // self.b
        block_col = col_index // self.b

        row_start = block_row * self.b
        row_end = row_start + self.b
        col_start = block_col * self.b
        col_end = col_start + self.b

        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                i = c + (r * self.n)
                if self.puzzle[i] == guess:
                    return False

        return True

    def valid(self, index, guess):
        return self.valid_for_row(index, guess) and self.valid_for_column(index, guess) and self.valid_for_block(index, guess)


if __name__ == "__main__":
    import sys
    
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 7, 0, 0, 2, 0],
        [2, 0, 5, 0, 0, 0, 7, 0, 0],
        [0, 5, 0, 0, 0, 0, 3, 0, 0],
        [0, 8, 0, 3, 0, 0, 0, 7, 0],
        [3, 1, 4, 0, 0, 0, 5, 8, 9],
        [9, 2, 0, 0, 0, 8, 0, 0, 7],
        [0, 0, 3, 0, 6, 0, 0, 5, 8],
        [5, 4, 0, 0, 0, 0, 0, 9, 1]]



    sudoku = Sudoku()
    sudoku.load_puzzle(grid)
    print("\nPuzzle:\n%s" % (sudoku))

    time = sudoku.solve()
    print("\nSolution:\n%s" % (sudoku))
    print("\nNumber of guesses: %s" % (sudoku.num_guesses))
    print("Total time: %s" % (time))