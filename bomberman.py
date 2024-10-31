import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Object: pass

def pprint(str):
    if False:
        print(str, file=sys.stderr, flush=True)

def print_entity(entity_type, owner, x, y, param_1, param_2):
    entity_str = ""
    if entity_type == 0:
        entity_str += f"player {owner} at ({x}, {y}) with {param_1} bombs of range {param_2}"

    if entity_type == 1:
        entity_str += f"bomb at ({x}, {y}) exploding in {param_1} rounds with range {param_2}"

    if entity_type == 2:
        entity_str += f"object at ({x}, {y}) wih value {param_1}"
    
    print(entity_str, file=sys.stderr, flush=True)

def dist(pos, player, acc = {}):
    if player.pos == me.pos:
        if player.pos == pos:
            return 1
        elif pos in acc:
            return len(acc[pos]) + 1
        else:
            return 100
    else:
        return abs(pos[0] - player.pos[0]) + abs(pos[1] - player.pos[1])

"""
def dfs(pos, acc, inacc):
    x, y = pos
    l = []
    for i in range(rang):
        l += [(x+1+i, y), (x-1-i, y), (x, y+1+i), (x, y-1-i)]  
    for p in l:
        if p in grid and not p in acc and not p in inacc:
            if grid[p] == ".":
                acc.add(p)
                _, acc, inacc = dfs(p, acc, inacc)
                if rang == 1:
                    # bombs don't change direction
                    _, acc, inacc = dfs(p, acc, inacc, rang)
            else:
                inacc.add(p)

    return pos, acc, inacc

def dfs(pos, acc, inacc):
    x, y = pos
    l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for p in l:
        if p in grid and not p in acc and not p in inacc:
            if grid[p] == ".":
                acc.add(p)
                _, acc, inacc = dfs(p, acc, inacc)
            else:
                inacc.add(p)

    return pos, acc, inacc
def bfs(pos):
    acc = {}
    steps = 0
    
    q = [(pos, steps)]

    while q:
        p, steps = q.pop(0)
        if p in grid and not p in acc:
            if grid[p] == "." and p not in bombs:
                acc[p] = steps
                
                x, y = p
                l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                for p in l:
                    q.append((p, steps+1))

    return acc

def bfs(pos, safe):
    """"""use steps as an int instead of a path
    """"""
    acc = {}
    steps = 0
    
    q = [(pos, steps)]
    # print(f"bfs {bombs=} {p not in bombs=} {not bombs=}", file=sys.stderr, flush=True)

    while q:
        p, steps = q.pop(0)
        # print(f"bfs {p=} {p in grid=}", file=sys.stderr, flush=True)

        if p in grid and not p in acc:
            # unexplored cell in grid
            # print(f"bfs {grid[p]=} {p not in bombs=} {not bombs=}", file=sys.stderr, flush=True)

            if p == pos:
                # my pos: 1 step because can stay here
                acc[p] = 1

                x, y = p
                l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                for p in l:
                    q.append((p, steps+1))

            elif grid[p] == "." and p not in bombs:
                # not me, wall, crate or bomb
                # cell considered inacc if explodes, in this case wait 1 round and try again
                while p in safe and steps in safe[p]:
                    steps += 1

                # if not p in safe or steps not in safe[p]:
                # no explosion
                acc[p] = steps

                x, y = p
                l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                for p in l:
                    q.append((p, steps+1))
            
            else:
                continue


    return acc
"""

