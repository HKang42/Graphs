from room import Room
from player import Player
from world import World

import pprint
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# assign variables so we don't need to types quotes every time we use a direction
n, s, w, e = ['n', 's', 'w', 'e']


# Create our graph dictionary to track nodes and connections
# Keys are room ID's
# Values are dictionaries. 
#       Keys are directions ('n', 's', 'e', 'w') and values are the connecting room
graph = {}


def flip(direction):
    """
    Given a compass direction (N, E, S, W)
    Return the opposite direction
    """
    # Split the cardinal directions into North/South and East/West
    # Apparently, there are words for these directions
    # https://en.wikipedia.org/wiki/Zonal_and_meridional_flow
    meridional = ['n', 's']
    zonal = ['e', 'w']  

    if direction in meridional:
        if direction == 'n':
            return 's'
        else:
            return 'n'
    
    elif direction in zonal:
        if direction == 'e':
            return 'w'
        else:
            return 'e'

    else:
        raise ValueError("Input direction must be 'n', 's', 'e', or 'w'.")


def room_adder(graph, room_object, direction, ID):
    """
    Given a graph dictionary and a room object
    
    Gets the possible connections/exits from the room object
    Creates a dictionary using the exits as keys
    Values are set to '?'

    Then takes the graph dictionary
    Adds the room ID as a key 
    The value is the dictionary of exits
    
    returns nothing
    """
    room_id = room_object.id
    room_connections = room_object.get_exits()
    
    # If we have not encountered this room before, make a new entry
    if room_id not in graph:
        
        # Create our connections dictionary
        connections = {}
        for exit in room_connections:
            connections[exit] = '?'
        
    # If we have seen the room before
    else:
        # Get what we already knew about the room's connections
        connections = graph[room_id]

    connections[direction] = ID
    graph[room_id] = connections

    return connections


def move(player, graph, direction):
    """
    Moves the player travel in the given direction
    
    Updates the Graph dictionary with the connections between the previous room 
    and the new room

    """
    # save old room, move player in direction, get new room
    prev_room = player.current_room
    player.travel(direction)
    new_room = player.current_room

    # Link our previous room to the new one
    room_adder(graph, prev_room, direction, new_room.id)

    # Link our new room to the previous one
    new_exits = room_adder(graph, new_room, flip(direction), prev_room.id)

    return new_exits


def direction_chooser(exits, reverse = False):
    if reverse == False:
        for direction in exits:
            if exits[direction] == '?':
                return direction
    
    # The above code causes our algorithm to prioritize directions in 
    # the order North, South, West, East
    elif reverse == True:
        dir = ['n', 's', 'w', 'e']
        for i in range(len(dir)-1, -1, -1):
            if dir[i] in exits:
                if exits[dir[i]] == '?':
                    return dir[i]
    #print(":(")
    return None


def unknown_room_bfs(graph, start_room):
    """
    Given our graph of nodes and a starting room ID,
    search for the closest room with an un-explored connection (This will not always be an unexplored room)
    
    returns list of directions to the closest unexplored room
    """
    visited = {}

    queue = []
    
    # For our starting room, there is no path
    visited = set()
    visited.add(start_room)

    starting_exits = graph[start_room]
    for dir in starting_exits:
        next_room = starting_exits[dir]
        queue.append( [next_room, [dir] ] )

    while len(queue) > 0:

        room, path = queue.pop(0)

        visited.add(room)

        exits = graph[room] 

        for dir in exits:
            
            next_room = exits[dir]
            next_path = path.copy()
            next_path.append(dir)

            # If we have already visited the room, then skip
            if next_room in visited:
                continue
            
            # If the next room is unexplored, then we return the path
            if next_room == '?':
                return next_path
            
            # Else, we add that room and the path to that room to the queue
            else:
                queue.append( [next_room, next_path])


def traversal(player, graph, traversal_path, total_rooms, printing = False):
    
    starting_exits = player.current_room.get_exits()
    dir = starting_exits[0]
    visited = set()
    visited.add(player.current_room.id)

    print("Map file:\t\t", map_file)
    print("Starting Room:\t\t", player.current_room.id)
    print("Starting Exits:\t\t", starting_exits)
    print("Starting Direction:\t", dir, '\n')

    if printing == True and total_rooms >= 10:
        p_check = input("Are you sure you want to print traversal process? (y/n) ")
        if p_check.lower() == 'y':
            pass
        else:
            raise ValueError("Please disable printing")

    while len(graph) < total_rooms:
        # If dir is None, then we have no unexplored rooms from our current position.
        # We need to backtrack until we find an unexplored room.
        if dir == None:

            path_to_unexplored = unknown_room_bfs(graph, player.current_room.id)

            for direction in path_to_unexplored[:-1]:
                player.travel(direction)
                traversal_path.append(direction)
            
            if printing == True:
                print('\nCurrent Room:', player.current_room.id)
                print('Direction:', dir)
                print(graph)

            dir = path_to_unexplored[-1]

        if printing == True:
            print('\nCurrent Room:', player.current_room.id)
            print('Direction:', dir)
            print(graph)
        
        exits = move(player, graph, dir)
        traversal_path.append(dir)
        
        visited.add(player.current_room.id)

        dir = direction_chooser(exits)

    return visited


print('\n')
v = traversal(player, graph, traversal_path, len(room_graph), printing = False)

# print('\nTraversal Path')
# print(traversal_path, '\n')
print('\nTraversal Path Length:   ', len(traversal_path))

print("Expected number of rooms:", len(room_graph))
print("Number of visited rooms: ", len(v))

# TRAVERSAL TEST
print('\n\n### TRAVERSAL TEST ###')
visited_rooms = set()
visited_rooms_ID = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    visited_rooms_ID.add(player.current_room.id)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# Print any missing rooms
miss = []
for room in room_graph:
    if room not in v:
        miss.append(room)
if len(miss) > 0:
    m = miss
else:
    m = None
print('\nMissing Rooms:', m, '\n')


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
