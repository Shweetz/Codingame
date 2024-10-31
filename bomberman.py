import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Object: pass

def pprint(str, file=sys.stderr, flush=True):
    if True:
        print(str, file=sys.stderr, flush=True)

def print_entity(entity_type, owner, x, y, param_1, param_2):
    entity_str = ""
    if entity_type == 0:
        entity_str += f"player {owner} at ({x}, {y}) with {param_1} bombs of range {param_2}"

    if entity_type == 1:
        entity_str += f"bomb at ({x}, {y}) exploding in {param_1} rounds with range {param_2}"

    if entity_type == 2:
        entity_str += f"object at ({x}, {y}) wih value {param_1}"
    
    pprint(entity_str)

def dist(pos, player, acc = {}):
    if player.pos == me.pos:
        if player.pos == pos:
            return 0
            # return 1
        elif pos in acc:
            
            # pprint(f"dist {pos=} {acc[pos]=}")
            return len(acc[pos])
        else:
            return 100
    else:
        return abs(pos[0] - player.pos[0]) + abs(pos[1] - player.pos[1])

def is_safe(pos, safe, path):
    # pprint(f"is_safe {pos=} r={not pos in safe or not len(path)+1 in safe[pos]}")
    return not pos in safe or not len(path)+1 in safe[pos]

def need_stop_bfs(visible, acc, inacc):
    for v in visible:
        if not v in acc and not v in inacc:
            return False
    return True

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
    # pprint(f"bfs {bombs=} {p not in bombs=} {not bombs=}")

    while q:
        p, steps = q.pop(0)
        # pprint(f"bfs {p=} {p in grid=}")

        if p in grid and not p in acc:
            # unexplored cell in grid
            # pprint(f"bfs {grid[p]=} {p not in bombs=} {not bombs=}")

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
    # visible is a cell that needs determine if accessible or not
    visible = set([pos])
    acc = {}
    inacc = set()
    q_done = set()

    # steps = 0
    # pprint(f"bfs {safe=}")
    q = [(pos, [])]
    # pprint(f"bfs {bombs=} {p not in bombs=} {not bombs=}")

    while q:
        # to break the outer while
        # continue_q = False

        if need_stop_bfs(visible, acc, inacc):
            # all shortest paths found
            break
    
        p, path = q.pop(0)

        # last_cell = path[-1] if path else (-1, -1)
        if ((p, tuple(path)) in q_done) or len(path) > 5:
            continue
        q_done.add((p, tuple(path)))
        # if path and path[0] == ((0, 11)):
        #     pprint(f"bfs {p=} {path=}")

        if p in grid:
            # unexplored cell in grid
            # pprint(f"bfs {grid[p]=} {p not in bombs=} {not bombs=}")

            is_target_reached = p == path[-1] if path else p == pos
            is_locked_by_bomb = p in bombs and (p != pos or [cell for cell in path if cell != p]) and bombs[p].rounds_nb >= len(path)
            is_cell_safe = is_safe(p, safe, path)

            if grid[p] == ".":
                # no wall or crate

                if is_cell_safe and not is_locked_by_bomb:
                    # no explosion or walking on a bomb
                    pprint(f"bfs {p=} {path}")

                    if not p in acc and is_target_reached:
                        # shortest path for p has just been found
                        acc[p] = path
                        pprint(f"bfs {p=} {acc[p]}")

                    x, y = p
                    l = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    for p2 in l:
                        q.append((p2, path + [p2]))
                        visible.add(p2)

                if not is_cell_safe:
                    pprint(f"    continue1 {p=} {visible - acc.keys() - inacc}")
                    continue
                    
                if not is_target_reached and not is_locked_by_bomb:
                    # not wall or crate or bomb (bomb placed still accessible until leaving cell)
                    # if not p in acc:
                    #     acc[p] = path
                    # pprint(f"{p=} {acc[p]=}2")

                    is_last_cell_safe = path and is_safe(path[-1], safe, path)

                    # if pos == (8,8) and p == (9,8) and p in safe and p in acc:
                    #     pprint(f"{safe[p]=}")
                    #     pprint(f"{len(acc[p])=}")
                        
                    # cell considered inacc if explodes in the number of moves to reach it
                    # while p in safe and len(acc[p])+2 in safe[p]:
                    # while p in safe and dist(p, me, acc)+1 in safe[p]:
                    #     # wait 1 round: re-add the last cell in path if accessible
                    #     if path and path[-1] in safe and not dist(p, me, acc)+1 in safe[path[-1]]:
                    #         # acc[p].append(path[-1])
                    #         q.append((p, acc[p] + p))
                    #     else:
                    #         continue_q = True
                    #         break

                    # if continue_q:
                    #     continue
                    # wait 1 round: re-add the last cell in path if accessible
                    # if not is_cell_safe and is_last_cell_safe:
                    #     acc[p].append(path[-1])
                    #     q.append((p, acc[p]))
                    #     pprint(f"    continue")
                    #     continue
                    # if is_last_cell_safe:
                    #     q.append((p, path + [path[-1]]))

                        # if not is_cell_safe:
                        #     acc[p].append(path[-1])
                    
                    
                    # cell considered inacc if a player is on it with bomb available and more than 1 cell from us
                    # if p in players and players[p].bomb_available and len(acc[p]) > 0:
                    #     pprint("in")
                    #     pprint(f"{players[p].bomb_available=}")
                    #     pprint(f"{len(acc[p])=}")
                    #     continue

                    # cell considered inacc if a player can get to it faster than me
                    # todo: only true if he has a bomb available or will get one before i reach the cell
                    # for _, player in players.items():
                    #     # pprint(f"")
                    #     if dist(p, player)+1 < dist(p, me, acc) and dist(p, player) < 4:
                    #         # pprint(f"{p=} {dist(p, player)=} {dist(p, me, acc)=}")
                    #         is_cell_safe = False
                    #         inacc.add(p)
                    #         break
                    
                    # if not is_cell_safe:
                    #     pprint(f"    continue2 {p=}")
                    #     continue

                    # cell accessible
                    # if not p in acc:
                    #     acc[p] = []
                    # acc[p].append(p)
                    # pprint(f"{p=} {acc[p]=}1")
            
            else:
                inacc.add(p)
        else:
            inacc.add(p)

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
        # pprint(f"{rang=}")
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

                    # pprint(f"{p=}")
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

    # pprint(f"eval_bomb")
    return boxes_nb, boom, safe
