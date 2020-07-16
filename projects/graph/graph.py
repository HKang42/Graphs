"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if (v1 and v2) in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("One or more vertices not found.")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise IndexError("Vertex not found")

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """

        # initialize queue with our starting vertex
        q = Queue()
        q.enqueue(starting_vertex)

        # Set for tracking nodes we've already visited
        visited = set()

        # Loop logic
        # Remove vertex from queue and check if it's been visited. 
        # If yes, 
        #       skip to next loop
        # If not, 
        #       add to set of visisted vertices
        #       add neighbors to the queue
        while q.size() > 0:
            vert = q.dequeue()
            
            if vert in visited:
                continue
            
            else:
                visited.add(vert)

                print(f"{vert}")

                neighbor_set = self.get_neighbors(vert)
                q.queue.extend(neighbor_set)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # The below code is analogous to the breadth first search (bft)
        # Only difference is that we use a stack instead of a queue
        # Only resulting change is that we can't extend a stack like q queue's list
        # So we use a loop to push nodes onto the stack

        s = Stack()
        s.push(starting_vertex)

        visited = set()

        while s.size() > 0:
            vert = s.pop()
            
            if vert in visited:
                continue
            
            else:
                visited.add(vert)

                print(f"{vert}")

                neighbor_set = self.get_neighbors(vert)
                for node in neighbor_set:
                    s.push(node)

    def dft_recursive(self, starting_vertex, stack = Stack(), visited = set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Base case is that the stack is empty after we have visited the first node
        if stack.size == 0 and starting_vertex in visited:
            return
        
        # Don't traverse a node if we've already visisted it
        if starting_vertex in visited:
            return
        
        if len(visited) == 0:
            stack.push(starting_vertex)

        visited.add(starting_vertex)

        print(f"{starting_vertex}")
        
        neighbor_set = self.get_neighbors(starting_vertex)
        for node in neighbor_set:
            stack.push(node)
        
        n = stack.pop()
        return self.dft_recursive(n, stack, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breadth-first order.
        """

        # Breadth-first search is pretty similar to breadth-first traversal.
        # The main difference is that we use lists of nodes instead of just single 
        # Visual illustration of how the code runs in "BFS - step by step.jpg"

        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        # Create a Set to store visited vertices
        # While the queue is not empty...
            # Dequeue the first PATH
            # Grab the last vertex from the PATH
            # If that vertex has not been visited...
                # CHECK IF IT'S THE TARGET
                  # IF SO, RETURN PATH
                # Mark it as visited...
                # Then add A PATH TO its neighbors to the back of the queue
                  # COPY THE PATH
                  # APPEND THE NEIGHOR TO THE BACK

        # remember to enqueue a list
        q = Queue()
        q.enqueue([starting_vertex])

        visited = set()

        while q.size() > 0:
            # Grab the oldest path
            vert_path = q.dequeue()

            # Get vertex at end of path
            vert = vert_path[-1]

            # Skip if we already visited it
            if vert in visited:
                continue
            
            # Check if it's our destination.
            # Note that because we use Breadth-First, we know that our first 
            # result is the shortest path 
            elif vert == destination_vertex:
                return vert_path

            # Otherwise we travel to the node and add the paths to each of
            # its neighbors to the queue
            else:
                visited.add(vert)

                neighbor_set = self.get_neighbors(vert)
                
                for neighbor in neighbor_set:

                    # We skip the neighbor that would take us to the previous node
                    # Note that our code would still work without this check
                    if neighbor != vert:
                        path = vert_path + [neighbor]
                        q.enqueue(path)
        
        raise IndexError("No such path exists. Please check node edges.")


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # The code here is essentially the same as in bfs, but adopted for dft.
        s = Stack()
        s.push([starting_vertex])

        visited = set()

        while s.size() > 0:
            vert_path = s.pop()
            vert = vert_path[-1]

            if vert in visited:
                continue

            elif vert == destination_vertex:
                return vert_path

            else:
                visited.add(vert)

                neighbor_set = self.get_neighbors(vert)
                for neighbor in neighbor_set:
                    if neighbor != vert:
                        path = vert_path + [neighbor]
                        s.push(path)
        
        raise IndexError("No such path exists. Please check node edges.")

    def dfs_recursive(self, starting_vertex, destination_vertex, stack = Stack(), visited = set()):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # If we are just starting, push the starting vertex into the stack
        if len(visited) == 0:
            stack.push([starting_vertex])

        # Grab the path on the top of the stack
        vert_path = stack.pop() 
        vert = vert_path[-1]

        # Base case is that the stack is empty after we have visited the first node
        if vert == destination_vertex:
            return vert_path
        
        # Don't traverse anymore if we reach a node we've already visisted
        if vert in visited:
            return

        # Otherwise, we add to our visited set
        # and add paths to neighbors to our stack
        visited.add(vert)

        neighbor_set = self.get_neighbors(vert)
        for neighbor in neighbor_set:
            if neighbor != vert:
                path = vert_path + [neighbor]
                stack.push(path)
        
        return self.dfs_recursive(starting_vertex, destination_vertex, stack, visited)

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
