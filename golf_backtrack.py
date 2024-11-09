import sys
import math

class Object: pass

class Cell:
    pos = (0, 0) # = r, c = i
    j = 0 # index in dir/actions
    nb = 3
    nb_cur = nb - j
    dir = [0, 0, 0] # len = nb
    actions = [[], [], []] # len = nb

def pprint(str, file=sys.stderr, flush=True):
    # if 0 <= i < 100:
    if True:
        pass
        # print(str, file=sys.stderr, flush=True)
    else:
        pass

def pprint_grid():
    line = "".join(grid_2d.values())
    pprint("\n".join([line[i:i+width] for i in range(0, len(line), width)]))
    pprint("")

def i_to_pos(i):
    return i // width, i % width

def pos_to_i(r, c):
    return r * width + c

def is_ball(i):
    return "1" <= grid[i] <= "9"

def get_sym_pos(dir, r, c, n):
    if dir == 0: return ">", (r, c+n)
    if dir == 1: return "v", (r+n, c)
    if dir == 2: return "<", (r, c-n)
    if dir == 3: return "^", (r-n, c)
    pprint(f"")
    pprint(f"ERROR {dir=}")
    pprint(f"")
    return "", 0
    
def try_next(i, j):
    """
    Backtrack and try next possibility
    j = -1 means ball backtrack, so try previous ball from final move
    """
    if is_ball(i):
        pprint(f"try_next from {i=}, {j=}, {dir[i]=}")

        if j == -1:
            # start backtracking ball from final move
            j = len(dir[i]) - 1

        # find final move, needed if the ball entered hole early
        while not j in actions[i]:
            if j >= 0:
                j -= 1
            else:
                pprint(f"error, {j=}")

        # restore cells
        for cell in actions[i][j]:
            grid_2d[cell] = grid[pos_to_i(*cell)]
        actions[i].pop(j)

        # try to +1 the last non-max elem in dir[i][j], then in dir[i], then in dir
        if dir[i][j] < 3:
            # try next direction
            dir[i][j] += 1
            pprint(f"try_next to : {i=}, {j=}, {dir[i]=}")
            return i, j

        elif dir[i][j] == 3:
            # backtrack

            # restore dir
            dir[i][j] = 0

            if j > 0:
                # try same ball, prev move
                return try_next(i, j-1)
            else:
                # try prev cell
                return try_next(i-1, -1)
        
        else:
            pprint(f"try_next error {dir[i][j]=}")
        
        
    else:
        # cell is not ball, try prev cell
        return try_next(i-1, -1)

    # pprint_grid()
    # pprint(f"try_next {i=}, {j=}")
    return i, j


grid_2d = {}
# those 4 have 1d position as if the grid was a line
grid = {}
pos_dict = {}
actions = {}
dir = {}

width, height = [int(i) for i in input().split()]
for r in range(height):
    row = input()

    for c in range(width):
        grid_2d[(r, c)] = row[c]

        i = r*width + c
        grid[i] = row[c]
        pos_dict[i] = {}
        pos_dict[i][0] = (i, c)
        actions[i] = {}
        if is_ball(i):
            dir[i] = [0 for i in range(int(row[c]))]

pprint(f"start grid: ")
pprint_grid()

# bruteforce all cells, start top-left and go right then down
# try directions in this order: right, down, left, up

i = 0
j = 0
is_ok = True
nb_cur = -1
r, c = 0, 0

while i < width * height:
    if is_ball(i):
        is_ok = True
        reached_hole = False
        nb = int(grid[i])
        if j == 0:
            pos_dict[i][j] = i_to_pos(i)
        
        while is_ok and not reached_hole:
            nb_cur = nb - j
            d = dir[i][j]
            r, c = pos_dict[i][j]
            actions[i][j] = []
            
            # pprint(f"{i=} {j=} {nb=} {nb_cur=}")

            # inflight: mark the way with arrows
            for n in range(nb_cur):
                sym, pos = get_sym_pos(d, r, c, n)
                # pprint(f"{d=} {r=} {c=} {n=} {sym=} {pos=}")

                if pos in grid_2d and grid_2d[pos] in [".", "X"] or n == 0:
                    grid_2d[pos] = sym
                    actions[i][j].append(pos)
                else:
                    is_ok = False
                    pprint(f"error on the way: ")
                    pprint_grid()
                    i, j = try_next(i, j)
                    break
            
            if not is_ok:
                break
            
            # landing: mark with "F" if hole filled
            _, pos = get_sym_pos(d, r, c, nb_cur)

            if pos in grid_2d and grid_2d[pos] in [".", "H"]:
                if grid_2d[pos] == "H":
                    reached_hole = True
                    grid_2d[pos] = "F"
                    actions[i][j].append(pos)

            else:
                is_ok = False
                pprint(f"error on landing: ")
                pprint_grid()
                i, j = try_next(i, j)
                break
            
            if not reached_hole:
                has_more_moves = j < nb - 1
                if has_more_moves:
                    # next move is the next entry in dir/actions
                    j += 1
                    pos_dict[i][j] = pos
                else:
                    is_ok = False
                    pprint(f"error no hole but no more moves: ")
                    pprint_grid()
                    i, j = try_next(i, j)

            pprint_grid()

    if is_ok:
        i += 1
        j = 0

    is_ok = True

for k, v in grid_2d.items():
    if v in ["X", "F"]:
        grid_2d[k] = "."

line = "".join(grid_2d.values())
print("\n".join([line[i:i+width] for i in range(0, len(line), width)]))
