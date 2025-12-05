from typing import List


class Solution:
    """
    https://leetcode.com/problems/smallest-sufficient-team/discuss/334572/Python-DP-Solution
    DP + Bit
    Time O(people * 2^skill)
    Space O(2^skill)
    """
    def smallestSufficientTeam(self, req_skills: List[str], people: List[List[str]]) -> List[int]:
        memo = {v: i for i, v in enumerate(req_skills)}
        dp = {0: []}
        for i, skills in enumerate(people):
            hisSkill = 0
            for skill in skills:
                if skill in memo:
                    hisSkill |= 1 << memo[skill]  # one bit stands for one skill

            for skillset in list(dp):
                need = dp[skillset]
                newSkillset = skillset | hisSkill  # new skillset bits = old skillset bits | his skillset bits
                if newSkillset == skillset: continue  # if his skillset is subset of old skillset, skip
                if newSkillset not in dp or \
                        len(need) + 1 < len(dp[newSkillset]):  # find a solution with fewer people
                    dp[newSkillset] = need + [i]  # append cur index
        N = len(req_skills)
        return dp[(1 << N) - 1]  # (1<<N) - 1 = 11111...1 (All skills met)


print(Solution().smallestSufficientTeam(req_skills=["algorithms", "math", "java", "reactjs", "csharp", "aws"], people=
[["algorithms", "math", "java"], ["algorithms", "math", "reactjs"], ["java", "csharp", "aws"], ["reactjs", "csharp"],
 ["csharp", "math"], ["aws", "java"]]))
