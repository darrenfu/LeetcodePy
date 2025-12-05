# Factory function for creating tuple subclasses with named fields
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)

# Pros vs plain tuple:
# •	Readability: p.x instead of p[0]
# •	Still lightweight & immutable like a tuple
# •	Works well in performance-sensitive, structured-data code
# (alternative to small classes / dicts)

# Double-ended queue: fast appends and pops from both ends
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)       # right side
dq.appendleft(0)   # left side
dq.pop()           # O(1)
dq.popleft()       # O(1)
# Pros vs list:
# •	list.pop(0) is O(n) (needs shifting); deque.popleft() is O(1)
# •	Designed for queue, sliding window, BFS, etc.
# •	You can also set maxlen for bounded history

# Single, layered view over multiple dicts
from collections import ChainMap

defaults = {"color": "red", "user": "guest"}
overrides = {"user": "alice"}

cfg = ChainMap(overrides, defaults)

print(cfg["user"])   # 'alice'
print(cfg["color"])  # 'red'

# Pros vs manually merging dicts:
# •	No copy; lookups walk mappings in order
# •	Great for layered configs: local → env → defaults
# •	Changes to inner dicts are instantly visible via the ChainMap

# Dict subclass that remembers insertion order
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
print(list(od.keys()))  # ['a', 'b']

# Pros vs plain dict:
# •	Pre-3.7: normal dicts were not guaranteed ordered; OrderedDict was.
# •	Extra methods: move_to_end, popitem(last=False) → great for LRU.
# •	Even now, it’s still useful for LRU and when you explicitly want those APIs.
#
# (Modern Python dicts preserve insertion order, but OrderedDict still gives LRU-ish operations cleanly.)

# Dict subclass that auto-creates a default value for missing keys
from collections import defaultdict

dd = defaultdict(list)
dd["a"].append(1)
dd["a"].append(2)
dd["b"].append(3)
# dd == {'a': [1, 2], 'b': [3]}

# Pros vs plain dict:
# •	Avoids boilerplate: `d.setdefault(key, []).append(x)`
# •	Very handy for grouping, adjacency lists, counting, etc.
# •	You pass a factory (list, set, int, custom function) to auto-create values.

# Wrapper around dict for easier subclassing
from collections import UserDict

class LowerCaseDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

d = LowerCaseDict()
d["Foo"] = 1
print(d["foo"])  # 1

# Pros vs subclassing dict directly:
# •	Dict is implemented in C and has some tricky internal behavior when subclassed.
# •	UserDict stores data in self.data (a real dict) and is pure Python → safer & easier to override.

# Wrapper around list for easier subclassing
from collections import UserList

class NonEmptyList(UserList):
    def append(self, item):
        if item is None:
            return
        super().append(item)

# Pros vs subclassing list:
# 	•	Similar story: list is C-level; overriding methods can be subtle.
# 	•	UserList wraps a real list in self.data,
# so you override behavior in pure Python with fewer gotchas.

# Wrapper around string for easier subclassing
from collections import UserString

class SafeString(UserString):
    def upper(self):
        return super().upper().replace("BAD", "***")

s = SafeString("bad value")
print(s.upper())  # '*** VALUE'

# Pros vs subclassing str:
# 	•	Strings are immutable, C-implemented, weird to subclass.
# 	•	UserString wraps a real string in .data, making it easier to customize behavior.
