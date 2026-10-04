# Find Minimum Compatible Version — Guided Practice / 引导练习

For Darren: read one hint level at a time, state the invariant aloud, then implement it yourself. The skeletons intentionally leave the search mechanics unfinished.

给 Darren：每次只读一级提示，先口述不变量，再自己实现。下方骨架刻意留空搜索细节。

Source / 来源：[question.md](question.md), including Read and Practice Parts 1–3. No executable solution is included. / 覆盖 Read 与 Practice 三部分，不包含可运行的完整解法。

## Problem restatement / 题目重述

| Part / 部分 | Given / 输入性质 | Return / 返回值 | Progression / 递进 |
| --- | --- | --- | --- |
| 1 | Strictly increasing integer versions; compatibility is globally `False…True`. / 整数版本严格递增，兼容性全局单调。 | Smallest compatible **version**, or `None`. / 最小兼容**版本值**，不存在则 `None`。 | Find a transition boundary. / 寻找转折边界。 |
| 2 | Only indices identify versions; the same global monotonicity holds. / 用索引标识版本，仍全局单调。 | Smallest compatible **index**, or `-1`. / 最小兼容**索引**，不存在则 `-1`。 | Keep the boundary search, account for expensive checks. / 保留边界搜索，关注昂贵检查次数。 |
| 3 | Lexicographically ordered triples; patch sequences and two levels of endpoint representatives are monotone. / 三元组按字典序排列，补丁序列及两层组尾代表序列单调。 | Lexicographically smallest compatible version, or `None`. / 字典序最小兼容版本，不存在则 `None`。 | Rebuild monotone search spaces at each level. / 在每层重新构造单调搜索空间。 |

All parts permit empty input. In Practice, the boolean list supplies the predicate results; treat each inspected entry as a conceptual expensive check. Part 2 specifies logarithmic time but gives no numeric call limit. Part 3 does not promise a globally monotone boolean array.

三部分都允许空输入。Practice 用布尔列表提供判定结果，可把每次读取视为一次昂贵检查。Part 2 要求对数时间，但没有给出具体调用额度；Part 3 不保证整个布尔数组单调。

## Hints（三级提示，由模糊到具体）

### Level 1 — Find the right question / 找对搜索目标

- **Part 1:** You need the earliest success, not just any success. What does one successful check tell you about earlier versions? / 你要的是最早成功项，不是任意成功项。一次成功检查对更早版本说明了什么？
- **Part 2:** Count predicate accesses separately from ordinary arithmetic. Can each answer eliminate many candidates? / 把判定访问次数与普通运算分开计数；一次回答能否排除大量候选？
- **Part 3:** A later minor may start with `False` even after an earlier minor ended with `True`. Which single version could tell you whether a whole group contains a success? / 较晚的 minor 开头可能是 `False`，即使较早 minor 结尾是 `True`。哪个版本能判断整个组内是否存在成功项？

### Level 2 — Boundary and representatives / 边界与代表项

- **Part 1:** Imagine a boundary `b` in `0…n`; `b = n` means no success. Search for that boundary by index, even when version numbers have gaps. / 想象边界 `b` 位于 `0…n`，`b = n` 表示全部失败。搜索索引边界，即使版本号有缺口。
- **Part 2:** There are `n + 1` possible boundaries. A boolean check supplies at most one bit of information. Think about a balanced decision tree and avoid repeated checks. / 有 `n + 1` 种边界位置，一次布尔检查至多提供一位信息。考虑平衡决策树，并避免重复检查。
- **Part 3:** For one `(major, minor)` block, inspect its last available patch. Then reason upward: can the last minor's representative summarize a major? / 对一个 `(major, minor)` 块检查最后一个实际存在的 patch。再向上推理：最后一个 minor 的代表能否概括整个 major？

### Level 3 — A route to implement / 可实现的路线

- **Part 1:** Use a first-true binary search. Choose one interval convention; derive both updates from its invariant. A `True` midpoint may still have an earlier `True` to its left. Map the final index to a version only after checking the sentinel. / 使用 first-true 二分，先选区间约定，再从不变量推导两种更新。中点为 `True` 时，左边仍可能存在更早的 `True`；最终先判断哨兵，再映射版本值。
- **Part 2:** Reuse that search, with one predicate access per iteration. Derive midpoint placement by balancing the remaining boundary possibilities. Do not scan, precheck both endpoints automatically, or check the final answer again without a reason. / 复用搜索，每轮只访问一次判定。通过平衡剩余边界候选推导中点；不要扫描、机械地先检查两端，或无理由地再次验证最终答案。
- **Part 3:** First index group boundaries using only version triples. Find the first successful major representative, then the first successful minor representative within that major, then the first successful patch within that minor. Prove each discarded group is entirely unsuccessful before coding. / 先仅用版本三元组建立分组边界。依次寻找第一个成功 major 代表、该 major 内第一个成功 minor 代表、该 minor 内第一个成功 patch。编码前先证明被丢弃的组全部失败。