def bfs(pos, safe):
    acc = {}
    # steps = 0

    q = [(pos, [])]
    # print(f"bfs {bombs=} {p not in bombs=} {not bombs=}", file=sys.stderr, flush=True)

    while q:
        # to break the outer while
        continue_q = False
    
        p, path = q.pop(0)
        # print(f"bfs {p=} {p in grid=}", file=sys.stderr, flush=True)

        if p in grid and not p in acc:
            # unexplored cell in grid
            # print(f"bfs {grid[p]=} {p not in bombs=} {not bombs=}", file=sys.stderr, flush=True)

            if p == pos:
                acc[p] = []

                # my pos: 1 step because can stay here if not inacc
                if p in safe and not dist(p, me, acc)+1 in safe[p]:
                    q.append((p, [pos]))

                x, y = p
                l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                for p2 in l:
                    q.append((p2, []))

            elif grid[p] == "." and (p not in bombs or p == pos):
                # not wall or crate or bomb (bomb placed still accessible until leaving cell)
                acc[p] = path

                # if pos == (8,8) and p == (9,8) and p in safe and p in acc:
                #     print(f"{safe[p]=}", file=sys.stderr, flush=True)
                #     print(f"{len(acc[p])=}", file=sys.stderr, flush=True)
                    
                # cell considered inacc if explodes in the number of moves to reach it
                # while p in safe and len(acc[p])+2 in safe[p]:
                while p in safe and dist(p, me, acc)+1 in safe[p]:
                    # wait 1 round: re-add the last cell in path if accessible
                    if path and path[-1] in safe and not dist(p, me, acc)+1 in safe[path[-1]]:
                        acc[p].append(path[-1])
                    else:
                        continue_q = True
                        break

                if continue_q:
                    continue

                # cell considered inacc if a player is on it with bomb available and more than 1 cell from us
                # if p in players and players[p].bomb_available and len(acc[p]) > 0:
                #     print("in", file=sys.stderr, flush=True)
                #     print(f"{players[p].bomb_available=}", file=sys.stderr, flush=True)
                #     print(f"{len(acc[p])=}", file=sys.stderr, flush=True)
                #     continue

                # cell considered inacc if a player can get to it faster than me
                # bonus: only true if he has a bomb available or will get one before i reach the cell
                for _, player in players.items():
                    # print(f"", file=sys.stderr, flush=True)
                    if dist(p, player)+1 < dist(p, me, acc) and dist(p, player) < 4:
                        print(f"{p=} {dist(p, player)=} {dist(p, me, acc)=}", file=sys.stderr, flush=True)
                        continue_q = True
                        break
                
                if continue_q:
                    continue

                # cell accessible
                if not p in acc:
                    acc[p] = []
                acc[p].append(p)

                x, y = p
                l = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                for p2 in l:
                    q.append((p2, acc[p]))
            
            else:
                continue


    return acc

def eval_bomb(safe, pos, rang, rounds_nb):
    """
    pos: bomb pos
    boom: cells that explode
    range: bomb range
    rounds_nb: rounds nb before bomb explodes (0 if bomb is just a test)
    """
    boom = set()
    boxes_nb = 0

    # bomb cell
    boom.add(pos)
    if rounds_nb != 0:
        if pos not in safe:
            safe[pos] = set()
        safe[pos].add(rounds_nb)
    
    # cells impacted by bomb
    l = [(+1, 0), (-1, 0), (0, +1), (0, -1)]
    for q in l:
        x, y = pos
        i = 1
        # print(f"{rang=}", file=sys.stderr, flush=True)
        for i in range(rang):
            # check every cell ins a direction until wall or out of range
            p = (x + q[0]*i, y + q[1] * i)
            # x += q[0]
            # y += q[1]
            if p in grid:
                if grid[p] == ".":
                    if p in bombs:
                        # bomb detonating the other: both at the earliest time
                        pass

                    # print(f"{p=}", file=sys.stderr, flush=True)
                    boom.add(p)

                    # add rounds_nb to the set of explosions on the cell
                    if rounds_nb != 0:
                        if p not in safe:
                            safe[p] = set()
                        safe[p].add(rounds_nb)
                    
                elif grid[p] in ("0", "1", "2"):
                    boxes_nb += 1
                    break
                else:
                    break

    # print(f"eval_bomb", file=sys.stderr, flush=True)
    return boxes_nb, boom, safe
"""
def update_cell_safety(safe, bomb_pos, bomb_range, bomb_rounds_nb):
    # print(f"ucs {bomb_pos=}", file=sys.stderr, flush=True)
    # print(f"ucs {safe=}", file=sys.stderr, flush=True)
    # if bomb_pos in safe.keys():
    _, boom, safe = eval_bomb(safe, bomb_pos, bomb_range, bomb_rounds_nb)
    # print(f"{boom=}", file=sys.stderr, flush=True)
        # for boom_pos in boom:
        #     if boom_pos in safe:
        #         safe.pop(boom_pos)

    # print(f"ucs {safe=}", file=sys.stderr, flush=True)
    return safe
"""
def find_safe_cells(safe, bombs):
    for k in safe:
        # safe by default
        safe[k] = set()
    
    # print(f"{safe=}", file=sys.stderr, flush=True)
    if (bombs):
        # bombs_pos = set([bomb.pos for bomb in bombs])

        # find safe cells from bomb
        # acc & bombs: bombs on accessible cells
        # print(f"bombs: {acc.keys() & bombs.keys()}", file=sys.stderr, flush=True)
        # print(acc, file=sys.stderr, flush=True)
        
        # remove bombs from safe cells
        # for bomb_pos in bombs_pos:
        #     if bomb_pos in safe:
        #         safe.pop(bomb_pos)
        # safe = safe - bombs_pos
        # print(f"{safe=}", file=sys.stderr, flush=True)
        
        # update bomb timers if chain reactions
        # for this, use a set of bombs to update: if a bomb has its rounds decreased, it is re-added to the set
        bombs_to_update = set(bombs.keys())
        # for b in bombs:
        #     bombs_to_update.add(b)

        while bombs_to_update:
            pos = bombs_to_update.pop()
            bomb = bombs[pos]
            # print(f"{pos=}", file=sys.stderr, flush=True)
            
            _, boom, _ = eval_bomb(safe, pos, bomb.range, bomb.rounds_nb)

            for p in boom:
                if p in bombs and p != pos:
                    # bomb at "pos" detonated another bomb at "p"
                    if bomb.rounds_nb < bombs[p].rounds_nb:
                        # bomb at "p" will detonate earlier, needs updating
                        print(f"{p=} {bomb.rounds_nb=} {bombs[p].rounds_nb=}", file=sys.stderr, flush=True)
                        bombs[p].rounds_nb = bomb.rounds_nb
                        bombs_to_update.add(p)


        # remove bombs explosion range from safe cells
        for pos, bomb in bombs.items():
            _, _, safe = eval_bomb(safe, pos, bomb.range, bomb.rounds_nb)

    # print(f"{safe=}", file=sys.stderr, flush=True)
    return safe

