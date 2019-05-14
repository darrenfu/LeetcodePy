class Solution(object):
    def isBoomerang(self, points):
        """
        :type points: List[List[int]]
        :rtype: bool
        """
        x0, y0 = points[0]
        x1, y1 = points[1]
        x2, y2 = points[2]
        if x0 == x1 and x1 == x2 and y0 != y1 and y0 != y2 and y1 != y2: return False
        if (x0 == x1 and y0 == y1) or (x1 == x2 and y1 == y2) or (x0 == x2 and y0 == y2): return False
        if x0 == x1 or x1 == x2 or x2 == x0: return True
        k1 = (y1 - y0) / (x1 - x0)
        b1 = y0 - k1 * x0
        k2 = (y2 - y1) / (x2 - x1)
        b2 = y1 - k2 * x1
        return not (k1 == k2 and b1 == b2)