## Invariants / 关键不变量

### Parts 1–2: preserve the first-true boundary / 保留首个 True 的边界

Let `b` be the first true index, or `n` if none exists. One useful convention keeps boundary candidates in the inclusive interval `[L, R]`, initially `[0, n]`. All real indices before `L` are known false; all real indices at or after `R` are known true. When `R = n`, that latter statement is vacuous: never query the sentinel.

令 `b` 为首个 True 的索引，全部失败时为 `n`。一种可用约定是让边界候选保持在闭区间 `[L, R]`，初始为 `[0, n]`。`L` 之前的真实索引均已知为 False；`R` 及其后的真实索引均已知为 True。`R = n` 时后一命题为空，绝不能查询哨兵。

For a real midpoint `m`, a false result implies `b > m`; a true result implies `b ≤ m`. Your updates must preserve `b`, strictly shrink the candidate interval, and stop when only one boundary remains. Derive the assignments yourself; do not mix this convention with a closed interval of actual array elements.

对真实中点 `m`，False 意味着 `b > m`，True 意味着 `b ≤ m`。更新必须保留 `b`、严格缩小候选区间，并在只剩一个边界时停止。具体赋值请自己推导；不要把这个约定与“闭区间里的真实数组元素”混用。

### Part 3: endpoint success is equivalent to group existence / 组尾成功等价于组内存在成功项

1. **Patch block:** With `False…True` patch monotonicity, a block contains a compatible version iff its last available patch is compatible. / **补丁块：** 由 `False…True` 单调性，块内存在兼容版本，当且仅当最后一个实际 patch 兼容。
2. **Major block:** Each minor endpoint represents existence in that minor. These representatives are monotone inside a major, so any successful minor exists iff the final minor endpoint succeeds. That endpoint is also the last version of the major. / **主版本块：** 每个 minor 的组尾代表该 minor 是否有解；这些代表在 major 内单调，因此存在成功 minor，当且仅当最后一个 minor 的组尾成功，而它正是该 major 的最后一个版本。
3. **Minimality:** The first successful major discards only wholly unsuccessful earlier majors. Repeat for minors; only then search patches. Lexicographic ordering makes this sequence produce the minimum triple. / **最小性：** 第一个成功 major 之前的 major 全部无解；对 minor 重复该推理，再搜索 patch。字典序保证逐层选择得到最小三元组。

This proof needs all three promises. Patch monotonicity alone does not make a major endpoint an existence witness.

该证明依赖三层保证。仅有 patch 单调性，不足以让 major 组尾代表整个 major 是否有解。

## Data structure / 数据结构选择与理由

**Parts 1–2:** Random-access arrays plus a few bounds suffice. Search indices, not version values. No copied boolean list, sorting, or tree is needed. / **Part 1–2：** 随机访问数组加几个边界变量足够。搜索索引而非版本值，无需复制布尔数组、排序或建树。

**Part 3:** Build an ordered major table; each major stores its ordered minor blocks. Store each minor as a half-open index range `[start, end)` into the original arrays. Its representative index is `end - 1`; a major's representative is the last minor's endpoint. Contiguous lexicographic groups make a single pass sufficient. Keep original indices so the predicate and version stay aligned.

**Part 3：** 建立有序 major 表，每个 major 保存有序 minor 块。每个 minor 用原数组的半开索引范围 `[start, end)` 表示，代表索引为 `end - 1`；major 的代表是最后一个 minor 的组尾。字典序让同组元素连续，一次扫描即可建表。保留原索引，确保判定与版本对应。

An optional cache keyed by original index avoids paying twice when a major endpoint, a minor endpoint, and a patch probe coincide. With real API calls, cache only if results are stable during the search. This cache is not required for correctness with the supplied lists.

可选缓存以原索引为键，避免 major 代表、minor 代表和 patch 探测重合时重复付费。真实 API 只有在搜索期间结果稳定时才适合缓存。题目提供的列表不需要缓存也能保证正确性。

## Algorithm / 算法步骤

### Part 1 — Establish the boundary primitive / 建立边界搜索原语

