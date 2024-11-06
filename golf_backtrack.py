import sys
import math

class Object: pass

class Cell:
    pos = (0, 0)
    dir = 0

def pprint(str, file=sys.stderr, flush=True):
    if True:
        pass
        print(str, file=sys.stderr, flush=True)
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

def i_to_dir_list(i, length):
    dir_list = []

    remain = i
    for _ in range(length):
        dir, remain = i // 4, i % 4
        dir_list.append(dir)
        i = i // 4

    return dir_list

def is_ball(i):
    return "1" <= grid[i] <= "9"

def get_sym_pos(dir, r, c, n):
    if dir == 0: return ">", (r, c+n)
    if dir == 1: return "v", (r+n, c)
    if dir == 2: return "<", (r, c-n)
    if dir == 3: return "^", (r-n, c)
    return "", 0
    
def try_next(i, j):
    pprint(f"try_next from {i=}, {j=}, {dir[i]=}")

    if is_ball(i):
        # pprint(f"try_next, {actions[-1]=}")
        # restore cells
        for cell in actions[-1]:
            # pprint(f"try_next, {cell=}")
            grid_2d[cell] = grid[pos_to_i(*cell)]
        actions.pop()

        # j = len(dir[i]) - 1
        # try to +1 the last non-max elem in dir[i][j], then in dir[i], then in dir[]
        if dir[i][j] < 4:
            # try next direction
            dir[i][j] += 1

        elif dir[i][j] == 4:
            # backtrack

            # restore dir
            dir[i][j] = 0

            if j > 0:
                # try same ball, last turn
                try_next(i, j-1)
            else:
                # try last cell
                try_next(i, 0)
    else:
        # cell is not ball, try last cell
        try_next(i, 0)

    pprint(f"try_next to : {i=}, {j=}, {dir[i]=}")
    pprint_grid()


grid = {}
grid_2d = {}
# grid = []
dir = {}
dir_e = [">", "v", "<", "^"]
states = {}
actions = []

width, height = [int(i) for i in input().split()]
for i in range(height):
    row = input()
    pprint(row)
    for j in range(width):
        grid[i*width + j] = row[j]
        grid_2d[(i, j)] = row[j]
        if is_ball(i*width + j):
            dir[i*width + j] = [0 for i in range(int(row[j]))]

pprint("")

# pprint(grid)

# bruteforce all cells, start top-left and go right then down
# try directions in this order: right, down, left, up

# for row in grid:
#     for c in row:

# cell_order = sorted(grid.keys())
# for cell in cell_order:
#     print(cell)

i = 0
states[0] = grid.copy()
is_ok = True

# for k, v in grid.items():
    # pprint(k)
    # dir[k]

while i < width * height:
    pprint(f"{i=}")
    if is_ball(i):
        is_ok = True
        reached_hole = False
        nb = int(grid[i])
        nb_cur = nb
        r, c = i_to_pos(i)

        while is_ok and not reached_hole:
            actions.append([])

            j = nb - nb_cur
            d = dir[i][j]

            # ball movement must be perpendicular to previous one
            if j > 0 and dir[i][j] % 2 == dir[i][j-1] % 2:
                try_next(i, j)
                is_ok = False
                break
            
            # if not is_ok:
            #     break

            pprint(f"{nb_cur=}")
            pprint(f"{d=}")
            # r, c = i_to_pos(i)
            # mark the way with arrows
            for n in range(nb_cur):
                pprint(f"{n=}")
                sym, pos = get_sym_pos(d, r, c, n)
                pprint(f"1{pos=}")
                if grid_2d[pos] in [".", "H", "X"] or n == 0:
                    pprint(f"{sym=}")
                    grid_2d[pos] = sym
                    actions[-1].append(pos)
                else:
                    is_ok = False
                    pprint_grid()
                    pprint(f"error on the way: ")
                    try_next(i, j)
                    break
            
            if not is_ok:
                break
            
            # mark landing with "." or "F"
            _, pos = get_sym_pos(d, r, c, nb_cur)
            land = pos_to_i(*pos)
            pprint(f"{pos=}")

            if pos in grid_2d and grid_2d[pos] in [".", "H"]:
                r, c = i_to_pos(land)
                # pprint(f"{(r,c)=}")
                # pprint(f"{land=}")
                grid_2d[(r, c)] = "."
                pprint_grid()

                if grid[land] == "H":
                    reached_hole = True
                    grid_2d[(r, c)] = "F"

            else:
                is_ok = False
                pprint(f"error on landing: ")
                pprint_grid()
                try_next(i, j)
            
            # if not is_ok:
                break
            
            # next push is 1 cell less and starts from current landing
            nb_cur -= 1
            # r, c = 

            pprint_grid()

    if is_ok:
        i += 1
    is_ok = True

    pprint_grid()

for k, v in grid_2d.items():
    if v in ["X", "F"]:
        grid_2d[k] = "."

line = "".join(grid_2d.values())
print("\n".join([line[i:i+width] for i in range(0, len(line), width)]))


"""







"""
