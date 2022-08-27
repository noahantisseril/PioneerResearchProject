from z3 import *
from random import shuffle


def Sudoku_Constraints(s, groups):
    for group in groups:
        s.add(Distinct(group))
        for number in range(1, 10):
            s.add(PbEq(tuple([(var == number, 1) for var in group]), 1))


def On_Board(x, y):
    return (x >= 0) and (y >= 0) and (x < 9) and (y < 9)


if __name__ == '__main__':
    s = Solver()
    grid = [[Int(f'r_{r}_c_{c}') for c in range(1, 10)] for r in range(1, 10)]
    cells = [cell for row in grid for cell in row]
    columns = [[grid[r][c] for r in range(9)] for c in range(9)]
    box_layout = [(i, j) for i in range(3) for j in range(3)]
    boxes = [[grid[x * 3 + ix][y * 3 + iy] for (ix, iy) in box_layout] for (x, y) in box_layout]

    hyper = False
    knight = False
    king = False
    if hyper:
        hyperbox_layout = [(1, 1), (5, 1), (1, 5), (5, 5)]
        hyperboxes = [[grid[x + ix][y + iy] for (ix, iy) in box_layout] for (x, y) in hyperbox_layout]
        Sudoku_Constraints(s, hyperboxes)
    if knight:
        knight_offset = [(2, 1), (1, 2)]
        knight_offset = [(x * i, y * j) for (i, j) in knight_offset for x in [-1, 1] for y in [-1, 1]]
        s.add(And([grid[i][j] != grid[i + i_offset][j + j_offset] for i in range(9) for j in range(9) for
                   (i_offset, j_offset) in knight_offset if On_Board(i + i_offset, j + j_offset)]))
    if king:
        king_offset = [(1, 0), (1, 1)]
        king_offset = [(x * i, y * j) for (i, j) in king_offset for x in [-1, 1] for y in [-1, 1]]
        s.add(And([grid[i][j] != grid[i + i_offset][j + j_offset] for i in range(9) for j in range(9) for
                   (i_offset, j_offset) in king_offset if On_Board(i + i_offset, j + j_offset)]))


    Sudoku_Constraints(s, grid)
    Sudoku_Constraints(s, columns)
    Sudoku_Constraints(s, boxes)
    s.add(And([And(1 <= cell, cell <= 9) for cell in cells]))
    s.push()
    shuffle(cells)
    number = 1
    for cell in cells:
        while s.check(cell == number) == unsat:
            number = (number % 9) + 1
        s.add(cell == number)
    s.check()
    model = s.model()

    solution = [[model[cell] for cell in row] for row in grid]
    clues = [[model[cell] for cell in row] for row in grid]
    indices = [(i, j) for i in range(9) for j in range(9)]
    shuffle(indices)
    s.pop()

    for row in solution:
        print([cell for cell in row])

    for (i, j) in indices:
        clues[i][j] = None
        s.push()
        s.add(grid[i][j] != solution[i][j])
        s.add(And([grid[i][j] == clues[i][j] for i in range(9) for j in range(9) if clues[i][j] != None]))
        if s.check() == sat:
            clues[i][j] = solution[i][j]
        s.pop()
    print("_______")
    for row in clues:
        print("".join(["[ ]" if cell == None else f"[{cell}]" for cell in row]))
    print(len([1 for row in clues for cell in row if cell != None]))