1. Handle empty input under the same no-answer convention. / 按无解约定处理空输入。
2. Initialize the boundary candidates and search using the invariant above. / 初始化边界候选，按上述不变量搜索。
3. Interpret the boundary: a real index maps to `versions[index]`; the sentinel maps to `None`. / 解释边界：真实索引映射到版本值，哨兵映射到 `None`。

```text
FIRST_TRUE_SKELETON(ordered items, predicate):
    establish boundary candidates, including a no-success sentinel
    while multiple boundary candidates remain:
        probe ← TODO: balance candidates without probing sentinel
        result ← evaluate predicate once
        TODO: retain exactly the boundary candidates consistent with result
    TODO: interpret the remaining boundary

PART_1:
    boundary ← FIRST_TRUE_SKELETON(version indices, compatibility)
    TODO: convert boundary into version value or None
```

### Part 2 — Account for calls / 核算调用次数

1. Reuse the same boundary primitive over indices. / 在索引上复用同一原语。
2. Record which indices were checked during a hand trace; ensure each loop adds at most one check. / 手推时记录检查索引，确保每轮最多一次检查。
3. Return the boundary index or translate the sentinel to `-1`. / 返回边界索引，或把哨兵转换为 `-1`。

```text
PART_2:
    boundary ← FIRST_TRUE_SKELETON(indices, counted compatibility probe)
    TODO: convert boundary into index or -1
    TODO: explain the worst-case decision depth
```

### Part 3 — Compose three valid searches / 组合三次合法搜索

1. Handle empty input; scan version keys to record majors and minor ranges without reading compatibility. / 处理空输入，仅扫描版本字段建立 major 和 minor 范围，不读取兼容性。
2. Search the major representative sequence. If none succeeds, return the no-answer result. / 搜索 major 代表序列；全部失败则返回无解。
3. Within the selected major, search its minor representative sequence. The existence invariant guarantees a successful minor. / 在选定 major 内搜索 minor 代表序列；存在性不变量保证有成功 minor。
4. Within that minor range, search its actual patch sequence. Convert the local boundary to the original index. / 在该 minor 范围内搜索实际 patch 序列，将局部边界转换为原索引。
5. Return the corresponding original version using the expected container format. / 按预期容器形式返回对应的原始版本。

```text
PART_3:
    groups ← TODO: build ordered ranges from version keys only
    chosen_major ← FIRST_TRUE_SKELETON(majors, compatibility at major endpoint)
    TODO: handle absence
    chosen_minor ← FIRST_TRUE_SKELETON(chosen major's minors,
                                      compatibility at minor endpoint)
    chosen_patch ← FIRST_TRUE_SKELETON(chosen minor's available patches,
                                      compatibility at original index)
    TODO: map selected patch back to the original version
```

Before implementing, trace Part 1 Example 1, Part 2's all-false example, and both Part 3 examples. Explain why Part 3 Example 1 may contain `True → False` without violating any promised monotonicity.

实现前手推 Part 1 示例 1、Part 2 全 False 示例，以及 Part 3 两个示例。解释为何 Part 3 示例 1 出现 `True → False` 仍不违反题目保证。

## Complexity / 复杂度

Let `n` be the number of versions. In Part 3 let `M` be the number of majors, `K` the total number of minor blocks, `m` the number of minors in the chosen major, and `p` the number of patches in the chosen minor.

令 `n` 为版本数。Part 3 中，`M` 为 major 数，`K` 为全部 minor 块数，`m` 为选中 major 内的 minor 数，`p` 为选中 minor 内的 patch 数。

| Part | Time / 时间 | Extra space / 额外空间 | Predicate checks / 判定次数 |
| --- | --- | --- | --- |
| 1 | `O(log(n + 1))` search / 搜索 | `O(1)` | `O(log(n + 1))` |
| 2 | `O(log(n + 1))` search / 搜索 | `O(1)` | A balanced boundary search can attain `ceil(log2(n + 1))` worst-case checks. / 平衡边界搜索可达该最坏次数。 |
| 3 | `O(n)` grouping, then `O(log(M + 1) + log(m + 1) + log(p + 1))` search / 分组后分层搜索 | `O(M + K)` group metadata / 分组元数据 | `O(log(M + 1) + log(m + 1) + log(p + 1))` |

For `n = 0`, return immediately with zero checks and constant time. Part 2 has `n + 1` possible outputs; a binary decision tree therefore needs at least `ceil(log2(n + 1))` checks in the worst case. This is a worst-case guarantee, not an optimality claim for every individual input or probability distribution. For the maximum Part 2 size, the bound is 20 checks.

