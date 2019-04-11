class Solution(object):
    def camelMatch(self, queries, pattern):
        """
        :type queries: List[str]
        :type pattern: str
        :rtype: List[bool]
        """

        def upper(s):
            return [c for c in s if c.isupper()]

        def is_sup(pattern, q):
            it = iter(q)
            # why c in it?
            return all(c in it for c in pattern)

        return [upper(query) == upper(pattern) and is_sup(pattern, query) for query in queries]

