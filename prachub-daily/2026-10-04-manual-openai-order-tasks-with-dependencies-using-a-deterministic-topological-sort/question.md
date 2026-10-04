# Question / 题目资料

- Company / 公司：OpenAI
- Title / 标题：Order Tasks with Dependencies Using a Deterministic Topological Sort
- Difficulty / 难度：medium / 中等
- Category / 分类：Coding & Algorithms / 编程与算法
- Topics / 主题：Graphs; Heaps & Priority Queues / 图；堆与优先队列
- Role / 职位：Software Engineer
- Round / 轮次：Technical Screen
- Question date / 题面日期：Not provided by MCP / MCP 未提供
- Attempt count / 做过人数：Not provided by MCP / MCP 未提供
- Retrieval date / 取题日期：2026-10-04
- Original URL / 原题链接：https://prachub.com/coding-questions/order-tasks-with-dependencies-using-a-deterministic-topological-sort
- URL returned by MCP / MCP 返回链接：https://prachub.com/interview-questions/order-tasks-with-dependencies-using-a-deterministic-topological-sort
- Source / 来源：PracHub MCP search_questions → exact OpenAI title match → get_question(include_solution=false).
- Scope / 范围：The English prompt below preserves all returned prompt sections, including starter stubs and source hints; quota footer omitted. No model solution was requested. / 下方英文保留 MCP 返回的全部题面章节，包括起始代码占位和原始提示；省略额度页脚，未请求参考解法。

## English original / 英文原文

# Order Tasks with Dependencies Using a Deterministic Topological Sort
OpenAI · Software Engineer · Technical Screen · Coding & Algorithms · medium · General
Topics: Graphs, Heaps & Priority Queues
https://prachub.com/interview-questions/order-tasks-with-dependencies-using-a-deterministic-topological-sort

Tasks have prerequisite tasks and form a directed acyclic graph. Return a valid execution order in which each task appears after all its prerequisites.

For this exercise, task IDs are integers and ties are resolved by returning the lexicographically smallest valid order. The task-ID representation and tie rule make the dependency-ordering follow-up deterministic.

### Function Signature

`order_tasks(n: int, dependencies: list[list[int]]) -> list[int]`

### Input

Tasks are numbered from `0` through `n - 1`. Each pair `[task, prerequisite]` means `prerequisite` must occur before `task`.

### Output

Return all task IDs exactly once in the lexicographically smallest valid order. Lexicographic comparison uses integer values at the first differing position. Return an empty list when `n` is zero.

### Constraints

- `0 <= n <= 100000`.
- `0 <= len(dependencies) <= 200000`.
- Every referenced task ID is in `[0, n)`.
- There are no repeated dependency pairs or self-dependencies.
- The graph is guaranteed to be acyclic.

### Examples

Input: `n = 4, dependencies = [[2,0],[2,1],[3,1]]`

Output: `[0,1,2,3]`

Input: `n = 4, dependencies = [[0,2],[1,2]]`

Output: `[2,0,1,3]`

Input: `n = 3, dependencies = []`

Output: `[0,1,2]`

Input: `n = 0, dependencies = []`

Output: `[]`

## Lexicographically Smallest Task Execution Order (Medium)

You are scheduling n tasks numbered from 0 through n - 1. Some tasks cannot begin until other tasks have finished.

Each element of dependencies is a pair [task, prerequisite], which means that prerequisite must occur before task. The dependency graph is guaranteed to be acyclic, so at least one valid execution order always exists.

Return a list that contains every task ID from 0 through n - 1 exactly once, ordered so that each task appears after all of its prerequisites. Several valid orders may exist; return the lexicographically smallest one. Lexicographic comparison scans the two orders position by position and prefers the order whose integer value is smaller at the first position where they differ. Return an empty list when n is zero.

Example 1:
Input: n = 4, dependencies = [[2, 0], [2, 1], [3, 1]]
Output: [0, 1, 2, 3]
Explanation: Task 2 must come after tasks 0 and 1, and task 3 must come after task 1. Tasks 0 and 1 are free at the start, and 0 is the smaller of them; after both are placed, tasks 2 and 3 are free and 2 is smaller.

