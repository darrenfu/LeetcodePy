# Requirement
# (1) Count the total number of machines in the tree
# You are given a distributed tree of machines (each machine knows its parent and children and can only communicate via asynchronous messages).
# Your task:
# Design a message-passing protocol so that the root machine eventually learns the total number of machines in the entire tree.
# Requirements:
# 	•	Use only asynchronous messages (sendAsync(msg) / receiveMessage(msg)).
# 	•	Every machine participates in the protocol.
# 	•	Leaf nodes must send their result upward.
# 	•	Non-leaf nodes must wait for all children to respond before sending their result upward.
# 	•	Root must output the final machine count.
# This must be done without global state, without shared memory, and without centralized control.

# Tree node
class Machine:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []
        # How many children have NOT responded yet?
        self.pending = 0
        # the running sum of subtree sizes from all children, plus itself.
        self.acc = 1

    def sendAsync(self, msg, target: "Machine"):
        # Conceptually asynchronous. In a real actor system this would enqueue.
        # For the interview we just call directly.
        target.receive(msg, self)

    def receive(self, msg: str, src: "Machine"):
        if msg == 'count':
            if not self.children: # leaf node
                # The subtree under me has size 1 (only myself).
                # This is the base case of the distributed DFS.
                if self.parent is not None:
                    # Reach leaf node, bottom up reporting agg count
                    self.sendAsync(('countResponse', 1), self.parent)
                else:
                    self.printResult() # output number of total machines
                return
            # fan out
            self.pending = len(self.children)
            for child in self.children:
                # Top down
                self.sendAsync("count", child)

        # Every time a child finishes its work and replies
        elif msg[0] == 'countResponse':
            node_cnt = msg[1]
            # I add that child’s subtree size into *my* running total
            self.acc += node_cnt
            # I mark that one of my children - i don't care which - has responded (aka. finished)
            self.pending -= 1

            if self.pending == 0: # all my children have responded
                if self.parent is None: # root node
                    self.printResult() # output number of total machines
                else:
                    # I can now report *my* subtree size to my parent
                    self.sendAsync(("countResponse", self.acc), self.parent)

    def printResult(self):
        print(f"[root id={self.id}, TOTAL = ", self.acc) # output number of total machines