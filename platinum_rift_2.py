import collections
import math
import random
import sys

class Object: pass

class Move:
    pods_count = 0
    zone_orig = 0
    zone_dest = 0 

def pprint(str, file=sys.stderr, flush=True):
    # if 0 <= i < 100:
    if True:
        pass
    else:
        print(str, file=sys.stderr, flush=True)
        pass

# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]

for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]

links = collections.defaultdict(set)
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]

    links[zone_1].add(zone_2)
    links[zone_2].add(zone_1)

pprint(f"{my_id=} {zone_count=} {link_count=}")

# game loop
while True:
    zone_value = {}
    moves = collections.defaultdict(int)
    
    my_platinum = int(input())  # your available Platinum
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]

        my_pods, en_pods = (pods_p0, pods_p1) if my_id == 0 else (pods_p1, pods_p0)

        if my_pods == 0:
            continue

        if my_pods != 0 or platinum != 0:
            pprint(f"{my_pods=} on {z_id=} with {platinum=}")
        
        pprint(f"{links[z_id]=}")
        # zone value for adjacent zones
        for adj in links[z_id]:
            if adj not in zone_value: zone_value[adj] = 0
            if owner_id == -1:
                zone_value[adj] += platinum + 1
            elif owner_id != my_id:
                zone_value[adj] += platinum - en_pods

        pprint(f"{links[z_id]=}")
        pprint(f"{zone_value=}")
        pods_left = my_pods

        while pods_left:
            # dict(adj_zone, value)
            adj_value = {key: zone_value[key] for key in links[z_id] if key in zone_value}
            max_adj_value = max(adj_value.values())
            # zones tied with best value
            adj_best = set(k for (k,v) in adj_value.items() if v == max_adj_value)
            pprint(f"{adj_value=}")
            pprint(f"{max_adj_value=}")
            pprint(f"{adj_best=}")

            # pick randomly one of adj_best to send a pod
            zone_dest = random.choice(list(adj_best))
            moves[(z_id, zone_dest)] += 1
            zone_value[zone_dest] -= 1
            pods_left -= 1

    # first line for movement commands
    if moves:
        string = ""
        # for move in moves:
        #     string += move.pods_count + " " + move.zone_orig + " " + move.zone_dest + " "
        for k, v in moves.items():
            string += f"{v} {k[0]} {k[1]} "
        print(string)
    else:
        print("WAIT")






    # second line no longer used (see the protocol in the statement for details)
    print("WAIT")