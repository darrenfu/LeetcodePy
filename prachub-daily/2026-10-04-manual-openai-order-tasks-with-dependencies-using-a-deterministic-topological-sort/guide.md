# Darren's guide / Darren 的解题引导

Read one hint level at a time and try implementing before opening the next. This guide contains reasoning and an incomplete pseudocode skeleton, not a submission.
建议每次只读一级提示，尝试实现后再看下一级。本报告给出推理和不完整的伪代码骨架，不提供可提交代码。

## Problem restatement / 题目重述

There are n integer task IDs, 0 through n − 1. A pair [task, prerequisite] requires prerequisite to appear first. Produce every ID exactly once, respecting all dependencies, and choose the lexicographically smallest valid order. The graph is a DAG; n = 0 returns []. Integer order matters, not string order.

共有 n 个整数任务 ID，范围是 0 到 n − 1。数对 [task, prerequisite] 要求 prerequisite 先出现。输出每个 ID 恰好一次，满足所有依赖，并在全部合法顺序中取字典序最小的一个。图保证无环；n = 0 返回 []。比较的是整数大小，不是字符串大小。

Before coding, explain why sorting all IDs fails for n = 4, dependencies = [[0,2],[1,2]]. Then identify the first legal choices and ask whether that set can change after one choice.
动手前，用 n = 4、dependencies = [[0,2],[1,2]] 说明为什么直接排序所有 ID 会失败。找出最初可选的任务，再思考选中一个后，可选集合会如何改变。

## Hints / 提示

### Level 1 — Eligibility / 一级：判断资格

Separate “legal to run now” from “preferred among legal tasks.” What information tells you that every prerequisite of a task has already appeared? Remember tasks that never occur in dependencies.
把“现在是否可以执行”和“在可执行任务中更偏好谁”分开思考。什么信息能表明一个任务的全部前置任务都已出现？别忘了从未出现在 dependencies 中的任务。

### Level 2 — Local choice / 二级：局部选择

Maintain the number of unfinished prerequisites for each task. Finishing a task should affect only tasks that directly depend on it. At the first differing position of two valid orders, what choice makes your prefix smaller?
维护每个任务尚未完成的前置任务数量。一个任务完成后，只应影响直接依赖它的任务。两个合法顺序在第一个不同的位置上，怎样选择才能让自己的前缀更小？

### Level 3 — Dynamic frontier / 三级：动态候选集合

Consider Kahn's topological traversal with a min-priority queue for all currently eligible IDs. Orient each edge prerequisite → task. When a remaining count becomes zero, that task joins the queue immediately, before the next selection. Work out the exact updates yourself.
考虑用 Kahn 拓扑遍历，并以最小优先队列管理所有当前可执行的 ID。每条边应为 prerequisite → task。当剩余计数变成零时，立即加入队列，再进行下一次选择。请自己写出具体更新操作。

Trace the second example by hand: initially eligible {2,3}; after choosing 2, the next candidate set is {0,1,3}. Explain why draining the original batch first gives the wrong tie-breaking behavior.
手动追踪第二个示例：初始候选为 {2,3}；选择 2 后，下次候选为 {0,1,3}。解释为什么先处理完旧的一批候选会违反择优规则。

## Invariants / 关键不变量

1. **Remaining count:** For every unplaced task, its count equals the number of incoming prerequisites that are still unplaced. Initialize from all edges; each completed prerequisite contributes exactly one decrement to each direct dependent.
   **剩余计数：** 对每个尚未输出的任务，计数等于尚未输出的入边前置任务数量。从全部边初始化；每个已完成的前置任务对每个直接后继恰好贡献一次递减。
2. **Eligible frontier:** Immediately before each selection, the priority queue contains exactly the unplaced tasks whose remaining count is zero, with each ID present once. New zero-count tasks enter at the transition to zero.
   **可执行集合：** 每次选择前，队列恰好包含剩余计数为零的所有未输出任务，每个 ID 仅出现一次。任务在计数变为零的瞬间进入集合。