def find_best_bomb_placement(acc, safe):
    best = Object()
    best.val = 0
    best.pos = me.pos
    # print(f"1{[cell for cell in acc]=}", file=sys.stderr, flush=True)
    # a = [cell for cell in safe if safe[cell] == set()]
    # print(f"1{a}", file=sys.stderr, flush=True)
    for pos in [cell for cell in acc if not safe[cell]]:
        # for every safe cell, check bomb placement breaking most boxes and leaving safe cell
        # pos = me.pos
        # bombs.add(pos)
        # print(f"{pos=} {acc.keys()=} {safe.keys()=}", file=sys.stderr, flush=True)
        boxes_nb, boom, safe = eval_bomb(safe, pos, me.bomb_range, 0)
        # print(f"{pos=} {safe.keys()=} {boom=}", file=sys.stderr, flush=True)

        is_safe_cell_accessible = safe.keys() - boom
        if is_safe_cell_accessible:
            # value is better with more boxes
            cur_val = boxes_nb

            if cur_val > 0:
                # distance malus
                # malus = 1 if 1 bomb and  x dist
                # malus = 2 if 2 bomb and  x dist
                # malus = 2 if 1 bomb and 2x dist
                malus = dist(pos, me, acc) * me.bomb_total / 4

                cur_val = max(cur_val - malus, 0.1)
                print(f"{pos=} {cur_val=} {malus=} d={dist(pos, me, acc)} bt={me.bomb_total}", file=sys.stderr, flush=True)

            # print(f"{pos=} {safe.keys() - boom=}", file=sys.stderr, flush=True)
            if cur_val > best.val:
                # most boxes broken yet
                best.val = cur_val
                best.pos = pos

            # elif boxes_nb == best.val and pos in acc and best.pos in acc and len(acc[pos]) < len(acc[best.pos]):
            #     # same number of boxes but closer cell
            #     best.val = boxes_nb
            #     best.pos = pos
    
    return best, safe

def move_to(pos, safe):
    # pathfind to pos, find the next cell
    print(f"move_to target {pos=}", file=sys.stderr, flush=True)
    # print(f"move_to target {acc=}", file=sys.stderr, flush=True)
    if pos in acc and acc[pos]:
        print(f"death here, recalculating... {safe[pos]=}", file=sys.stderr, flush=True)
        if 2 in safe[pos]:
            for p in acc:
                if acc[p] == 1 and 2 not in safe[p]:
                    return p
        else:
            print(f"move_to {acc[pos]=}", file=sys.stderr, flush=True)
            
            # if me.pos == (0,4):
            #     return (0,4)

            return acc[pos][0]
    else:
        if 2 in safe[pos]:
            print(f"death here, recalculating... {safe[pos]=}", file=sys.stderr, flush=True)
            for p in acc:
                if len(acc[p]) == 1 and 2 not in safe[p]:
                    return p
        return pos
    
width, height, my_id = [int(i) for i in input().split()]

