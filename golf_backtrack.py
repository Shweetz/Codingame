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
    if 0 <= i < 100:
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
        # pprint(f"try_next, {actions[-1]=}")

        if j == -1:
            # start backtracking ball from final move
            j = len(dir[i]) - 1

        while not j in actions[i]:
            if j >= 0:
                pprint(f"{i=}, {j=}")
                j -= 1
            else:
                pprint(f"error, {j=}")

        # restore cells
        # pprint(f"{actions[-1]=}")
        # pprint(f"{actions[i][j]=}")
        for cell in actions[i][j]:
            # pprint(f"try_next, {cell=}")
            grid_2d[cell] = grid[pos_to_i(*cell)]
        actions[i].pop(j)

        # j = len(dir[i]) - 1
        # try to +1 the last non-max elem in dir[i][j], then in dir[i], then in dir[]
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
                # try same ball, last turn
                return try_next(i, j-1)
            else:
                # try last cell
                return try_next(i-1, -1)
        
        else:
            pprint(f"try_next error {dir[i][j]=}")
        
        
    else:
        # cell is not ball, try last cell
        return try_next(i-1, -1)

    # pprint_grid()
    # pprint(f"try_next {i=}, {j=}")
    return i, j


grid = {}
grid_2d = {}
# grid = []
dir = {}
dir_e = [">", "v", "<", "^"]
states = {}
actions = {}
pos_dict = {}

width, height = [int(i) for i in input().split()]
for i in range(height):
    row = input()
    pprint(row)
    for j in range(width):
        grid[i*width + j] = row[j]
        grid_2d[(i, j)] = row[j]
        if is_ball(i*width + j):
            dir[i*width + j] = [0 for i in range(int(row[j]))]
            # actions[i*width + j] = [0 for i in range(int(row[j]))]
            pos_dict[i*width + j] = {}
            pos_dict[i*width + j][0] = (i, j)

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
j = 0
states[0] = grid.copy()
is_ok = True
nb_cur = -1
r, c = 0, 0

# for k, v in grid.items():
    # pprint(k)
    # dir[k]

while i < width * height:
    # pprint(f"{i=}")
    if is_ball(i):
        is_ok = True
        reached_hole = False
        nb = int(grid[i])
        if j == 0:
            # nb_cur = nb
            # r, c = i_to_pos(i) # restore properly when backtracking on another ball rebound
            pos_dict[i][j] = i_to_pos(i)

        while is_ok and not reached_hole:
            # j = nb - nb_cur
            nb_cur = nb - j
            pprint(f"{i=} {j=} {nb=} {nb_cur=}")
            
            d = dir[i][j]
            # actions.append([])
            if not i in actions:
                actions[i] = {}
            # pprint(f"{ actions[i]=}")
            actions[i][j] = []

            # ball movement must be perpendicular to previous one
            # if j > 0 and dir[i][j] % 2 == dir[i][j-1] % 2:
            #     try_next(i, j)
            #     is_ok = False
            #     break
            
            # if not is_ok:
            #     break

            # pprint(f"{nb_cur=}")
            # pprint(f"{d=}")
            # r, c = i_to_pos(i)
            # mark the way with arrows
            for n in range(nb_cur):
                sym, pos = get_sym_pos(d, r, c, n)
                pprint(f"{d=} {r=} {c=} {n=} {sym=} {pos=}")
                # pprint(f"1{pos=}")
                if pos in grid_2d and grid_2d[pos] in [".", "H", "X"] or n == 0:
                    # pprint(f"{sym=}")
                    grid_2d[pos] = sym
                    actions[i][j].append(pos)
                else:
                    is_ok = False
                    if pos in grid_2d:
                        pprint(f"{pos=} {grid_2d[pos]=} ")
                    pprint(f"error on the way: ")
                    pprint_grid()
                    i, j = try_next(i, j)
                    # nb_cur = nb - j
                    r, c = pos_dict[i][j]
                    break
            
            if not is_ok:
                break
            
            # mark landing with "." or "F"
            _, pos = get_sym_pos(d, r, c, nb_cur)
            land = pos_to_i(*pos)
            # pprint(f"{pos=}")
            if pos in grid_2d:
                pprint(f"land {pos=} {grid_2d[pos]=} ")

            if pos in grid_2d and grid_2d[pos] in [".", "H"]:
                # r, c = i_to_pos(land)
                r, c = pos
                # pprint(f"{(r,c)=}")
                # pprint(f"{land=}")
                # grid_2d[pos] = "."
                # pprint_grid()

                if grid[land] == "H":
                    reached_hole = True
                    grid_2d[pos] = "F"
                    actions[i][j].append(pos)

            else:
                is_ok = False
                pprint(f"error on landing: ")
                pprint_grid()
                i, j = try_next(i, j)
                r, c = pos_dict[i][j]
                pprint(f"{r=} {c=}")
                # nb_cur = nb - j
            
            # if not is_ok:
                break
            
            # next push is 1 cell less and starts from current landing
            # nb_cur -= 1
            # next push is the next entry in dir/actions
            if not reached_hole: 
                has_more_moves = j < nb - 1
                if has_more_moves:
                    j += 1
                    pos_dict[i][j] = pos
                else:
                    is_ok = False
                    pprint(f"error no hole but no more moves: ")
                    pprint_grid()
                    i, j = try_next(i, j)
                    r, c = pos_dict[i][j]

            pprint_grid()

    if is_ok:
        # pprint(f"is_ok1 {i=}")
        i += 1
        j = 0
        r, c = i_to_pos(i)
        # pprint(f"is_ok2 {i=}")

    is_ok = True

    # pprint(f"is_ok3 {i=}")
    # pprint_grid()

for k, v in grid_2d.items():
    if v in ["X", "F"]:
        grid_2d[k] = "."

line = "".join(grid_2d.values())
print("\n".join([line[i:i+width] for i in range(0, len(line), width)]))