3. **Valid prefix:** Every prerequisite of every task in the output prefix appears earlier in that prefix. Selecting from the zero-count frontier preserves this property.
   **合法前缀：** 输出前缀中每个任务的所有前置任务都已经在它之前出现。选择零计数候选能保持这个性质。
4. **Smallest prefix:** Suppose the prefix agrees with a lexicographically optimal order. That order's next task must be eligible. Choosing the smallest eligible ID cannot be worse at this position. It also admits a completion: deleting a zero-indegree vertex leaves a DAG. Induct on prefix length.
   **最小前缀：** 假设当前前缀与某个字典序最优顺序相同，该最优顺序的下一个任务一定可执行。选择当前最小可执行 ID，在这一位置不会更差；同时仍然能够完成排序，因为删除零入度顶点后剩余图仍是 DAG。对前缀长度做归纳。

Try explaining invariant 4 aloud without saying only “greedy works.” Distinguish feasibility from the lexicographic objective.
尝试口头解释不变量 4，避免只说“贪心是对的”。把可行性与字典序目标分别论证。

## Data structure / 数据结构选择与理由

- **Adjacency lists indexed by ID:** Store direct dependents of each prerequisite. This lets you touch only outgoing edges when completing a task; it avoids repeatedly scanning all dependencies.
  **按 ID 索引的邻接表：** 为每个前置任务保存直接后继。任务完成时只访问其出边，避免反复扫描全部依赖。
- **An n-entry remaining-count array:** IDs are dense, so an array is simple and gives constant-time access. Allocate for all n tasks, including isolated vertices.
  **长度为 n 的剩余计数数组：** ID 连续，数组简单且可常数时间访问。必须涵盖全部 n 个任务，包括孤立顶点。
- **A min-heap of eligible integer IDs:** The frontier changes during traversal. A FIFO queue can produce a valid topological order but does not guarantee the required smallest order; a heap supports dynamic minimum selection.
  **可执行整数 ID 的最小堆：** 候选集合在遍历中不断变化。普通 FIFO 队列能给出合法拓扑序，却不能保证本题的最小顺序；堆支持动态取最小值。
- **An output list:** Append each chosen ID once. Under the stated assumptions, remaining-count transitions already prevent duplicate insertion; a separate visited set is unnecessary.
  **输出列表：** 每次选择后追加该 ID 一次。在题目假设下，计数转为零的过程已经防止重复入队，无须额外 visited 集合。

## Algorithm / 算法步骤

1. Create graph and count entries for every ID. Interpret each [task, prerequisite] in the correct direction.
   为全部 ID 建立图和计数条目，按正确方向解释每个 [task, prerequisite]。
2. Build outgoing adjacency and initial remaining counts from dependencies.
   从依赖列表建立出边邻接表与初始剩余计数。
3. Collect every zero-count task into a min-heap.
   把全部零计数任务收集到最小堆中。
4. Repeatedly choose the smallest currently eligible task and append it. Update each direct dependent's remaining count; add a newly eligible task before choosing again.
   反复选择当前最小可执行任务并追加。更新各直接后继的剩余计数；在下次选择前加入新解锁的任务。
5. Return the order. For the guaranteed DAG, its length must be n; for n = 0, it is empty.
   返回顺序。对于保证无环的输入，长度必须为 n；n = 0 时自然为空。

Incomplete pseudocode skeleton — fill in the TODOs yourself.
不完整伪代码骨架——请自行补充 TODO。

```text
ORDER_TASKS(n, dependencies):
    outgoing, remaining ← TODO: initialize for every task ID
    TODO: translate dependency pairs into graph and counts
    ready ← TODO: construct a minimum-priority frontier
    order ← empty sequence

    while ready is not empty:
        current ← TODO: select according to the tie rule
        TODO: extend the valid prefix
        for each direct dependent of current:
            TODO: update its state and detect the eligibility transition

    TODO: verify the expected output length and return the order
```

Before implementing, draw the graph for [[2,0],[2,1],[3,1]], write its initial counts, and trace frontier/count updates after every choice.
实现前，画出 [[2,0],[2,1],[3,1]] 的图，写出初始计数，并记录每次选择后的候选集合与计数变化。