Example 2:
Input: n = 4, dependencies = [[0, 2], [1, 2]]
Output: [2, 0, 1, 3]
Explanation: Tasks 0 and 1 both require task 2, so only tasks 2 and 3 are free at the start. Taking the smaller free task, 2, releases 0 and 1, and the remaining free tasks are then taken in increasing order.

All task IDs fit comfortably in a 32-bit signed integer; no value in the input or the output exceeds 2^31 - 1.

### Constraints
- 0 <= n <= 100000.
- 0 <= len(dependencies) <= 200000.
- Every referenced task ID is in [0, n).
- There are no repeated dependency pairs or self-dependencies.
- The graph is guaranteed to be acyclic.
- Each dependency is a pair [task, prerequisite] meaning prerequisite must occur before task.
- All values fit in a 32-bit signed integer; no value exceeds 2^31 - 1.

### Examples
- Input: `(0, [])` → Output: `[]` — Minimum valid input: zero tasks produce an empty order.
- Input: `(1, [])` → Output: `[0]` — Singleton: the only task has no prerequisites.

### Sample tests
- Input: `(0, [])` → Output: `[]` — Minimum valid input: zero tasks produce an empty order.
- Input: `(1, [])` → Output: `[0]` — Singleton: the only task has no prerequisites.

### Starter code
**python**
```python
def order_tasks(n, dependencies):
    raise NotImplementedError("Not implemented")
```
**java**
```java
class Solution {
    public java.util.List<Integer> order_tasks(int n, int[][] dependencies) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
```
**cpp**
```cpp
#include <vector>
#include <stdexcept>
class Solution {
public:
    std::vector<int> order_tasks(int n, const std::vector<std::vector<int>>& dependencies) {
        throw std::logic_error("Not implemented");
    }
};
```
**javascript**
```javascript
function order_tasks(n, dependencies) {
    throw new Error("Not implemented");
}
```

### Hints (interviewer only — reveal one at a time, and only when asked)
1. A task may be placed only once every one of its prerequisites has been placed. How many unplaced prerequisites does each task have at the start, and how does that count change as you place tasks?
2. At many steps more than one task is legal. The lexicographic rule compares orders at the first position where they differ, which pins down exactly which of the legal tasks you must place next.
3. Tasks that no pair mentions still belong in the output, and n can be zero.


## Chinese translation / 中文翻译

# 使用确定性拓扑排序安排有依赖关系的任务
OpenAI · 软件工程师 · 技术筛选面试 · 编程与算法 · 中等 · 通用
主题：图、堆与优先队列
https://prachub.com/interview-questions/order-tasks-with-dependencies-using-a-deterministic-topological-sort

任务具有前置任务，并构成一个有向无环图。返回一个有效执行顺序，使每个任务都出现在它的所有前置任务之后。

本题中，任务 ID 是整数；当存在多个有效顺序时，返回字典序最小的顺序。任务 ID 的表示方式和择优规则使这一依赖排序追问题具有确定的结果。

### 函数签名

`order_tasks(n: int, dependencies: list[list[int]]) -> list[int]`

### 输入

任务编号为 `0` 到 `n - 1`。每个数对 `[task, prerequisite]` 表示 `prerequisite` 必须出现在 `task` 之前。

### 输出

返回所有任务 ID，且每个 ID 恰好出现一次，顺序是所有有效顺序中字典序最小的。字典序比较依据第一个不同位置上的整数值。当 `n` 为零时，返回空列表。

### 约束

- `0 <= n <= 100000`。
- `0 <= len(dependencies) <= 200000`。
- 每个被引用的任务 ID 都位于 `[0, n)`。
- 不存在重复的依赖数对或自依赖。
- 保证图无环。

### 示例

输入：`n = 4, dependencies = [[2,0],[2,1],[3,1]]`