`n = 0` 时立即返回，零次检查、常数时间。Part 2 有 `n + 1` 种可能输出，因此二叉决策树最坏至少需要 `ceil(log2(n + 1))` 次检查。这是最坏情况保证，不代表每个具体输入或概率分布下都最优；Part 2 最大输入规模对应 20 次。

Part 3's low API count does **not** imply logarithmic total time: building group metadata is linear. If each real predicate costs `C`, the single-query total is `O(n + C · (log(M + 1) + log(m + 1) + log(p + 1)))`. A cache adds space proportional to distinct probes. Repeated queries on a fixed catalog can reuse group metadata, but reusing compatibility requires stable results.

Part 3 API 次数少**不等于**总时间为对数：建组是线性的。若每次真实判定成本为 `C`，单次查询总成本如上。缓存空间与不同探测索引数成正比。固定目录的多次查询可复用分组，但复用判定结果需要稳定性保证。

## Pitfalls and variants / 常见坑与变体

- **Return contracts differ.** Part 1 returns a value, Part 2 an index; their no-answer markers differ. Part 3's displayed annotation is `list[int]`, but its prose explicitly allows `None`, and examples show tuples. Preserve the required semantics and confirm the judge's container expectation. / **返回契约不同。** Part 1 返回值，Part 2 返回索引，无解标记也不同。Part 3 注解为 `list[int]`，文字允许 `None`，示例使用元组；保持语义并确认判题器对容器的要求。
- **Do not stop at the first successful probe.** It is evidence for an upper boundary, not necessarily the minimum. / **遇到成功探测不能立即结束。** 它能限制边界，但未必是最小项。
- **Sentinel and progress bugs.** Test empty input, one false, one true, all false, all true, success only at the last entry, and gaps in version numbers. Every update must reduce uncertainty. / **哨兵和推进错误。** 手测空输入、单 False、单 True、全 False、全 True、仅末项成功和版本号有缺口；每次更新必须缩小不确定范围。
- **Representatives mean last available versions.** Groups may have uneven sizes and missing numeric major/minor/patch values. Do not invent versions, assume a dense grid, or use the first patch as an existence witness. / **代表是最后一个实际版本。** 分组可不等长，数字可有缺口；不能虚构版本、假设稠密网格，或用首个 patch 代表组内是否有解。
- **Local and global indices differ.** A selected minor's patch offset must map back to the original arrays. Major and minor tables preserve numeric order, not string order such as `"10" < "2"`. / **局部和全局索引不同。** minor 内 patch 偏移必须映射回原数组；分组保持数值顺序，不采用字符串排序。
- **Never flatten Part 3 into one compatibility search.** Try two minor blocks with `[False, True]` each: the flat sequence resets, while both endpoint representatives are true. / **不要把 Part 3 展平后二分兼容性。** 两个 minor 块各为 `[False, True]` 时，整体发生回落，两个组尾代表却都为 True。
- **If an upper-level promise disappears:** retain searches only where monotonicity remains. For example, patch-only monotonicity allows scanning minor blocks in lexicographic order and searching inside the first successful block; it does not justify binary-searching major representatives. / **若上层保证被取消：** 只在仍单调的序列上二分。例如仅有 patch 单调性时，可按字典序扫描 minor 块，在首个有解块内搜索，不能直接二分 major 代表。
- **Budget variants:** A strict budget below the decision-tree lower bound cannot guarantee an exact answer for every monotone input. If success is expected very early and the catalog has unknown extent, exponential probing followed by boundary search is a separate variant; derive its calls and bounds rather than assuming it improves this finite-array task. / **预算变体：** 预算低于决策树下界时，无法保证对所有单调输入给出精确答案。若成功通常很早且目录长度未知，可讨论指数探测再二分；需另行推导调用次数和边界，不能默认它更适合本题有限数组。
- **Production variants:** Changing API results, failures, and prerelease/build identifiers are outside the supplied model. Agree on a stable snapshot, error policy, and ordering before adapting the algorithm. / **真实系统变体：** API 结果变化、请求失败及预发布/构建标识超出题目模型；扩展前需明确稳定快照、错误策略和排序规则。

Self-check / 自检：Can you justify every skipped interval, prove endpoint/existence equivalence, distinguish API calls from preprocessing, and explain each return marker—before writing code? / 写代码前，你能否证明每段跳过区间无解、说明组尾与存在性等价、区分 API 调用和预处理，并解释所有返回标记？
