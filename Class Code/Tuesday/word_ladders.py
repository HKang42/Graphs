"""
Word Ladders
------------

Given two words (begin_word and end_word), and a dictionary's word list, return
the shortest transformation sequence from begin_word to end_word, such that:

Only one letter can be changed at a time.

Each transformed word must exist in the word list. Note that begin_word is not
a transformed word.

Note:

Return None if there is no such transformation sequence.
All words contain only lowercase alphabetic characters.
You may assume no duplicates in the word list.
You may assume begin_word and end_word are non-empty and are not the same.

start:  hit
ending: cog


hit -> hot -> hog -> cog
hit -> hot -> cot -> cog

starting: sail
ending: boat
"""

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def find_ladders(begin_word, end_word):  # BFS
    visited = set()
    q = Queue()

    q.enqueue([begin_word])

    while q.size() > 0:
        path = q.dequeue()

        v = path[-1]

        if v not in visited:
            visited.add(v)

            if v == end_word:
                return path

            for neighbor in get_neighbors(v):
                path_copy = list(path)
                path_copy.append(neighbor)
                q.enqueue(path_copy)

    return None



word_set = set()

# Read all words from the file and add them to the set

with open('words.txt') as f:
    for line in f:
        word = line.strip()  # remove newlines

        word_set.add(word)

#letters = ['a', 'b', 'c'...
import string
letters = list(string.ascii_lowercase)

def get_neighbors(word):   # O(n^2) over word len
    neighbors = []

    string_word = list(word)   #  ['w', 'o', 'r', 'd']

    for i in range(len(string_word)):

        for letter in letters:  # for every letter in the alphabet
            temp_word = list(string_word)  # Make a copy that we can munge

            temp_word[i] = letter

            w = "".join(temp_word)  # Turn it back into a string

            if w == word:  # Words are not their own neighbors
                continue

            if w in word_set:
                neighbors.append(w)

    return neighbors


print(find_ladders("sail", "boat"))
print(find_ladders("hit", "cog"))


