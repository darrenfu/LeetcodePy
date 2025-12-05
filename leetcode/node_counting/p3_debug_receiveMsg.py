class Machine:
    def __init__(self, val):
        self.val = val
        self.parent: "Machine | None" = None
        self.children: list["Machine"] = []

        self.pending = 0  # how many children we're waiting for

    def sendAsync(self, msg, target: "Machine"):
        # Conceptually async – direct call here for simplicity
        target.receiveMessage(msg, self)

    def receiveMessage(self, msg, src: "Machine"):
        # Start of "compute max in subtree" protocol
        if msg == "max":
            # ❌ BUG #1: update self.val using *stale* child values BEFORE
            # asking children to compute THEIR subtree max.
            if self.children:
                child_vals = [ch.val for ch in self.children]  # STALE values
                self.val = max([self.val] + child_vals)

            if not self.children:
                # leaf: just send my current value upward
                if self.parent is not None:
                    self.sendAsync(("maxResponse", self.val), self.parent)
                return

            # fan out to children
            self.pending = len(self.children)
            for ch in self.children:
                self.sendAsync("max", ch)

        elif msg[0] == "maxResponse":
            child_max = msg[1]

            # ❌ BUG #2: directly overwrite self.val per child, with no accumulator.
            # This can lose previously seen bigger values or parent’s own value.
            self.val = max(self.val, child_max)

            self.pending -= 1

            if self.pending == 0:
                # done with all children, send result up
                if self.parent is not None:
                    self.sendAsync(("maxResponse", self.val), self.parent)
                else:
                    print(f"[root] FINAL MAX AT ROOT = {self.val}")

## Correct answer
class Machine:
    def __init__(self, val):
        self.val = val
        self.parent: "Machine | None" = None
        self.children: list["Machine"] = []

        # how many children we’re still waiting for
        self.pending = 0
        # accumulator for the max over my subtree (including myself)
        self.max_acc = self.val

    def sendAsync(self, msg, target: "Machine"):
        # Conceptually async – direct call here for simplicity
        target.receiveMessage(msg, self)

    def receiveMessage(self, msg, src: "Machine"):
        # Start of "compute max in subtree" protocol
        if msg == "max":
            if not self.children:
                # Leaf: its subtree max is just its own value
                if self.parent is not None:
                    self.sendAsync(("maxResponse", self.val), self.parent)
                else:
                    # I'm the root and also a leaf
                    print(f"[root] FINAL MAX AT ROOT = {self.val}")
                return

            # Non-leaf: initialize accumulator with my own value
            self.max_acc = self.val

            # Fan out to children (post-order style: children compute first)
            self.pending = len(self.children)
            for ch in self.children:
                self.sendAsync("max", ch)

        elif msg[0] == "maxResponse":
            child_max = msg[1]

            # incorporate this child's subtree max
            self.max_acc = max(self.max_acc, child_max)

            self.pending -= 1

            if self.pending == 0:
                # all children responded; now my subtree max is finalized
                self.val = self.max_acc

                if self.parent is not None:
                    # send my subtree max upward
                    self.sendAsync(("maxResponse", self.val), self.parent)
                else:
                    # I'm the root: global protocol done
                    print(f"[root] FINAL MAX AT ROOT = {self.val}")