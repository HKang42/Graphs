from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


n, s, w, e = ['n', 's', 'w', 'e']

"""
You may find the following commands useful:
#   player.current_room.id
#   player.current_room.get_exits()
#   player.travel(direction) 
"""

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


def direction_chooser(exits):
    for direction in exits:
        if exits[direction] == '?':
            return direction
    
    #print(":(")
    return None


def traversal(player, graph, traversal_path, total_rooms, printing = False):
    
    starting_exits = player.current_room.get_exits()
    dir = starting_exits[0]

    visit_counter = 1

    while dir is not None:
        if printing == True:
            print('\nCurrent Room:', player.current_room.id)
            print('Direction:', dir)
            print(graph)
        
        exits = move(player, graph, dir)
        traversal_path.append(dir)
        visit_counter += 1

        if visit_counter >= total_rooms:
            return

        dir = direction_chooser(exits)
        
        # If dir is None, then we have no unexplored rooms from out current position.
        # We need to backtrack until we find an unexplored room.
        if dir == None:
            # Backtrack by looping with a negative interval (remember to subtract 1 from the start and end range)
            # Get the last direction, flip it, and move that way.
            # Check to see if there is an unexplored room.
            # If yes, dir is no longer None and we break
            # Else, we backtrack again
            for i in range(len(traversal_path) - 1, -1, -1):
                last_move = traversal_path[i]
                back_track = flip(last_move)
                exits = move(player, graph, back_track)
                traversal_path.append(back_track)
                dir = direction_chooser(exits)

                # Stop when we find an unexplored room
                if dir is not None:
                    break
                
                # If our backtracking loop cannot find an unexplored room, then return
                if i == 0:
                    return 

    print('\nCurrent Room:', player.current_room.id)
    print('Direction:', dir)
    print(graph)

traversal(player, graph, traversal_path, len(room_graph))

print('\nTraversal Path')
print(traversal_path, '\n')


#print('\n\n')
#print(graph)

# print(player.current_room.id)
# print(graph)

# direction = direction_chooser(exits)
# exits = move(player, graph, direction)
# print(player.current_room.id, direction)
# print(graph)

# direction = direction_chooser(exits)
# print(exits)
# exits = move(player, graph, direction)
# print(player.current_room.id, direction)
# print(graph)

# direction = direction_chooser(exits)
# exits = move(player, graph, direction)
# print(player.current_room.id, direction)
# print(graph)

# direction = direction_chooser(exits)
# exits = move(player, graph, direction)
# print(player.current_room.id, direction)
# print(graph)

# direction = direction_chooser(exits)
# exits = move(player, graph, direction)
# print(player.current_room.id, direction)
# print(graph)


"""
Start at a room with known ID and exits

Pick a valid exit 

Travel through that exit


Get new room ID
Get valid exits

Save that ID as the value for the exit

Create entry for the ID in our Graph
Values are the valid exits


Pick valid exit


"""


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



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