"""
def update_cell_safety(safe, bomb_pos, bomb_range, bomb_rounds_nb):
    # pprint(f"ucs {bomb_pos=}")
    # pprint(f"ucs {safe=}")
    # if bomb_pos in safe.keys():
    _, boom, safe = eval_bomb(safe, bomb_pos, bomb_range, bomb_rounds_nb)
    # pprint(f"{boom=}")
        # for boom_pos in boom:
        #     if boom_pos in safe:
        #         safe.pop(boom_pos)

    # pprint(f"ucs {safe=}")
    return safe
"""
def find_safe_cells(safe, bombs):
    for k in safe:
        # safe by default
        safe[k] = set()
    
    # pprint(f"{safe=}")
    if (bombs):
        # bombs_pos = set([bomb.pos for bomb in bombs])

        # find safe cells from bomb
        # acc & bombs: bombs on accessible cells
        # pprint(f"bombs: {acc.keys() & bombs.keys()}")
        # pprint(acc)
        
        # remove bombs from safe cells
        # for bomb_pos in bombs_pos:
        #     if bomb_pos in safe:
        #         safe.pop(bomb_pos)
        # safe = safe - bombs_pos
        # pprint(f"{safe=}")
        
        # update bomb timers if chain reactions
        # for this, use a set of bombs to update: if a bomb has its rounds decreased, it is re-added to the set
        bombs_to_update = set(bombs.keys())
        # for b in bombs:
        #     bombs_to_update.add(b)

        while bombs_to_update:
            pos = bombs_to_update.pop()
            bomb = bombs[pos]
            # pprint(f"{pos=}")
            
            _, boom, _ = eval_bomb(safe, pos, bomb.range, bomb.rounds_nb)

            for p in boom:
                if p in bombs and p != pos:
                    # bomb at "pos" detonated another bomb at "p"
                    if bomb.rounds_nb < bombs[p].rounds_nb:
                        # bomb at "p" will detonate earlier, needs updating
                        pprint(f"{p=} {bomb.rounds_nb=} {bombs[p].rounds_nb=}")
                        bombs[p].rounds_nb = bomb.rounds_nb
                        bombs_to_update.add(p)


        # remove bombs explosion range from safe cells
        for pos, bomb in bombs.items():
            _, _, safe = eval_bomb(safe, pos, bomb.range, bomb.rounds_nb)

    # pprint(f"{safe=}")
    return safe

