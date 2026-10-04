# Check if CIDR is fully canceled by rules — Darren's guide / 思路引导

Source / 来源: [verified PracHub question](https://prachub.com/coding-questions/check-if-cidr-is-fully-canceled-by-rules), full description read on 2026-10-04. Read one hint level at a time and implement the missing operations yourself. / 每次只读一级提示，自己实现缺失的操作。

## Problem restatement / 题目重述

**EN:** Track the addresses of the target that have not yet been canceled. An allow rule removes its overlap with that state. A deny rule fails immediately when it touches that state. Success requires an empty state and no earlier failure. Order affects the answer: allowing a whole target before denying it succeeds; reversing those two rules fails.

**中文：** 跟踪目标中尚未取消的地址。Allow 删除它与当前状态的交集；deny 一旦碰到当前状态就立即失败。成功需要状态为空，且之前没有发生失败。顺序会改变结果：先 allow 整个目标、再 deny 整个目标会成功；反过来会失败。

Before coding, explain why checking only the target's two endpoints is insufficient. / 写代码前，解释为什么仅检查目标的两个端点不够。

## Hints（三级提示，由模糊到具体）

### Level 1 — model the changing state / 第一级：明确变化的状态

**EN:** What is left after each rule? Can an address that disappears ever come back? Draw a short number line and remove a middle portion. How many pieces must the next rule inspect?

**中文：** 每条规则处理后还剩什么？已消失的地址会回来吗？画一条短数轴，删去中间一段。下一条规则需要检查几个片段？

### Level 2 — choose a representation / 第二级：选择表示方式

**EN:** An IPv4 address fits in an unsigned 32-bit integer. A CIDR describes a contiguous, aligned range. Keep only the remaining ranges, rather than enumerating individual addresses. The host bits of the supplied address must be cleared when finding the network's start. How would `/0` and `/32` behave?

**中文：** IPv4 地址可表示为无符号 32 位整数。一个 CIDR 对应连续且对齐的区间。只存剩余区间，不逐个枚举 IP。求网络起点时需要清掉输入地址的主机位。`/0` 和 `/32` 应该如何处理？

### Level 3 — derive one local transition / 第三级：推导单个片段的转移

**EN:** Use inclusive intervals `[L,R]`. Two intervals overlap exactly when `max(L,A) <= min(R,B)`. Subtracting one interval from another leaves zero, one, or two pieces. Sketch the no-overlap, full-removal, left-cut, right-cut, and middle-cut cases. Decide which endpoints move by one, and when a candidate piece is empty. Build a fresh list rather than modifying the list you are traversing.

**中文：** 使用闭区间 `[L,R]`。两区间相交的充要条件是 `max(L,A) <= min(R,B)`。一个区间减去另一个区间会留下零、一或两个片段。画出不相交、完全删除、切左边、切右边、切中间五种情况，自己确定哪些端点需要加一或减一，以及何时片段为空。构造新列表，不要边遍历边修改原列表。

## Invariants / 关键不变量

1. **Exact meaning / 精确含义:** Before each rule, the stored union equals the original target minus the union of earlier allow blocks, provided no earlier deny has already failed. / 每条规则执行前，若此前未被 deny 判失败，存储区间的并集恰好等于原目标减去此前所有 allow 地址块的并集。
2. **Representation / 表示:** Every stored interval is nonempty, inside the target, ordered by start, and disjoint from every other stored interval. / 所有区间非空、位于目标内、按起点排序且互不重叠。
3. **Monotonicity / 单调性:** Allow can only shrink the remaining set. Deny never restores or removes addresses; it only decides whether processing must stop. / Allow 只会缩小剩余集合；deny 不恢复或删除地址，只决定是否立即停止。
4. **Order / 顺序:** A deny must inspect the state produced by its predecessors. A later allow cannot rescue an earlier deny failure. / Deny 必须检查前序规则产生的状态；后来的 allow 不能补救先前 deny 导致的失败。

**Proof prompt / 证明练习:** Establish the invariants at initialization, show that subtraction preserves them, then connect them to both failure and final success. Explain why the empty state is absorbing, so early success is safe. / 证明初始化满足不变量、区间减法保持不变量，再说明它们如何支撑失败和最终成功。解释空状态为何是吸收状态，从而可以提前返回成功。

## Data structure / 数据结构选择与理由

**EN:** Start with a sorted list of disjoint integer intervals. It directly supports scanning for intersection and rebuilding the survivors after subtraction. It avoids expanding a `/0` into billions of addresses and avoids converting each surviving interval back into CIDRs. The output only asks for a boolean, so preserving CIDR notation internally is unnecessary.

**中文：** 优先使用按起点排序的互不相交整数区间列表。它方便扫描重叠，并在减法后重建剩余片段；避免把 `/0` 展开为数十亿个 IP，也不用把每个剩余区间重新拆回 CIDR。输出只需要布尔值，内部不必保留 CIDR 字符串形式。

**EN:** A set of individual IPs is too large. One bounding interval loses holes. A prefix trie or an ordered interval tree may help with many repeated queries or updates, but needs more machinery than this single target and at most 2000 rules require. Keep semantic rule order even if an index orders intervals spatially.

**中文：** 逐个 IP 的集合过大；单个包围区间会丢掉中间空洞。大量重复查询或更新时可考虑前缀树或有序区间树，但本题只有单个目标、最多 2000 条规则，列表更容易实现和证明。即使索引按地址排序，也必须保留规则的语义顺序。

## Algorithm / 算法步骤

**EN:** Derive and implement these operations independently:

1. Convert dotted IPv4 to an integer; turn each CIDR into its normalized inclusive network interval.
2. Initialize remaining state with the target interval.
3. Process rules in order. For deny, search all remaining pieces for any intersection and stop on failure. For allow, replace each piece with its surviving fragments.
4. Decide success from whether anything remains. Optionally stop once the state is empty.

**中文：** 分别推导并实现以下操作：

1. 把点分 IPv4 转成整数，再把 CIDR 转成规范化的网络闭区间。
2. 用目标区间初始化剩余状态。
3. 按顺序处理规则。Deny 检查所有剩余片段，发现交集立即失败；allow 将每个片段替换为减法后的残余片段。
4. 根据是否还有剩余区域决定成功；也可在状态变空后提前成功。

The skeleton deliberately leaves conversion, subtraction, and terminal decisions for Darren to fill in. / 骨架有意留出转换、减法及终止判断，由 Darren 完成。

```text
NORMALIZE_CIDR(cidr):
    TODO: parse address and prefix; clear host bits
    TODO: derive inclusive start and end; handle /0 and /32

SUBTRACT_ONE(piece, rule_interval):
    TODO: draw the five relative-position cases
    TODO: return only nonempty surviving pieces, in order

CHECK_TARGET(target, rules):
    remaining <- [NORMALIZE_CIDR(target)]
    for each rule IN INPUT ORDER:
        block <- NORMALIZE_CIDR(rule.cidr)
        if rule is deny:
            TODO: test overlap with the current remaining union
            TODO: apply immediate-failure semantics
        otherwise:
            next_remaining <- empty list
            for each piece in remaining:
                TODO: append SUBTRACT_ONE survivors
            remaining <- next_remaining
        TODO: consider safe early termination
    TODO: decide the final boolean from the invariant
```

## Complexity / 复杂度

**EN:** Let `n` be the number of rules and `k_i` the number of remaining intervals before rule `i`. A list scan takes `O(k_i)` per rule, for `O(n + sum(k_i))` time overall. Subtracting one contiguous rule interval increases the number of pieces by at most one: only a piece containing both cut boundaries can split into two. Thus `k_i <= i+1` with zero-based indexing, giving `O(n²)` worst-case time and `O(n)` auxiliary space, including the fresh replacement list. IPv4 width is fixed at 32 bits, so conversion is constant work per CIDR. This cost does not depend on the number of addresses in the target.

**中文：** 设规则数为 `n`，第 `i` 条规则前有 `k_i` 个剩余区间。每条规则扫描成本为 `O(k_i)`，总时间为 `O(n + sum(k_i))`。减去一个连续规则区间最多使片段数增加一：只有同时包含切割两端的片段才会裂成两个。因此使用从零开始的下标时 `k_i <= i+1`，最坏时间 `O(n²)`，辅助空间 `O(n)`，包含新建的替换列表。IPv4 固定为 32 位，每个 CIDR 转换成本视为常数。成本不随目标包含的 IP 数量增长。

## Pitfalls and variants / 常见坑与变体

| Check / 检查点 | Reason / 原因 |
|---|---|
| Deny against remaining state / Deny 检查剩余状态 | An already-canceled address cannot trigger a later failure. / 已取消地址不能触发后续失败。 |
| Never reorder rules / 不重排规则 | Merging all allows first changes the answer when a deny came earlier. / 先合并所有 allow 会改变前置 deny 的语义。 |
| Normalize host bits / 规范化主机位 | Noncanonical CIDRs still describe their full network. / 非规范地址仍表示整个网络。 |
| Inclusive endpoints / 闭区间端点 | A shared endpoint is overlap; subtraction must not leave the canceled endpoint behind. / 共享端点也是重叠；减法不能留下已取消端点。 |
| `/0`, `/32`, maximum IPv4 / 边界前缀与最大地址 | Fixed-width languages need care with shifts by 32 and overflow near `2^32-1`. / 固定位宽语言需注意移位 32 位及最大地址附近溢出。 |
| No rules / 空规则 | A valid target is nonempty; nothing cancels it. / 有效目标非空，没有规则就无法取消。 |
| Inspect every surviving piece / 检查全部剩余片段 | A deny may touch only the last piece after several splits. / 多次切割后 deny 可能仅碰到最后一个片段。 |

**Self-checks, not page examples / 自检用例，非页面示例:** Use target `10.0.0.0/24` unless stated otherwise.

- Allow the whole target, then deny it → `True`; reverse them → `False`. / 先完整 allow 再 deny 为真，反之为假。
- Allow `10.0.0.64/26`, then deny that same `/26` → no immediate failure, but final `False` because other addresses remain. / 先取消中间 `/26` 再 deny 同一段，不立即失败，但其他地址仍在，最终为假。
- After that middle removal, deny `10.0.0.200/32` → immediate `False`. / 删去中间段后 deny 最后片段中的单个地址，应立即失败。
- Duplicate allows, outside-target rules, noncanonical targets, and a `/32` target at `255.255.255.255` should all have deliberate tests. / 重复 allow、目标外规则、非规范目标、最大地址处 `/32` 目标都要刻意自检。

**Variants / 变体:** If the task asks for uncovered addresses, return the final interval collection after defining how deny failure is reported. IPv6 changes the width to 128 and requires corresponding arithmetic. A last-match-wins firewall, a default-allow firewall, or a request for the status of one IP has a different contract; derive its invariant anew. / 若要求未覆盖地址，可在明确 deny 失败如何报告后返回最终区间集合。IPv6 将位宽改为 128 并需要相应运算。最后匹配优先、默认允许的防火墙或单 IP 状态查询具有不同契约，需要重新推导不变量。