# game loop
while True:
    grid = {}
    players = {}
    bombs = {}
    # acc = {}
    safe = {}
    me = Object()

    # fill grid
    for i in range(height):
        row = input()
        for j, c in enumerate(row):
            grid[(i, j)] = row[j]
            # safe[(i, j)] = set()

        # print(row, file=sys.stderr, flush=True)

    # fill me.pos and bombs
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        # print_entity(entity_type, owner, x, y, param_1, param_2)

        pos = (y, x)

        if entity_type == 0:
            if owner == my_id:
                me.pos = pos
                me.bomb_available = param_1
                me.bomb_range = param_2
                # me.bomb_placed = 0
                me.bomb_total = param_1 # will add bombs placed
                me.next_bomb_in = 100 # will add my earliest exploding bomb

            else:
                player = Object()
                player.pos = pos
                player.bomb_available = param_1
                players[pos] = player

        if entity_type == 1:
            bomb = Object()
            bomb.pos = pos
            bomb.rounds_nb = param_1
            bomb.range = param_2
            bombs[pos] = bomb

            if owner == my_id:
                me.bomb_total += 1
                me.next_bomb_in = min(me.next_bomb_in, bomb.rounds_nb)

    # print("", file=sys.stderr, flush=True)

    # find unsafe cells
    safe = find_safe_cells(safe, bombs)
    # print(f"{safe=}", file=sys.stderr, flush=True)
    
    # find accessible cells
    acc = bfs(me.pos, safe)
    print(f"{len(acc)=}", file=sys.stderr, flush=True)
    # print(f"{acc=}", file=sys.stderr, flush=True)
    
    # accessible and not unsafe are safe
    for cell in acc:
        if cell not in safe:
            safe[cell] = set()
    
    # delete inaccessible cells
    for cell in safe.keys() - acc.keys():
        del safe[cell]

    # find the bomb breaking most boxes and while leaving safe cell
    best, safe = find_best_bomb_placement(acc, safe)
    print(f"{best.val=}", file=sys.stderr, flush=True)
    print(f"{best.pos=}", file=sys.stderr, flush=True)
    # print(f"{safe=}", file=sys.stderr, flush=True)

    # temp condition : only 1 bomb at a time
    # if best.val > 0 and me.bomb_available and me.pos == best.pos and not me.bomb_placed:
    if best.val > 0 and me.bomb_available and me.pos == best.pos:
        # place bomb, calculate next best bomb placement and run to it
        _, _, safe = eval_bomb(safe, me.pos, me.bomb_range, 8)
        print(f"{safe=}", file=sys.stderr, flush=True)
        best, safe = find_best_bomb_placement(acc, safe)
        print(f"{safe=}", file=sys.stderr, flush=True)
        print(f"{best.val=}", file=sys.stderr, flush=True)
        print(f"{best.pos=}", file=sys.stderr, flush=True)
        y, x = move_to(best.pos, safe)
        print(f"BOMB {x} {y}")
    elif best.pos in safe and safe[best.pos] == set():
        y, x = move_to(best.pos, safe)
        print(f"{safe=}", file=sys.stderr, flush=True)
        print(f"move best", file=sys.stderr, flush=True)
        print(f"MOVE {x} {y}")
    else:
        # find closest safe cell
        safe_cells = [pos for pos in safe if safe[pos] == set()]
        if safe_cells:
            y, x = move_to(sorted(safe_cells)[0], safe)
        else:
            # safe_cells = [pos for pos in safe if 2 not in safe[pos]]
            # if safe_cells:
            #     y, x = move_to(sorted(safe_cells)[0])
            # else:
            #     print(f"DEATH!!!!!!!!!", file=sys.stderr, flush=True)
            y, x = move_to(me.pos, safe)

        print(f"{safe=}", file=sys.stderr, flush=True)
        print(f"{sorted(safe)=}", file=sys.stderr, flush=True)
        print(f"move closest", file=sys.stderr, flush=True)
        print(f"MOVE {x} {y}")
    # if me.pos not in safe:
    #     # current cell is not safe, run to a safe cell
    #     x, y = sorted(safe)[0]
    #     print(f"not safe", file=sys.stderr, flush=True)
    #     print(f"MOVE {x} {y}")
    # else:
    #     if me.bomb_available:
    #         # safe cells exist after placing, so place bomb and run to safety
    #         if safe:
    #             x, y = best.pos
    #             print(f"safe after place, bomb val={boxes_nb}", file=sys.stderr, flush=True)
    #             print(f"BOMB {x} {y}")
    #         else:
    #             x, y = me.pos
    #             print(f"not safe after place", file=sys.stderr, flush=True)
    #             print(f"MOVE {x} {y}")
    #     else:
    #         x, y = me.pos
    #         print(f"wait for bomb available", file=sys.stderr, flush=True)
            # print(f"MOVE {x} {y}")



    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # print("BOMB 6 5")
