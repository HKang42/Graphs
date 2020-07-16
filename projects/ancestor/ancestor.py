"""
Write a function that, 
    given the dataset and the ID of an individual in the dataset, 
    returns their earliest known ancestor – the one at the farthest distance from the input individual. 
    If there is more than one ancestor tied for "earliest", return the one with the lowest numeric ID. 
    If the input individual has no parents, the function should return -1.

"""

"""
Generate the graph using the parent-child pairs from the dataset.
    We only need to be able to go "up" 
    Use a directional graph?

    We need to traverse the entire graph from our starting point and moving upwards
        Probably use BFT
        Use something to track progress

"""
# Maybe we don't need to make a graph
# Since we only need to move in 1 direction (from child to parent), we cam use a dictionary/hash table
# Each key is a child and values are the parents.

# Given our input, we lookup the parents 
#   if the parents exists, then we use them as keys (i.e. are they children to anyone) and find their parents
#   repeat this process until we have exhausted the nodes.

# As we traverse, we need to track the number of nodes/parents we move through
# At the end, return the longest one.

def earliest_ancestor(ancestors, starting_node = 0):
    
    # Create dictionary from the list of parent-child pairs
    # Each key is a child. Each value is a list of parents
    # I was pretty tempted to call this tree of ancestors the "Ancestree"
    ancestor_graph = {}
    for pair in ancestors:
        parent = pair[0]
        child = pair[1]
        
        if child not in ancestor_graph:
            ancestor_graph[child] = [parent]
        else:
            ancestor_graph[child].append(parent)
    
    # If the input person has no parents, return -1
    if starting_node not in ancestor_graph:
        return -1

    # Parents will act as our queue for the BFT (refer to graph.py in the "graph" directory)
    # It will be a list where each entry is a sublist of parents.
    parents = []
    for parent in ancestor_graph[starting_node]:
        parents.append([parent])

    # Dictionary we will use to track path length.
    # Each key is a path length. 
    # Each value is a list of parents that correspond to that distance from our starting node
    paths = {}
    
    # Track the oldest/farthest distance 
    earliest = 0

    # As long as there are parents in our list, we loop 
    while len(parents) > 0:
        parent_list = parents.pop(0)
        parent = parent_list[-1]

        # If the parent has no parent, then we have reached the end of this line
        # We record the number of parents it took to reach him/her as well as the path
        if parent not in ancestor_graph:
            generations = len(parent_list)
            earliest = max(generations, earliest)

            if generations not in paths:
                paths[generations] = [parent]
            else:
                paths[generations].append(parent)
            continue
        
        # If the parent has parent(s) then we append each to parents
        # e.g. if child 1 has parents 3, and 4, then we append [1,3] and [1,4]
        else:
            new_parents = ancestor_graph[parent]
            
            for new_par in new_parents:
                path = parent_list + [new_par]
            
                parents.append(path)
    
    return sorted(paths[earliest])[0]



test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 6))