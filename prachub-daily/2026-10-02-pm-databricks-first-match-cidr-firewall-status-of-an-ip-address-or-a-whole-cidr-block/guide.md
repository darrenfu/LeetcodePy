# First-Match CIDR Firewall: Status of an IP Address or a Whole CIDR Block — Guided Report / 引导报告

Source / 来源: [verified problem](https://prachub.com/coding-questions/first-match-cidr-firewall-status-of-an-ip-address-or-a-whole-cidr-block). Read [question.md](question.md) first. / 请先读题面。本报告为独立教学推导，不是网站 Solution 的转载。

For Darren: try each hint before opening the next. The skeleton deliberately leaves parsing, event handling, and winner selection to you. / Darren，请逐级阅读提示并先自己尝试。骨架刻意留空解析、事件处理和规则选择，不包含可直接提交的完整代码。

## Problem restatement / 题目重述

**EN:** Define the decision for one address first: among rules containing it, choose the smallest original index, or default to DENY. A CIDR query asks whether this decision is ALLOW everywhere in its range. The range may contain billions of addresses, while at most 100,000 rules describe where decisions can change.

**中文：** 先定义单点状态：在覆盖该地址的规则中，选原始下标最小者；没有则默认拒绝。CIDR 查询问的是范围内是否处处允许。范围可能包含数十亿个地址，但只有至多十万条规则决定状态在哪里可能变化。

Before coding, explain why reversing two overlapping rules can change the answer, and why checking only a block's endpoints is insufficient. / 写代码前，先说明为什么交换两条重叠规则可能改变答案，以及为什么只检查目标块两端不够。

## Hints（三级提示，由模糊到具体）

### Level 1 / 第一级：换一种表示

**EN:** Which parts of an IPv4 string represent significance rather than text? Could a prefix be represented by a continuous interval? For the whole-block query, do you need to inspect every address, or only places where rule membership can change?

**中文：** IPv4 字符串中的哪些部分有数值位权？前缀能否表示为连续区间？查询整个块时，是否只需要考察规则覆盖集合可能变化的位置，而无须枚举地址？

### Level 2 / 第二级：优先级与分段

**EN:** Preserve the rule index as its priority. Between consecutive rule boundaries, the set of covering rules is constant. Therefore one winning rule describes the entire segment. CIDRs are disjoint or nested, but multiple disjoint ALLOW prefixes can jointly satisfy a larger query.

**中文：** 把规则原始下标保留为优先级。相邻规则边界之间，覆盖规则集合不变，所以一条胜出规则就能决定整段。CIDR 之间不是不相交就是嵌套，但多个不相交的 ALLOW 前缀也可能共同满足一个更大的查询。

### Level 3 / 第三级：扫描线的状态

**EN:** Try half-open intervals. Clip each rule to the query, create entry/exit events for nonempty intersections, and sort the distinct boundaries. Keep active rules in a structure that exposes the smallest index. A min-heap plus an active flag per index supports lazy removal: an expired item can remain inside the heap until it reaches the top. An empty active set means DENY for any nonempty segment.

**中文：** 尝试半开区间。先把规则裁剪到目标范围，为非空交集创建进入和退出事件，再排序去重边界。用能返回最小下标的数据结构维护活动规则。最小堆配合每个下标的活动标记支持惰性删除：过期项可以留在堆内，直到成为堆顶再弹出。非空段上没有活动规则就意味着 DENY。

Exercise / 练习：For the `.7` DENY example, draw the boundaries around that singleton, then reverse the rule order. / 对 `.7` 被拒绝的示例画出单点两侧边界，再交换两条规则顺序。

## Invariants / 关键不变量

1. **Normalized coverage / 规范化覆盖。** Let `x` be the unsigned integer address and `p` the prefix length. Let `s = 2^(32-p)` and `L = floor(x/s) * s`; the represented set is `[L, L+s)`. Bare IPs use `p=32`. This clears host bits in rules and targets alike. / 令 `x` 为地址整数、`p` 为前缀长度。设 `s = 2^(32-p)`、`L = floor(x/s) * s`，该块就是 `[L, L+s)`；裸地址用 `p=32`。规则和目标的主机位都由此清零。
2. **First match / 首次匹配。** The winner at an address minimizes the original rule index, not prefix length, address order, or action. / 胜出者按规则原始下标最小来选，不能按前缀长度、地址顺序或动作选择。
3. **Constant segment / 段内恒定。** After processing all events at boundary `b`, the active set for `[b, next_b)` is exactly the rules containing that segment. No rule starts or ends inside it. / 处理边界 `b` 上全部事件后，活动集合恰好覆盖 `[b, next_b)`；段内没有规则开始或结束。
4. **Heap validity / 堆的有效性。** A rule is inserted once at its clipped start and marked inactive at its clipped end. After stale heap tops are removed, the top has the smallest active index. / 每条规则在裁剪后起点入堆一次，在终点标记失效；清理失效堆顶后，堆顶是最小活动下标。
5. **Universal acceptance / 全称条件。** Every visited nonempty segment must be allowed. One denied segment is a sufficient counterexample; reaching the query end without one proves ALLOW. / 每个访问到的非空段都必须允许。一个拒绝段就足以否定；若到达目标终点仍没有反例，就能证明整个目标允许。

Prove invariant 3 by considering one rule's start and end before reasoning about the heap. / 先用单条规则的起点、终点证明不变量 3，再证明堆如何选优先级。

## Data structure / 数据结构选择与理由

**EN:** For a bare address, start with an ordered rule list and a linear membership scan; no preprocessing index is necessary. For a large block, use a boundary-to-events mapping, sorted boundary array, active flags, and a min-heap keyed by original index. Keep actions in the original array. Include the query's own endpoints even if no rule touches them, so uncovered gaps remain visible.

**中文：** 单点查询先用有序规则列表线性扫描成员关系，不必建立查询索引。大块查询使用“边界 → 事件”的映射、已排序边界数组、活动标记和按原始下标排序的最小堆；动作保存在原列表。即使没有规则触及目标边界，也必须加入目标自身两端，避免遗漏未覆盖区域。

**EN:** The heap gives priority among overlapping rules; the events identify where that priority might change. Sorting intervals by start alone cannot preserve first-match semantics. A naive repeated interval-subtraction list can fragment and become quadratic. A binary prefix trie is a valid alternative, but it must track earliest rule indices and aggregate descendant coverage; an ordinary longest-prefix-match trie solves a different contract.

**中文：** 堆解决重叠规则之间的优先级，事件解决优先级在哪里可能变化。只按区间起点排序不能保证首次匹配语义。反复用普通列表做区间减法可能碎片化并退化为平方时间。二进制前缀 trie 可以作为另一种方向，但必须记录最早规则下标并汇总子树覆盖；普通最长前缀匹配 trie 对应不同的接口约定。

## Algorithm / 算法步骤

**EN steps:**

1. Normalize the target and each rule into half-open integer intervals, retaining rule indices and actions.
2. For a bare target, optionally use the simpler first-match linear scan.
3. For a block, intersect rules with the target. Discard empty intersections; build entry and exit events for the rest.
4. Add target endpoints, group events sharing a coordinate, and sort coordinates.
5. At each coordinate, apply all exits and entries before evaluating the following segment. Remove stale heap tops. Skip zero-length segments.
6. Determine the winning active action, using DENY if none exists. Stop at the first nonempty denied segment. Return ALLOW only after all target segments pass.

**中文步骤：**

1. 把目标和各条规则规范化为整数半开区间，保留规则下标和动作。
2. 裸地址可以使用更简单的首次匹配线性扫描。
3. 块查询中先计算规则与目标的交集，丢弃空交集，为其余交集建立进入、退出事件。
4. 加入目标两端，把同坐标事件分组并排序坐标。
5. 每个坐标先处理全部退出和进入事件，再评估右侧区间；清理失效堆顶，跳过零长度段。
6. 从活动规则中确定胜出动作，无活动规则则为 DENY。遇到第一个非空拒绝段即可停止；所有目标段通过后才返回 ALLOW。

Pseudocode scaffold / 伪代码骨架（TODOs are your implementation work / 留空处由你完成）：

```text
NORMALIZE(pattern):
    TODO: parse address and optional prefix
    TODO: clear host bits and produce half-open boundaries

STATUS(rules, target):
    query := NORMALIZE(target)
    TODO: choose point-scan or block-sweep path

    for each indexed rule in original order:
        TODO: normalize, clip to query, and register events
    TODO: include query boundaries and order event coordinates
    active, priority_heap := empty state

    for each boundary with a following boundary:
        TODO: apply every event at this boundary
        TODO: restore the valid-minimum heap invariant
        TODO: derive the following segment's decision
        TODO: reject a nonempty segment if it supplies a counterexample
    TODO: justify the final return from the universal-acceptance invariant
```

Self-check / 自检：After processing a coordinate, can you state exactly which interval you are about to evaluate? / 处理完一个坐标后，你能准确说出下一步评估哪个区间吗？

## Complexity / 复杂度

**EN:** Write `n` for total rules and `m ≤ n` for rules whose normalized intervals intersect the target. IPv4 width is fixed at 32, so parsing is constant work per pattern. A bare-address scan takes worst-case `O(n)` time and `O(1)` auxiliary space when parsing on demand. For the proposed sweep, clipping takes `O(n)`, sorting `O(m log(m+1))`, and each rule enters and leaves the heap at most once, also `O(m log(m+1))`. Total time is `O(n + m log(m+1))`, worst-case `O(n log n)`, with `O(m)` auxiliary space if nonintersecting rules are discarded. Retaining all normalized rules instead uses `O(n)` space. The bound depends on rules, not the number of addresses in the block.

**中文：** 设总规则数为 `n`，与目标相交的规则数为 `m ≤ n`。IPv4 固定为 32 位，每个模式解析为常数工作。单点按需解析扫描最坏时间 `O(n)`、额外空间 `O(1)`。扫描线裁剪时间 `O(n)`，排序时间 `O(m log(m+1))`，每条相交规则至多入堆、出堆各一次，堆操作同样为 `O(m log(m+1))`。总时间 `O(n + m log(m+1))`，最坏 `O(n log n)`；丢弃不相交规则时额外空间 `O(m)`。若保留所有规范化规则，则空间为 `O(n)`。复杂度取决于规则数，不依赖目标块里的地址数量。

## Pitfalls and variants / 常见坑与变体

| Check / 检查 | EN | 中文 |
|---|---|---|
| Rule order / 规则顺序 | Earlier ALLOW can shadow later DENY; DENY has no automatic priority. | 更早 ALLOW 可以遮蔽更晚 DENY；DENY 并非天然优先。 |
| Interior exception / 内部例外 | Allowed endpoints do not exclude a denied singleton inside. | 两端允许不排除中间存在被拒绝的单点。 |
| Collective coverage / 联合覆盖 | Two allowed /25 halves may satisfy a /24 query. | 两个允许的 /25 半块可以共同满足 /24 查询。 |
| Default / 默认 | Keep uncovered nonempty gaps; they evaluate to DENY. | 未覆盖的非空间隙必须保留，并判为 DENY。 |
| Host bits / 主机位 | `10.0.0.7/24` represents the same block as `10.0.0.0/24`, including in the target. | `10.0.0.7/24` 与 `10.0.0.0/24` 表示同一个块；目标也如此。 |
| Extreme prefixes / 极端前缀 | /0 spans `[0, 2^32)`; /32 is a singleton, not an empty interval. | /0 为 `[0, 2^32)`；/32 是单点，不是空区间。 |
| Arithmetic / 运算 | `2^32` is a valid exclusive endpoint. Avoid signed overflow, unbounded complement masks, and shifting a 32-bit word by 32. | `2^32` 是合法右开端点；避免有符号溢出、无限位取反掩码及对 32 位数移位 32 位。 |
| Event grouping / 事件分组 | Apply all events at a coordinate before checking its right-hand segment. Exiting rules cannot cover that segment. | 同坐标全部事件处理后才检查右侧段；退出规则不能覆盖右侧。 |
| Lazy deletion / 惰性删除 | An expired heap top must be removed repeatedly until the top is active or the heap is empty. | 连续弹出失效堆顶，直到堆顶有效或堆为空。 |
| Duplicate prefixes / 重复前缀 | Keep original indices distinct even if prefixes and actions repeat. | 即使前缀与动作重复，也要区分原始规则下标。 |

**EN practice checks:** Trace the source examples, then create cases for: an early /0 ALLOW followed by a narrower DENY; the reverse order; a gap between allowed pieces; a /32 query at `255.255.255.255`; and a target with nonzero host bits. Record expected results before implementation. For tiny ranges only, compare your future implementation against an independently written per-address first-match oracle.

**中文练习检查：** 手推题面示例，再构造：更早 /0 ALLOW 后跟更窄 DENY、交换它们顺序、允许片段中间有空隙、`255.255.255.255` 的 /32 查询、目标主机位非零。先写预期结果，再实现。只对很小的范围，用自行编写的逐地址首次匹配基准来比对未来实现。

**EN variants (not extra source requirements):** With many queries against fixed rules, consider preprocessing disjoint effective-action segments and indexing denied coverage. If rules can change dynamically, reassess update costs. IPv6 changes the bit width and integer representation. A three-way ALLOW/DENY/MIXED result or longest-prefix policy would change the contract and must be clarified separately.

**中文变体（不是本题新增要求）：** 若固定规则需要大量查询，可考虑预处理互不相交的最终动作段，并索引拒绝区域。若规则动态更新，重新评估更新代价。IPv6 会改变位宽及整数表示。三态 ALLOW/DENY/MIXED 返回值或最长前缀策略都会改变题意，需要另行明确。
