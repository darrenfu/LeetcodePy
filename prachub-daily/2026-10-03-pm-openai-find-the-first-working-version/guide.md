# Find the First Working Version — Guided Report / 引导报告

Source / 来源: [PracHub](https://prachub.com/coding-questions/find-the-first-working-version), both Description parts / 两部分题面。This is an independently written learning guide, not the site's solution. / 本文为独立编写的学习引导，并非网站答案。

## Problem restatement / 题目重述

**EN:** Normalize each version into three integers, padding missing components with zero. Working versions form a suffix in numeric lexicographic order, starting at the supplied `works_from` threshold. Part 1 asks for the first qualifying **original list element**. Part 2 asks for the first qualifying **existing triple**, returned in three-component form, without flattening the grouped catalog. The threshold itself need not exist in the input. Here the API is imaginary: the threshold is explicitly supplied.

**中文：** 将版本规范化为三个整数，缺省分量补零。按整数三元组的字典序，可用版本从给定阈值 `works_from` 开始构成后缀。第一部分返回第一个符合条件的**原始列表元素**；第二部分返回第一个符合条件的**已存在三元组**，输出三分量字符串，且不能展开整个目录。阈值本身不一定出现在输入中。本题 API 是假想接口，输入已直接提供阈值。

Before writing, state what “earliest” means when `['12', '12.0', '12.0.0']` all compare equal. / 动手前说明：当 `['12', '12.0', '12.0.0']` 比较结果相等时，“最早元素”应指什么？

## Hints（三级提示，由模糊到具体）

### Level 1 / 一级：Recognize the shape / 观察形状

**EN:** Write down several normalized versions and mark each as working or not working. How many transitions can appear? In a grouped catalog, which component decides the comparison before the other components matter?

**中文：** 写出若干规范化版本，标记是否可用。结果最多发生几次真假切换？在分组目录中，哪个分量会先决定大小，使剩余分量不再影响比较？

### Level 2 / 二级：Choose the boundary / 选择边界

**EN:** Part 1 is a search for the first value greater than or equal to a threshold, not an arbitrary equal match. For Part 2, locate a candidate major group, then reason separately about “equal to threshold major” and “strictly greater.” Repeat that distinction for minor. A greater prefix frees you from all lower-component thresholds.

**中文：** 第一部分要找第一个大于或等于阈值的位置，而不是任意一个相等位置。第二部分先定位候选 major，区分“等于阈值 major”和“严格更大”；minor 也如此。一旦高位前缀更大，就不再受后续分量阈值限制。

### Level 3 / 三级：Handle exhaustion / 处理耗尽

**EN:** Use a lower-bound search in each ordered list you actually need. If the equal major/equal minor branch has no sufficient patch, inspect the next existing minor's smallest patch. If that major offers no answer, inspect the next existing major's smallest minor and patch. Do not invent missing versions or retain the old patch/minor threshold after advancing a higher component.

**中文：** 对实际需要访问的有序列表做 lower-bound 搜索。若相同 major、相同 minor 下没有足够大的 patch，考虑下一个已存在 minor 的最小 patch；若该 major 无答案，考虑下一个已存在 major 的最小 minor 与 patch。不能虚构缺失版本，也不能在高位前进后继续沿用旧的低位阈值。

## Invariants / 关键不变量

**EN:**

- Normalization preserves numeric version semantics: compare major, then minor, then patch; equal triples represent equal values.
- For a half-open lower-bound search `[lo, hi)`, every index before `lo` is too small; every index at or after `hi` within the list qualifies. The unknown boundary lies between them, allowing the end-of-list sentinel.
- Each update must preserve those facts and strictly reduce `hi - lo`. At termination, the boundary is the first qualifying index or the sentinel.
- In Part 2, all groups skipped before the candidate are too early or have been proved unable to contain an answer. A strictly greater major makes its smallest existing descendant sufficient; an equal major with a strictly greater minor does likewise for that minor's smallest patch.
- Non-empty child lists guarantee that the smallest descendant exists once an eligible group is selected.

**中文：**

- 规范化保留整数版本语义：先比 major，再比 minor，最后比 patch；相同三元组表示相同版本值。
- 半开区间 lower-bound 搜索 `[lo, hi)` 中，`lo` 之前都太小，列表中 `hi` 及之后都符合条件；未知边界位于二者之间，并允许取列表末尾哨兵。
- 每次更新必须保持上述结论，并严格缩小 `hi - lo`。终止位置即第一个符合条件的下标或末尾哨兵。
- 第二部分跳过的分组要么太早，要么已证明不含答案。major 严格更大时，其最小已存在后代就符合条件；major 相等而 minor 严格更大时，该 minor 的最小 patch 同样符合条件。
- 子列表非空，保证选定合格分组后存在最小后代。

Proof exercise / 证明练习：Explain both why the returned version works and why no earlier existing version can work. / 分别说明返回版本为何可用，以及为什么更早的已存在版本都不可用。

## Data structure / 数据结构选择与理由

**EN:** Keep the given random-access lists. Parse the threshold once into an integer triple. In Part 1, normalize only the versions inspected during search; retain the original string for the return value. In Part 2, search major/minor keys directly in the nested records and patch numbers directly in their list. No heap, tree, dictionary, copied key arrays, or flattened catalog is needed. A conceptual `LOWER_BOUND_BY_KEY` helper can search records without materializing all keys.

**中文：** 保留输入的可随机访问列表。阈值只解析一次，得到整数三元组。第一部分只规范化搜索访问到的版本，返回时保留原字符串。第二部分直接搜索嵌套记录中的 major/minor 键及 patch 列表。无需堆、树、字典、复制的键数组或展开目录。概念上的 `LOWER_BOUND_BY_KEY` 可以直接按记录键搜索，不必构造完整键数组。

## Algorithm / 算法步骤

### Part 1 / 第一部分

1. Normalize the threshold. / 规范化阈值。
2. Search for the first normalized list value at least that threshold. Derive the two boundary updates from the invariant yourself. / 搜索第一个规范化后不小于阈值的元素；自行根据不变量推导两个边界更新。
3. Distinguish a valid index from the end sentinel; preserve the original spelling. / 区分有效下标和末尾哨兵；保留原始写法。

Pseudocode skeleton / 伪代码骨架（intentional gaps / 有意留空）：

```text
threshold ← NORMALIZE(works_from)
[lo, hi) ← full index range
while unresolved boundary remains:
    mid ← choose midpoint
    qualifies ← compare NORMALIZE(versions[mid]) with threshold
    TODO: update one boundary while preserving the invariant
TODO: map the final boundary to an original element or no answer
```

### Part 2 / 第二部分

1. Normalize the threshold and locate the first major not below it. / 规范化阈值，定位第一个不小于阈值 major 的分组。
2. A larger major needs only its smallest existing descendant. An equal major needs a minor lower bound. / major 更大时只需最小已存在后代；major 相等时继续定位 minor 的下界。
3. A larger minor needs only its smallest patch. An equal minor needs a patch lower bound. / minor 更大时只需最小 patch；minor 相等时继续定位 patch 的下界。
4. If a lower-level search is exhausted, advance to the next existing parent-level candidate and choose its smallest descendants. Derive the fallback order and bounds checks. / 低层搜索耗尽时，移至父层的下一个已存在候选，并选择其最小后代；自行推导回退顺序及越界检查。
5. Format an actual catalog triple as `major.minor.patch`, or report no answer. / 将真实存在的目录三元组格式化为 `major.minor.patch`，或报告无答案。

```text
threshold ← NORMALIZE(works_from)
major_candidate ← LOWER_BOUND_BY_KEY(catalog, threshold.major)
TODO: handle no candidate, greater major, and equal major
    minor_candidate ← LOWER_BOUND_BY_KEY(selected minors, threshold.minor)
    TODO: handle greater minor, equal minor, and exhausted minors
        patch_candidate ← LOWER_BOUND(selected patches, threshold.patch)
        TODO: handle a found patch or carry to the next existing group
TODO: format the selected existing triple, or report no answer
```

Fill these gaps only after tracing both official examples and a case that advances to another major. / 先手动追踪两个官方示例，再追踪一个需要跨 major 的例子，之后才补全空缺。

## Complexity / 复杂度

**EN:** Let `n` be the flat-list size, `L` the maximum version-string length. On-demand normalization gives Part 1 `O(L log(n + 1) + L)` time and `O(L)` temporary parsing space, or `O(log(n + 1))` time and `O(1)` space under the given bounded component sizes. Normalizing the entire input first instead costs `O(nL)` time and extra storage.

For Part 2, let `M` be the number of major groups, `m` the number of minors in the threshold-equal major actually searched, and `p` the patches in the threshold-equal minor actually searched; use zero for an unvisited level. Time is `O(L + log(M + 1) + log(m + 1) + log(p + 1))`; advancing to the next existing group takes constant work because child lists are non-empty. Auxiliary space is `O(L)` for parsing/formatting, constant under the stated bounds, without storage proportional to the catalog. These bounds assume random access and key searches without copying lists.

**中文：** 设扁平列表长度为 `n`，最长版本字符串长度为 `L`。按需规范化时，第一部分时间为 `O(L log(n + 1) + L)`，临时解析空间为 `O(L)`；按题目限定的分量大小，将字符串长度视为常数时，分别为 `O(log(n + 1))` 和 `O(1)`。若先规范化整个输入，则需 `O(nL)` 时间及额外存储。

第二部分设 major 分组数为 `M`，实际搜索的阈值相等 major 下 minor 数为 `m`，实际搜索的阈值相等 minor 下 patch 数为 `p`；未访问层记为零。时间为 `O(L + log(M + 1) + log(m + 1) + log(p + 1))`。子列表非空，移至下一个已存在分组只需常数操作。解析与格式化辅助空间为 `O(L)`，按给定范围视为常数，且不需与目录大小成比例的存储。以上假设列表可随机访问，按键搜索时不复制列表。

## Pitfalls and variants / 常见坑与变体

- **Numeric order / 数值顺序:** String comparison misorders `'10'` and `'2'`, or `'1.10'` and `'1.2'`. Parse integers; do not use floating point. / 字符串比较会排错这些版本；解析整数，不要转浮点数。
- **Padding and ties / 补零与相等:** Pad to three components before comparing. Part 1 does not forbid equivalent duplicates, so search the first qualifying position. / 比较前补齐三分量；第一部分未禁止等价重复版本，要找第一个符合条件的位置。
- **Return contract / 返回约定:** Part 1 preserves the input string; Part 2 always emits three components. Both may return `None` despite the site's `str` reference annotation. / 第一部分保留原字符串，第二部分总是输出三分量；两部分都允许 `None`，别被网站类型标注误导。
- **Sparse catalogs / 稀疏目录:** The next existing patch/minor/major need not be the current number plus one. The threshold need not exist. Never fabricate a triple. / 下一个已存在编号不一定是当前值加一；阈值可能不存在，不能虚构三元组。
- **Threshold reset / 阈值重置:** After moving to a greater minor, take its smallest patch even if below the old patch threshold. After moving to a greater major, take its smallest minor and patch. / minor 前进后选最小 patch，即使低于旧阈值；major 前进后选最小 minor 和 patch。
- **Boundary checks / 边界检查:** Trace empty input, all working, none working, exact equality, absent threshold major/minor, exhausted patches, exhausted minors, and the final major. / 手推空输入、全部可用、全部不可用、恰好相等、阈值 major/minor 缺失、patch 耗尽、minor 耗尽及最后一个 major。
- **Variant: black-box API / 变体：黑盒 API:** If only an expensive monotonic `works` API is available, search by its boolean response and count calls separately; the supplied-threshold comparison shortcut is unavailable. / 若只有昂贵的单调 API，按返回布尔值搜索，并单独统计调用次数；不能再直接用已知阈值比较。
- **Variant: changed guarantees / 变体：保证改变:** Non-monotonic working status invalidates binary search. Unsorted input requires ordering work; empty child groups require additional navigation logic. Full semantic-version prerelease/build rules are outside this numeric-only statement. / 可用状态非单调时二分失效；无序输入需额外排序，空子分组需额外导航逻辑；完整语义版本的预发布及构建标记规则不属于本题。
