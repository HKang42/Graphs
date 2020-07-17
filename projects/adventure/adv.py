from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
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

def room_adder(graph, room_object):
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

    connections = {}

    for direction in room_connections:
        connections[direction] = '?'
    
    graph[room_id] = connections


# Create our graph dictionary to track nodes and connections
# Keys are room ID's
# Values are dictionaries. 
#       Keys are directions ('n', 's', 'e', 'w') and values are the connecting room
graph = {}

#room_id = player.current_room.id
#room_connections = player.current_room.get_exits()
#graph[room_id] = room_connections
room = player.current_room
room_adder(graph, room)


print(graph)


player.travel(n)


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



# print('\n')
# print(player.current_room.id)
# print(player.current_room.get_exits())
# player.travel('n')
# player.travel('w')
# player.travel('w')
# player.travel('n')
# print(player.current_room.id)
# print(player.current_room.get_exits())
# print('\n')



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
"""


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