## Complexity / 复杂度

Let V = n and E = len(dependencies). Building graph/counts costs O(V + E). Each edge is updated once, and each task enters/leaves the heap at most once. Total time is O(E + V log(V + 1)); writing +1 keeps the bound meaningful for V = 0 or 1. Heapifying the initial eligible list costs O(V), though individual initial pushes also fit the total bound.

令 V = n、E = len(dependencies)。建图和计数耗时 O(V + E)。每条边只更新一次，每个任务最多入堆、出堆各一次。总时间为 O(E + V log(V + 1))；加 1 让 V = 0 或 1 时的表达也成立。对初始候选列表做 heapify 耗时 O(V)；即使逐个入堆，也不改变总时间上界。

Auxiliary space is O(V + E), including adjacency, counts, and frontier. The output occupies another O(V), leaving the same overall bound.
额外空间为 O(V + E)，包括邻接表、计数和候选集合。输出另占 O(V)，总体空间上界不变。

## Pitfalls and variants / 常见坑与变体

- **Reversed edges:** [task, prerequisite] is an edge prerequisite → task. Test a single dependency and state which ID must appear first.
  **边方向写反：** [task, prerequisite] 对应 prerequisite → task。用单条依赖测试，明确谁必须先出现。
- **Missing isolated tasks:** Initialize over 0..n−1, not only IDs seen in dependencies. Check n = 3 with no edges.
  **漏掉孤立任务：** 初始化要覆盖 0..n−1，而非仅覆盖依赖中出现的 ID。检查 n = 3 且没有边的情况。
- **Sorting only once or sorting batches:** Newly unlocked smaller IDs must compete immediately with older candidates. Revisit the {2,3} → {0,1,3} trace.
  **只排序一次或分批排序：** 新解锁的小 ID 必须立即与旧候选竞争。重新检查 {2,3} → {0,1,3} 的过程。
- **Enqueuing too early or twice:** A dependent becomes eligible only when all its prerequisites are done. Insert on the transition to zero; do not scan all zero counts after every step.
  **提前或重复入队：** 只有所有前置任务都完成后才能执行。在计数变成零时插入，避免每步扫描所有零计数任务。
- **Integer comparison:** IDs such as 2 and 10 must compare numerically. DFS postorder or a FIFO queue alone does not guarantee the specified optimum.
  **整数比较：** 2 和 10 必须按数值比较。仅用 DFS 后序或 FIFO 队列不能保证本题规定的最优顺序。
- **Cycle variant:** The original input is guaranteed acyclic. If that guarantee is removed, fewer than n processed vertices indicate a cycle; define an explicit error/result contract rather than treating a partial order as success.
  **有环变体：** 原题保证无环。若取消保证，处理数量少于 n 表示存在环；应明确错误或返回契约，不能把部分顺序当成功。
- **Duplicate-edge variant:** The original forbids repeated pairs. If duplicates become allowed, either deduplicate consistently or preserve multiplicity in both adjacency and counts; mixing the two breaks the invariant.
  **重复边变体：** 原题禁止重复数对。若允许重复，必须一致地去重，或让邻接表和计数同时保留重数；两者混用会破坏不变量。
- **Custom tie rule / uniqueness:** A different priority needs a well-defined comparison key. To investigate uniqueness, ask what it means if the eligible frontier contains multiple tasks at some step.
  **自定义择优规则／唯一性：** 改变优先级时需要明确定义比较键。若研究顺序是否唯一，可思考某一步候选集合出现多个任务意味着什么。

Self-checks / 自测：empty input; one task; no edges; a chain; one prerequisite unlocking several tasks; several prerequisites gating one task; disconnected components; a newly unlocked ID smaller than an existing candidate.
空输入；单任务；无边；依赖链；一个前置任务解锁多个任务；多个前置任务共同约束一个任务；不连通分量；新解锁 ID 小于已有候选。对每种情况自行写出期望顺序，再验证自己的实现。
