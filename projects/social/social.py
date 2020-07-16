import random

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships, seed = None):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """

        if seed:
            random.seed(seed)

        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # Shuffle the possible friendships
        random.shuffle(possible_friendships)

        # Add friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # We want shortest path to each person, so we use a BFT
        # Reference the code from the Ancestors Assignment

        # Start our Queue
        # Get our initial set of neighbors
        friend_queue = list(self.friendships[user_id])
        
        visited[user_id] = [user_id]

        # add each friend to visited dictionary
        # value is the path from initial user to them
        for friend in friend_queue:
            visited[friend] = [user_id, friend]

        while len(friend_queue) > 0:
            friend = friend_queue.pop(0)

            # Get friend's set of friends
            next_friends = self.friendships[friend]

            for next_friend in next_friends:
                
                # If we've already traversed this friend, then skip.
                if next_friend in visited:
                    continue
                
                # Add next friend to visited.
                # Set value equal to the friend's path + friend
                visited[next_friend] = visited[friend] + [next_friend]

                # Add next friend to our queue
                friend_queue.append(next_friend)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2, 42)
    print("\nRandomly Generated Network")
    print(sg.friendships)
    start = 1
    print("\nStarting user ID:", start)
    connections = sg.get_all_social_paths(start)
    print("\nConnections")
    print(connections,'\n')
