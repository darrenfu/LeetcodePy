# Compute Balances and Minimize Settlements — Guided practice / 引导练习

Source / 来源: [PracHub question](https://prachub.com/coding-questions/compute-balances-and-minimize-settlements), both Description parts verified 2026-10-03. Read `question.md` first. This report supplies reasoning prompts and an incomplete pseudocode scaffold for Darren to implement independently.

来源：2026-10-03 核对详情页 Description 中的两部分。先阅读 `question.md`。本报告提供思考提示与不完整伪代码骨架，由 Darren 独立完成实现。

## Problem restatement / 题目重述

**English.** Part 1 reduces one day's records into a user-to-net-balance mapping, excluding final zeros. Part 2 accepts a zero-sum balance mapping and returns the smallest transfer **count**, not a list of transfers. Positive balances receive money; negative balances pay. The small number of non-zero users makes exhaustive optimization plausible.

**中文。** 第一部分把一天的记录聚合成用户净余额映射，排除最终余额为零的用户。第二部分输入零和余额映射，输出最少转账**次数**，不是转账清单。正余额用户收款，负余额用户付款。非零用户数较少，因此可以考虑穷举优化。

Before coding, explain why timestamps do not affect Part 1's final sum, and why Part 1's example cannot automatically be passed into Part 2. Write the two functions' input and output contracts separately.

动手前，解释时间戳为什么不影响第一部分最终求和，以及为何不能直接把第一部分示例传入第二部分。分别写出两个函数的输入输出约定。

## Hints（三级提示，由模糊到具体）

### Level 1 / 一级：What information matters? / 什么信息重要？

**English.** After processing all records, does transaction order matter? For settlement counting, do names matter, or only the non-zero balances? Can two independent sets of users settle without exchanging money between the sets?

**中文。** 处理完全部记录后，交易顺序还重要吗？计算结算次数时，用户名重要，还是非零余额重要？两组用户是否能各自结清，而无需跨组转账？

### Level 2 / 二级：Find the optimization target / 找到优化目标

**English.** A zero-sum group can settle internally in at most one fewer transfer than its account count. Splitting it into two zero-sum groups can save a transfer. Try to maximize the number of disjoint zero-sum groups. Why must every connected component of a completed settlement graph sum to zero?

**中文。** 一个零和组内部最多可以用“账户数减一”笔转账结清。若能拆成两个零和组，可以再省一笔。尝试最大化互不重叠的零和组数量。为什么完整结算图的每个连通分量都必须是零和？

### Level 3 / 三级：Represent the remaining users / 表示剩余用户

**English.** Give the `n` non-zero users fixed indices and represent a subset by a bitmask. Cache each subset's balance sum. In a remaining set, anchor one user and enumerate only zero-sum subgroups containing that user; recursively optimize the remainder. This avoids counting different orders of the same groups. Decide the base case, impossible-state marker, recurrence, and memoization key yourself before filling the scaffold.

**中文。** 给 `n` 个非零用户固定编号，用位掩码表示子集，缓存子集余额和。在剩余集合中固定一个用户，只枚举包含此用户的零和子组，然后递归优化剩余集合。这样可以避免同一组划分的不同排列重复出现。先自行确定终止条件、不可达标记、递推式和缓存键，再补全骨架。

## Invariants / 关键不变量

- **Aggregation / 聚合：** After any processed prefix, each stored balance equals that user's sum over that prefix. Zero filtering is based on the final sum. / 处理任意前缀后，记录的余额等于该用户在此前缀中的变化量之和。是否过滤零余额，以最终结果为准。
- **Conservation / 守恒：** Part 2 starts with total balance zero. Paying `x` raises a debtor's remaining balance by `x` and lowers a creditor's by `x`; their sum is unchanged. / 第二部分初始总余额为零。付款 `x` 使债务人的剩余余额增加 `x`，收款人的剩余余额减少 `x`，两者之和不变。
- **Partition / 划分：** Selected groups are disjoint and zero-sum; every original non-zero account appears exactly once in a complete partition. Removing a zero-sum group leaves a zero-sum remainder. / 已选择的组互不重叠且各自零和；完整划分中，每个原始非零账户恰好出现一次。移除零和组后，剩余集合仍为零和。
- **Search / 搜索：** A memoized state describes only the remaining account set. No branch mutates the underlying balance values. / 缓存状态只描述剩余账户集合，各分支不修改原始余额数组。

**Why the objective works / 为什么目标成立。** A settlement graph component with `k` vertices needs at least `k - 1` edges to be connected and must have zero net sum. Conversely, matching debtors and creditors inside any zero-sum group needs at most `k - 1` transfers: each transfer exhausts at least one remaining account, and the last exhausts two. A group with a proper zero-sum subset may need fewer than `k - 1`, because it can split. A partition maximizing the number of zero-sum groups leaves no such splittable group. Combine the graph lower bound and this construction to justify the optimum `n - G_max`.

结算图中，一个含 `k` 个顶点的连通分量至少需要 `k - 1` 条边，且分量余额之和必须为零。反过来，任意零和组内配对债务人与债权人，最多用 `k - 1` 笔转账：每笔至少结清一个剩余账户，最后一笔结清两个。如果组内存在真零和子集，就可以拆组，实际可能少于 `k - 1`。零和组数量最大的划分不会留下这种可拆组。结合图的下界与组内结算的构造，论证最优次数为 `n - G_max`。

## Data structure / 数据结构选择与理由

**English.** Use a hash map keyed by user ID for Part 1's repeated accumulation. For Part 2, extract non-zero values into a fixed array; names are unnecessary when only the count is returned. A bitmask identifies remaining accounts without copying sets. A subset-sum table supports constant-time zero-sum checks, and a memo table stores the best group count per remaining mask. A heap of largest balances can find a feasible settlement but does not establish minimality.

**中文。** 第一部分用以用户 ID 为键的哈希映射，方便反复累加。第二部分把非零余额提取到固定数组；只返回次数时，不需要用户名。位掩码表示剩余账户，无需复制集合。子集和表支持常数时间零和判断，缓存表保存每个剩余掩码的最大组数。最大余额堆可以构造可行结算，却不能证明次数最少。

## Algorithm / 算法步骤

1. **Aggregate / 聚合：** Scan the records, accumulating per-user deltas, then filter final zeros. / 扫描记录，按用户累加变化量，最后过滤零余额。
2. **Prepare / 准备：** For Part 2, discard zero values; check the zero-sum precondition when designing an API outside the judge. Assign fixed indices. / 第二部分排除零余额，固定编号；若设计题目之外的 API，应检查零和前提。
3. **Subset sums / 子集和：** Derive each subset sum from a smaller subset plus one account. / 从较小子集的和加上一个账户余额，推导当前子集和。
4. **Search partitions / 搜索划分：** Anchor one remaining account, consider every zero-sum subgroup containing it, and combine one chosen group with an optimal partition of the remainder. Memoize. / 固定一个剩余账户，考虑所有包含它的零和子组，将当前组与剩余集合的最优划分结合并缓存。
5. **Convert / 转换：** Convert the maximum group count to the minimum transfer count. Explain why the empty input works. / 把最大组数转换为最少转账次数，解释空输入如何处理。

### Pseudocode scaffold / 伪代码骨架

Intentionally incomplete: Darren must supply the state transitions and enumeration. / 特意留空：由 Darren 补充状态转移与枚举细节。

```text
COMPUTE_BALANCES(records):
    totals ← empty user map
    for each record:
        TODO: update the correct user's running total
    TODO: return only final non-zero entries

MIN_TRANSFERS(balance_map):
    values ← non-zero balances in a fixed order
    TODO: define the empty case and full mask
    TODO: build subset sums using a smaller-subset relation
    memo ← empty state cache

    BEST_GROUPS(remaining_mask):
        TODO: base case and cache lookup
        anchor ← one fixed account in remaining_mask
        for each candidate subgroup containing anchor:
            TODO: reject groups that are not zero-sum
            TODO: combine this group with the remaining-state result
            TODO: keep the best feasible group count
        TODO: cache and return

    TODO: convert BEST_GROUPS(full_mask) into transfer count
```

Before implementation, manually trace a two-account case and a case with two independent cancelling pairs. Show that each recursive step removes at least one account and that the full mask always has a feasible group when the precondition holds.

实现前，手工追踪两个账户的例子，以及两对独立相消账户的例子。说明每步递归至少移除一个账户，并说明在零和前提下，完整集合本身总是一个可选零和组。

## Complexity / 复杂度

Let `m` be the record count, `u` the distinct user count, and `n` the non-zero account count in Part 2. / 设 `m` 为记录数，`u` 为不同用户数，`n` 为第二部分非零账户数。

- **Part 1 / 第一部分：** Expected `O(m + u)` time and `O(u)` space using a hash map, including final filtering. / 哈希映射下期望时间 `O(m + u)`，空间 `O(u)`，包括最终过滤。
- **Part 2 / 第二部分：** `O(u)` preprocessing, `O(2^n)` subset-sum preparation, and an `O(3^n)` upper bound for memoized state/submask enumeration. The anchor reduces redundant choices without changing this upper bound. Total space is `O(u + 2^n)` including the input mapping, or `O(n + 2^n)` auxiliary space, with `O(n)` recursion depth. / 预处理 `O(u)`，子集和准备 `O(2^n)`，带缓存的状态与子掩码枚举上界为 `O(3^n)`。固定账户可减少重复选择，但不改变这个上界。包含输入映射的总空间为 `O(u + 2^n)`，辅助空间为 `O(n + 2^n)`，递归深度为 `O(n)`。

Derive the `3^n` bound by assigning each account to outside the current state, inside the chosen subgroup, or inside the remainder. These bounds assume constant-cost integer arithmetic; very large integers add bit-length costs. No numeric maximum for `n` is supplied by the page.

用三种归属推导 `3^n`：账户不在当前状态中、在所选子组中、或在剩余集合中。上述分析假定整数运算为常数成本，超大整数需额外考虑位数成本。页面未给出 `n` 的具体上限。

## Pitfalls and variants / 常见坑与变体

- **Greedy is not proof / 贪心不是最优证明：** Try balances `+8, +7, +5, -12, -8`. Largest-first pairing uses four transfers, while the cancelling pair and remaining zero-sum triple admit three. This is a teaching example, not a source-page example. / 试验余额 `+8, +7, +5, -12, -8`。最大值优先配对会使用四笔；相消的一对与剩余零和三元组可以用三笔。这是教学自拟示例，不是原题示例。
- **Do not sort timestamps unnecessarily / 不必额外排序时间戳：** Part 1 asks for a final sum over one day, not chronological replay with intermediate constraints. / 第一部分求同一天的最终和，不是带中间约束的时间顺序重放。
- **Keep contracts separate / 区分前提：** Part 1 does not promise a zero total. Its first example sums to 40. Part 2 explicitly requires zero total. / 第一部分不保证总和为零，示例 1 总和为 40；第二部分明确要求零和。
- **Zeros and duplicates / 零与重复值：** Ignore zero accounts in the optimization. Equal balance values still represent distinct users; do not discard one merely because its value repeats. / 优化中忽略零余额；相同余额仍对应不同用户，不能按数值去重。
- **Numeric precision / 数值精度：** Preserve the integer model. In a currency variant use integer minor units or exact decimals, not floating-point equality. / 保持整数模型；货币变体使用整数最小货币单位或精确十进制，避免浮点数判零。
- **Mask errors / 掩码错误：** Candidate groups must be non-empty subsets of the remaining mask and include the anchor. The remainder must exclude exactly that group. / 候选组必须是剩余掩码的非空子集且包含固定账户，剩余状态必须恰好移除该组。
- **Output boundary / 输出边界：** The title mentions a plan, but the required return is a count. A variant requesting actual transfers needs user IDs, recorded partition choices, and an internal debtor-to-creditor construction. / 标题提到方案，但要求返回次数。若变体要求实际转账清单，则需保留用户 ID、记录划分选择，并在各组内构造债务人向债权人的转账。
- **Changed objectives / 目标变更：** Fees, forbidden pairs, per-transfer limits, or a large `n` change the problem. Do not assume this subset method or its guarantees still apply. / 手续费、禁止配对、单笔限额或很大的 `n` 都会改变问题，不能直接沿用此方法及其保证。

Suggested self-checks / 建议自查：empty records; a user's deltas cancelling to zero; a user becoming non-zero again after an intermediate zero; empty/all-zero balances; one opposite pair; repeated balances; multiple independent groups; the greedy counterexample above. Verify conservation and the transfer-count bound `1 ≤ answer ≤ n - 1` for non-empty valid Part 2 inputs. / 空记录、用户变化量相消、中途为零后再次非零、空或全零余额、一对相反余额、重复余额、多个独立组、上述贪心反例。非空且有效的第二部分输入应满足守恒，并有 `1 ≤ 答案 ≤ n - 1`。
