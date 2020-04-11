from collections import defaultdict


class KVStore:

    def __init__(self):
        self.global_version = 0
        self.kvmap = defaultdict(list)

    def parse(self, line: str):
        args = line.split(" ")
        if 2 <= len(args) <= 3:
            cmd, key = args[0], args[1]
            if cmd == "GET":
                if len(args) == 2:
                    ret = self.get(key)
                    self.formatOutput(cmd, key, ret)
                elif len(args) == 3:
                    version = int(args[2])
                    ret = self.get(key, version)
                    self.formatOutput(cmd, key, ret, version)
                else:
                    raise Exception("Invalid input")
            elif cmd == "PUT":
                val = int(args[2])
                self.put(key, val)
                self.formatOutput(cmd, key, val)
            else:
                raise Exception("Invalid input")
        else:
            raise Exception("Invalid input")

    def formatOutput(self, cmd: str, key: str, val: int, version: int=None) -> str:
        if cmd == "PUT":
            print("PUT(#" + str(self.global_version) + ") " + key + " = " + str(val))
        elif cmd == "GET":
            val = "<NULL>" if val is None else str(val)
            if version is None:
                print("GET " + key + " = " + val)
            else:
                print("GET " + key + "(#" + str(version) + ") = " + val)
        else:
            raise Exception("Invalid command")

    def put(self, key: str, value: int) -> None:
        self.global_version += 1
        self.kvmap[key] += (value, self.global_version),

    def get(self, key: str, version: int = None) -> int:
        vals = self.kvmap[key]
        if not vals:
            return None
        if version is None:
            # get the tail of value list
            return vals[-1][0]
        # use binary search to find the largest value position close to the version
        lo, hi = 0, len(vals)-1  # head version and tail version in the list
        while lo <= hi:
            mid = lo + (hi-lo)//2
            mid_version = vals[mid][1]
            if version == mid_version:
                return vals[mid][0]
            if version < mid_version:
                hi = mid-1
            else:
                lo = mid+1
        return None if hi == -1 else vals[hi][0]


s = KVStore()
while True:
      line = input()
      s.parse(line)

# s.put("k1", 11)
# s.put("k1", 12)
# s.put("k2", 23)
# s.put("k2", 24)
# s.put("k1", 15)
# print(s.get("k1"))  # 15
# print(s.get("k2"))  # 24
# print(s.get("k1", 0))  # None
# print(s.get("k1", 1))  # 11
# print(s.get("k1", 2))  # 12
# print(s.get("k1", 3))  # 12
# print(s.get("k1", 4))  # 12
# print(s.get("k1", 5))  # 15
# print(s.get("k1", 6))  # 15
# print(s.get("k1", 1000))  # 15
# print(s.get("k2", 2))  # None
# print(s.get("k2", 4))  # 24
# print(s.get("k3", 4))  # None
# print(s.get("k3"))  # None


