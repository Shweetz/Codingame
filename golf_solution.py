import sys
from itertools import product

W, H = [int(i) for i in input().split()]
N = W * H
grid = "".join(input() for i in range(H)) # format 2d grid in a 1d line

#Find all balls and holes
balls = set(j for j in range(N) if grid[j].isdigit())
holes = set(j for j in range(N) if grid[j] == "H")
        
#Find all paths each ball might take.
paths = []
for b in balls:
    shots = int(grid[b])
    for directions in product((-W, -1, 1, W), repeat = shots):  # N, W, E, S | W/-W means changing line in 2d grid
        path = [b]
        for distance in range(shots,0,-1):
            dir = directions[shots-distance]
            start = path[-1]
            inflight = [start + dir * s for s in range(1, distance)]
            finish = start + dir * distance
            
            if finish < 0 or finish >= N: break # land out of grid
            if dir in (-1,1) and (finish // W != start // W): break # land on different line when going west or east
            if grid[finish] not in ".H": break # land on obstacle
            if finish in path: break # land on visited tile
            if (balls | holes).intersection(inflight): break # fly over ball/hole

            path += inflight + [finish]
            if finish in holes:
                if path not in paths:
                    paths += [path]        
                break

#Holes or balls which have a unique path get it added to the answer list.
#Any paths that overlap this path are removed.
#Holes and balls with multiple path options may still all have common cells that other holes and balls cannot use.
answer = []
while paths:
    for x in (balls | holes):
        xpaths = [p for p in paths if x in p]
        if len(xpaths) == 1:
            definite = xpaths[0]
            answer += [definite]
            paths = [p for p in paths if not set(definite).intersection(p)]
        elif len(xpaths) > 1:
            xpathsets = [set(xp) for xp in xpaths]
            xcommoncells = set.intersection(*xpathsets)
            paths = [p for p in paths if x in p or not xcommoncells.intersection(p)]

#Calculate output 1d line.
output = ["."] * N
for a in answer:
    for i in range(len(a)-1):
        dir = a[i+1] - a[i]
        output[a[i]] = {-W:"^", -1:"<", 1:">", W:"v"}[dir]

#Format 1dline in 2d grid
for ii in range(H):
    print("".join(output[ii*W:(ii+1)*W]))
	