输出：`[0,1,2,3]`

输入：`n = 4, dependencies = [[0,2],[1,2]]`

输出：`[2,0,1,3]`

输入：`n = 3, dependencies = []`

输出：`[0,1,2]`

输入：`n = 0, dependencies = []`

输出：`[]`

## 字典序最小的任务执行顺序（中等）

你需要安排 n 个任务，编号从 0 到 n - 1。有些任务必须等其他任务完成后才能开始。

dependencies 的每个元素都是数对 [task, prerequisite]，表示 prerequisite 必须出现在 task 之前。保证依赖图无环，因此总是至少存在一种有效执行顺序。

返回一个列表，其中 0 到 n - 1 的每个任务 ID 恰好出现一次，且每个任务都出现在它的所有前置任务之后。可能存在多个有效顺序；请返回字典序最小的一个。字典序比较逐个位置扫描两个顺序，在第一个不同的位置上，整数值较小的顺序更优。当 n 为零时，返回空列表。

示例 1：
输入：n = 4, dependencies = [[2, 0], [2, 1], [3, 1]]
输出：[0, 1, 2, 3]
解释：任务 2 必须在任务 0 和 1 之后，任务 3 必须在任务 1 之后。开始时任务 0 和 1 都可以执行，0 更小；当它们都被放入顺序后，任务 2 和 3 都可以执行，其中 2 更小。

示例 2：
输入：n = 4, dependencies = [[0, 2], [1, 2]]
输出：[2, 0, 1, 3]
解释：任务 0 和 1 都依赖任务 2，所以开始时只有任务 2 和 3 可以执行。选择其中较小的任务 2 后，任务 0 和 1 被解锁，接下来每次从当前可执行任务中选择最小的任务。

所有任务 ID 都能用 32 位有符号整数表示；输入和输出中的任何值都不超过 2^31 - 1。

### 约束
- 0 <= n <= 100000。
- 0 <= len(dependencies) <= 200000。
- 每个被引用的任务 ID 都位于 [0, n)。
- 不存在重复的依赖数对或自依赖。
- 保证图无环。
- 每条依赖都是数对 [task, prerequisite]，表示 prerequisite 必须出现在 task 之前。
- 所有值都能用 32 位有符号整数表示；任何值都不超过 2^31 - 1。

### 示例
- 输入：`(0, [])` → 输出：`[]` —— 最小合法输入：零个任务产生空顺序。
- 输入：`(1, [])` → 输出：`[0]` —— 单个任务：唯一的任务没有前置任务。

### 样例测试
- 输入：`(0, [])` → 输出：`[]` —— 最小合法输入：零个任务产生空顺序。
- 输入：`(1, [])` → 输出：`[0]` —— 单个任务：唯一的任务没有前置任务。

### 起始代码
以下原始起始代码仅含未实现的占位，不是答案。

**python**
```python
def order_tasks(n, dependencies):
    raise NotImplementedError("Not implemented")
```
**java**
```java
class Solution {
    public java.util.List<Integer> order_tasks(int n, int[][] dependencies) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
```
**cpp**
```cpp
#include <vector>
#include <stdexcept>
class Solution {
public:
    std::vector<int> order_tasks(int n, const std::vector<std::vector<int>>& dependencies) {
        throw std::logic_error("Not implemented");
    }
};
```
**javascript**
```javascript
function order_tasks(n, dependencies) {
    throw new Error("Not implemented");
}
```

### 提示（原题标注：仅面试官可见；仅在被要求时逐条展示）
1. 只有当一个任务的所有前置任务都已被放入顺序后，才能放入该任务。每个任务开始时有多少个尚未放入顺序的前置任务？随着任务被放入，这个计数如何变化？
2. 在很多步骤中，不止一个任务可以合法地被选择。字典序规则比较两个顺序第一个不同的位置，因此能确定下一步必须选择哪个合法任务。
3. 即使某个任务没有出现在任何依赖数对中，它也必须出现在输出里；n 也可以为零。