def find_best_bomb_placement(acc, safe):
    best = Object()
    best.val = 0
    best.pos = me.pos
    # pprint(f"1{[cell for cell in acc]=}")
    # a = [cell for cell in safe if safe[cell] == set()]
    for cell, path in acc.items():
        pprint(f"{cell} {path}")
        
    for pos in [cell for cell in acc if not safe[cell]]:
        # for every safe cell, check bomb placement breaking most boxes and leaving safe cell
        # pos = me.pos
        # bombs.add(pos)
        # pprint(f"{pos=} {acc.keys()=} {safe.keys()=}")
        boxes_nb, boom, safe = eval_bomb(safe, pos, me.bomb_range, 0)
        # pprint(f"{pos=} {safe.keys()=} {boom=}")

        safe_cells = safe.keys() - boom
        is_safe_cell_accessible = [cell for cell in safe_cells if len(acc[cell]) < 8]
        if is_safe_cell_accessible:
            # pprint(f"{pos=} safe={safe.keys() - boom}")

            # value is better with more boxes
            cur_val = boxes_nb

            if cur_val > 0:
                # distance malus = dist * rounds / x
                # - malus = 1 if 1 bomb and 4 dist
                # - malus = 2 if 2 bomb and 4 dist
                # - malus = 2 if 1 bomb and 8 dist
                # - malus = 1 if 1 bomb and 6 dist but 2 rounds until next bomb
                # distance is reduced by rounds until next bomb
                malus_dist = max(dist(pos, me, acc) - me.next_bomb_in, 0)
                malus = malus_dist * me.bomb_available / 4

                cur_val = max(cur_val - malus, 0.1)
                # pprint(f"{pos=} {cur_val=} {malus=} d={dist(pos, me, acc)} bt={me.bomb_total}")
                # if dist(pos, me, acc) != len(acc[pos]):
                #     pprint(f"aaaaaaaaaaaaaaaa d={dist(pos, me, acc)} d2={len(acc[pos])}")
                

            # pprint(f"{pos=} {safe.keys() - boom=}")
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
    pprint(f"move_to target {pos=}")
    # pprint(f"move_to target {acc=}")
    if pos in acc and acc[pos]:
        if 2 in safe[pos]:
            pprint(f"death1 here, recalculating... {safe[pos]=}")
            for p in acc:
                if acc[p] == 1 and 2 not in safe[p]:
                    return p
        else:
            pprint(f"move_to {acc[pos]=}")
            
            # if me.pos == (0,4):
            #     return (0,4)

            return acc[pos][0]
    else:
        if 2 in safe[pos]:
            pprint(f"death2 here, recalculating... {safe[pos]=}")
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

        # pprint(row)

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
                if me.bomb_available:
                    me.next_bomb_in = 0
                else:
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

    # pprint("")

    # find unsafe cells
    safe = find_safe_cells(safe, bombs)
    # pprint(f"{safe=}")
    
    # find accessible cells
    acc = bfs(me.pos, safe)
    pprint(f"{len(acc)=}")
    # pprint(f"{acc=}")
    
    # accessible and not unsafe are safe
    for cell in acc:
        if cell not in safe:
            safe[cell] = set()
    
    # delete inaccessible cells
    for cell in safe.keys() - acc.keys():
        del safe[cell]

    # find the bomb breaking most boxes and while leaving safe cell
    best, safe = find_best_bomb_placement(acc, safe)
    pprint(f"{best.val=}")
    pprint(f"{best.pos=}")
    # pprint(f"{safe=}")

    # temp condition : only 1 bomb at a time
    # if best.val > 0 and me.bomb_available and me.pos == best.pos and not me.bomb_placed:
    if best.val > 0 and me.bomb_available and me.pos == best.pos:
        # place bomb, calculate next best bomb placement and run to it
        _, _, safe = eval_bomb(safe, me.pos, me.bomb_range, 8)
        pprint(f"{safe=}")
        best, safe = find_best_bomb_placement(acc, safe)
        pprint(f"{safe=}")
        pprint(f"{best.val=}")
        pprint(f"{best.pos=}")
        y, x = move_to(best.pos, safe)
        print(f"BOMB {x} {y}")
    elif best.pos in safe and safe[best.pos] == set():
        y, x = move_to(best.pos, safe)
        pprint(f"{safe=}")
        pprint(f"move best")
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
            #     pprint(f"DEATH!!!!!!!!!")
            y, x = move_to(me.pos, safe)

        pprint(f"{safe=}")
        pprint(f"{sorted(safe)=}")
        pprint(f"move closest")
        print(f"MOVE {x} {y}")
    # if me.pos not in safe:
    #     # current cell is not safe, run to a safe cell
    #     x, y = sorted(safe)[0]
    #     pprint(f"not safe")
    #     pprint(f"MOVE {x} {y}")
    # else:
    #     if me.bomb_available:
    #         # safe cells exist after placing, so place bomb and run to safety
    #         if safe:
    #             x, y = best.pos
    #             pprint(f"safe after place, bomb val={boxes_nb}")
    #             pprint(f"BOMB {x} {y}")
    #         else:
    #             x, y = me.pos
    #             pprint(f"not safe after place")
    #             pprint(f"MOVE {x} {y}")
    #     else:
    #         x, y = me.pos
    #         pprint(f"wait for bomb available")
            # pprint(f"MOVE {x} {y}")



    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # print("BOMB 6 5")
