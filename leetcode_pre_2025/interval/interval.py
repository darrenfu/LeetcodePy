# Definition for an interval.
class Interval(object):
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return "({}, {})".format(self.start, self.end)
