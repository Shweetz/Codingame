import collections
from dataclasses import dataclass
import math
import random
import sys

# ----- classes

class Object: pass

class Move:
    pods_count = 0
    zone_orig = 0
    zone_dest = 0

@dataclass
class Zone:
    z_id: int = 0
    owner_id: int = 0
    my_pods: int = 0
    en_pods: int = 0
    visible: int = 0
    platinum: int = 0

    def values(self):
        return self.z_id, self.owner_id, self.my_pods, self.en_pods, self.visible, self.platinum

# ----- functions

def pprint(str, file=sys.stderr, flush=True):
    # if 0 <= i < 100:
    if True:
        pass
        print(str, file=sys.stderr, flush=True)
    else:
        pass

def pathfind(src, dst):
    """bfs with path including src and dest for easy path reversing"""
    seen = set()
    paths_to = {}
    
    q = [(src, [])]

    while q:
        p, path = q.pop(0)
        # pprint(f"{p=} {path=}")

        if not p in seen:
            seen.add(p)
            paths_to[p] = path + [p]

            if p == dst:
                pprint(f"path from {src} to {dst}={paths_to[dst]}")
                return paths_to[dst]
            
            for adj in links[p]:
                q.append((adj, path + [p]))

    return paths_to[dst]

# def find_en_base(my_base):
#     """ deduce where enemy base is, knowing that it is our base mirrored
#     enemy base must have same number of heighbors than ours, and its neighbors also must have same number of neighbors
#     """
#     # possibilities = set(range(0, zone_count))
#     not_en_base = set([my_base])
#
#     for p in zone_input.keys() - not_en_base:
#         if len(links[p]) != len(links[my_base]):
#             not_en_base.add(p)

# ----- initialization input
links = collections.defaultdict(set)
my_base = -1
en_base = -1

# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]

for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]

# zone links
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]

    links[zone_1].add(zone_2)
    links[zone_2].add(zone_1)

for link in links:
    # a pod can stay in its zone, so add zone link to itself
    links[link].add(link)

pprint(f"{my_id=} {zone_count=} {link_count=}")

# game loop
while True:
    # grab input
    zone_input = collections.defaultdict(Zone)
    # assign a value to every zone
    zone_value = collections.defaultdict(int)
    
    my_platinum = int(input())  # your available Platinum
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]

        if my_id == 0:
            my_pods = pods_p0
            en_pods = pods_p1
        else:
            my_pods = pods_p1
            en_pods = pods_p0
        
        if my_base == -1 and my_pods > 0: my_base = z_id
        if en_base == -1 and en_pods > 0: en_base = z_id
        
        # zone_input[z_id] = owner_id, my_pods, en_pods, visible, platinum
        zone_input[z_id] = Zone(z_id, owner_id, my_pods, en_pods, visible, platinum)

        # zone value
        zone_value[z_id] += platinum
        zone_value[z_id] -= zone_input[z_id].my_pods
        zone_value[z_id] += zone_input[z_id].en_pods
        if zone_input[z_id].owner_id == -1:
            zone_value[z_id] += 1

        # if zone_value[z_id] != 1:
        #     pprint(f"zone_value[{z_id}]={zone_value[z_id]}")

    # decide moves
    moves = collections.defaultdict(int)
    pprint(f"{my_base=}, {en_base=}")

    for k, v in zone_input.items():
        z_id, owner_id, my_pods, en_pods, visible, platinum = v.values()

        if my_pods == 0:
            continue

        if my_pods != 0 or platinum != 0:
            pprint(f"{my_pods=} on {z_id=} with {platinum=}")

        pprint(f"links[{z_id}]={links[z_id]}")
        pods_left = my_pods

        # pods attack enemy base
        path = pathfind(z_id, en_base)
        moves[(z_id, path[1])] += pods_left
        pods_left -= pods_left
        
        # pods defend base
        # TODO?

        # pods explore
        # spread pods in the zone to adjacent as needed
        while pods_left:
            # dict(adj_zone, value)
            adj_value = {key: zone_value[key] for key in links[z_id] if key in zone_value}
            max_adj_value = max(adj_value.values())
            # zones tied with best value
            adj_best = set(k for (k,v) in adj_value.items() if v == max_adj_value)

            if z_id == 264:
                pprint(f"{adj_value=}")
                pprint(f"{max_adj_value=}")
                pprint(f"{adj_best=}")

            # pick randomly one of adj_best to send a pod
            # todo: pick the closest to enemy base? or closest to contest zone?
            zone_dest = random.choice(list(adj_best))
            moves[(z_id, zone_dest)] += 1
            zone_value[zone_dest] -= 1
            pods_left -= 1

    # first line for movement commands
    pprint(f"{moves=}")
    if moves:
        string = ""
        # for move in moves:
        #     string += move.pods_count + " " + move.zone_orig + " " + move.zone_dest + " "
        for k, v in moves.items():
            # don't explicitely move a pod to the zone it's already in
            if k[0] != k[1]:
                string += f"{v} {k[0]} {k[1]} "
        print(string)
    else:
        print("WAIT")

    # second line no longer used (see the protocol in the statement for details)
    print("WAIT")

"""todo
remember platinum value even if zone not visible

calculate all zone distance to my base and en_base
discover all zones closer to my base
defend zones at equal distance
defend with value proportionate to enemy forces and danger (distance to base or platinum)
defend platinum or chokepoints behind platinum
"""
