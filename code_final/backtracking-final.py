import time
from datetime import datetime

def print_grid(arr):
    for i in range(9):
        for j in range(9):
            print(arr[i][j], end=" ")
        print()

def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if(arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False

def used_in_col(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False

def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if(arr[i + row][j + col] == num):
                return True
    return False

def check_location_is_safe(arr, row, col, num):
    return (not used_in_row(arr, row, num) and
            not used_in_col(arr, col, num) and
            not used_in_box(arr, row - row % 3, col - col % 3, num))

def solve_sudoku(arr):
    global num_guesses   
    l = [0, 0]
    
    
    if(not find_empty_location(arr, l)):
        return True
    
    row = l[0]
    col = l[1]
    
    # consider digits 1 to 9
    for num in range(1, 10): 
        num_guesses += 1
        
        
        if(check_location_is_safe(arr, row, col, num)):
            
            arr[row][col] = num

           
            if(solve_sudoku(arr)):
                return True

            
            arr[row][col] = 0
            
    
    return False


if __name__ == "__main__":
    
    grid = [[0 for x in range(9)] for y in range(9)]
    
    # memasukkan grid sesuai clue yang diinginkan (bisa diubah sesuai tingkat kesulitan yang diinginkan)
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 7, 0, 0, 2, 0],
        [2, 0, 5, 0, 0, 0, 7, 0, 0],
        [0, 5, 0, 0, 0, 0, 3, 0, 0],
        [0, 8, 0, 3, 0, 0, 0, 7, 0],
        [3, 1, 4, 0, 0, 0, 5, 8, 9],
        [9, 2, 0, 0, 0, 8, 0, 0, 7],
        [0, 0, 3, 0, 6, 0, 0, 5, 8],
        [5, 4, 0, 0, 0, 0, 0, 9, 1]]
    
    num_guesses = 0  # inisialisasi guess counter
    
    start_time = datetime.now()

    print("Puzzle")
    print_grid(grid)
    print("")
    # kalau ketemu, print grid
    if(solve_sudoku(grid)):
        print("Solution")
        print_grid(grid)
        print("\nNumber of guesses: %d" % num_guesses)
        print("Total time: %s seconds" % (datetime.now() - start_time))
    else:
        print("No solution exists")