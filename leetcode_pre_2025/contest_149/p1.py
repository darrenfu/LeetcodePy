from datetime import datetime


class Solution:
    def dayOfYear(self, date: str) -> int:
        dt = datetime.strptime(date, '%Y-%m-%d')

        def isLeapYear(y: int) -> bool:
            if y % 4 == 0:
                if y % 100 == 0:
                    return y % 400 == 0
                return True
            return False
        leap = isLeapYear(dt.year)
        days = [0, 31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        res = 0
        for m in range(dt.month):
            res += days[m]
        res += dt.day
        return res


print(Solution().dayOfYear("2019-01-09"))
print(Solution().dayOfYear("2019-02-10"))
print(Solution().dayOfYear("2003-03-01"))
print(Solution().dayOfYear("2004-03-01"))
