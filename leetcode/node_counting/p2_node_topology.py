# (2) Return the entire tree topology to the root
# Extend the previous protocol so that the root not only gets the total count but reconstructs the full tree structure:
# Each machine must return a structured description of its subtree
# (e.g., {id: X, children: [ ... ]})
# back to its parent, and the root must assemble the full topology.
# Requirements:
# 	•	Use messages "topology" (downward request) and "topologyResponse" (upward reply).
# 	•	Each machine builds a JSON-like object describing:
#       { id: myId, children: [ subtree1, subtree2, ... ] }
#   •	Leaf nodes reply immediately with their own structure.
#   •	Internal nodes send "topology" down to children, wait for all "topologyResponse" messages, then merge them.
#   •	Root must output the final tree topology.
#  This is a distributed bottom-up tree reassembly protocol.

# Tree node
class Machine:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []
        # How many children have NOT responded yet?
        self.pending = 0
        # the running topology of subtree topology from all children, plus itself.
        self.topology = {'id': self.id, 'children': []}

    def sendAsync(self, msg, target: "Machine"):
        # Conceptually asynchronous. In a real actor system this would enqueue.
        # For the interview we just call directly.
        target.receive(msg, self)

    def receive(self, msg: str, src: "Machine"):
        if msg == 'topology':
            if not self.children: # leaf node
                # This is the base case of the distributed DFS.
                if self.parent is not None:
                    # Reach leaf node, bottom up reporting
                    self.sendAsync(('topologyResponse', self.topology), self.parent)
                else:
                    # Root-leaf node
                    self.printResult()
                return

            # fan out
            self.pending = len(self.children)
            for child in self.children:
                # Top down
                self.sendAsync("topology", child)

        # Every time a child finishes its work and replies
        elif msg[0] == 'topologyResponse':
            subtree = msg[1]
            # I add that child’s topology into *my* running topology
            self.topology['children'].append(subtree)
            # I mark that one of my children - i don't care which - has responded (aka. finished)
            self.pending -= 1

            if self.pending == 0: # all my children have responded
                if self.parent is None: # root node
                    self.printResult()
                else:
                    # I can now report *my* subtree size to my parent
                    self.sendAsync(("topologyResponse", self.topology), self.parent)

    # output number of total machines
    def printResult(self):
        print(f"[root id={self.id}, FULL_TOPOLOGY = ", self.topology) # output number of total machines
