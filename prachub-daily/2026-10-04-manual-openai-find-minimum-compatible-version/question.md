# Find Minimum Compatible Version

- Company / 公司：OpenAI
- Category / 分类：Coding & Algorithms
- Difficulty / 难度：MEDIUM（Practice 分项：Easy / Medium / Hard）
- Question date / 题面日期：Mar 9, 2026
- People solved / 做过人数：183（用户提供的目标题快照；本次站内搜索卡片显示 0 people solved，未在 Read 详情页核实 183）
- Role / 岗位：Machine Learning Engineer
- Interview round / 面试轮次：Onsite
- Coding page last updated / 编程页更新时间：Apr 19, 2026
- Original question / 原题链接：https://prachub.com/interview-questions/find-minimum-compatible-version?view=text
- Practice / 输入输出、约束与示例来源：https://prachub.com/coding-questions/find-minimum-compatible-version
- Retrieved / 读取日期：2026-10-04（Chrome，kotime42@gmail.com，Premium Member）

存档说明：英文部分保留 Read 原题干及 Practice 三部分的完整题干、示例、约束和函数签名；中文部分随后翻译。仅做题面存档。第三部分的页面签名返回类型为 `list[int]`，题干同时允许 `None`，以下均照原页面保留。

## English original — Read

You are given a list of software versions sorted in ascending numeric order and an expensive predicate is_compatible(version). Return the minimum version that satisfies the requirement, or None if no version works.

The interview usually progresses through three parts:

Base version
The predicate is globally monotone: all earlier versions return False , and once a version returns True , all later versions also return True .
Find the first compatible version.
Call-budget version
Same monotonicity assumption as Part 1.
The interviewer tracks how many times you call is_compatible , so you should minimize API calls.
Layered-monotonic version
The global sequence is not necessarily monotone.
Versions are triples (major, minor, patch) .
For a fixed (major, minor) , compatibility over patch is monotone.
At the major and minor levels, representative checks allow you to binary-search candidate groups.
Use this layered monotonicity to find the minimum compatible version with few predicate calls.

The core skills are binary search, careful version ordering, and adapting search strategy when monotonicity only holds within subranges.


## English original — Practice

### Part 1: First Compatible Version

Part 1: Easy
OpenAI
Machine Learning Engineer
Quick Overview

This question evaluates binary search, monotonic predicates, careful version ordering, and cost-aware optimization of expensive compatibility checks. It is commonly asked in the Coding & Algorithms domain to test reasoning about monotonicity, minimizing API calls, and adapting search strategies when monotonicity holds only within subranges; the level of abstraction combines conceptual understanding of monotone properties with practical application of efficient search techniques.

You are given a sorted list of distinct integer software versions and a boolean list compatible of the same length. compatible[i] represents the result of an expensive predicate is_compatible(versions[i]).

The predicate is globally monotone: the values in compatible have the form False, False, ..., False, True, True, ..., True.

Return the smallest version that is compatible, or None if no version works.

#### Examples

##### Example 1

Input: `([100, 101, 102, 103, 104], [False, False, True, True, True])`

Output: `102`

Notes: The first compatible entry is at index 2, so the answer is version 102.

##### Example 2

Input: `([5, 7, 9], [False, False, False])`

Output: `None`

Notes: No version is compatible.

#### Constraints

- `0 <= len(versions) <= 200000`
- `len(versions) == len(compatible)`
- `versions` is strictly increasing
- `compatible` has the form `False...False, True...True`

Function reference (as displayed):

`def solution(versions: list[int], compatible: list[bool]) -> int | None:`

### Part 2: First Compatible Index Under a Call Budget

Part 2: Medium
OpenAI
Machine Learning Engineer
Quick Overview

This question evaluates binary search, monotonic predicates, careful version ordering, and cost-aware optimization of expensive compatibility checks. It is commonly asked in the Coding & Algorithms domain to test reasoning about monotonicity, minimizing API calls, and adapting search strategies when monotonicity holds only within subranges; the level of abstraction combines conceptual understanding of monotone properties with practical application of efficient search techniques.

A version catalog contains versions identified only by indices 0 to n - 1 in increasing order. Checking whether a version is compatible is expensive.

For this coding problem, the results of the expensive API are provided as a boolean list compatible, where compatible[i] is the result of checking version i. The list is monotone: all False values come before all True values.

Return the smallest compatible index, or -1 if none are compatible. The intended solution should use binary search so the number of checks stays small.

#### Examples

##### Example 1

Input: `([False, False, True, True, True],)`

Output: `2`

Notes: The first compatible index is 2.

##### Example 2

Input: `([False, False, False],)`

Output: `-1`

Notes: There is no `True` value.

#### Constraints

- `0 <= len(compatible) <= 1000000`
- `compatible` is monotone nondecreasing
- Your algorithm should run in `O(log n)` time

Function reference (as displayed):

`def solution(compatible: list[bool]) -> int:`

### Part 3: Minimum Compatible Semantic Version with Layered Monotonicity

Part 3: Hard
OpenAI
Machine Learning Engineer
Quick Overview

This question evaluates binary search, monotonic predicates, careful version ordering, and cost-aware optimization of expensive compatibility checks. It is commonly asked in the Coding & Algorithms domain to test reasoning about monotonicity, minimizing API calls, and adapting search strategies when monotonicity holds only within subranges; the level of abstraction combines conceptual understanding of monotone properties with practical application of efficient search techniques.

You are given a sorted list of software versions as triples (major, minor, patch) and a boolean list compatible of the same length. compatible[i] is the result of an expensive predicate for versions[i].

The full list is not necessarily globally monotone, so one binary search over the entire array may fail. However, the data obeys layered monotonicity:

For a fixed (major, minor), compatibility over increasing patch is monotone.
Inside a fixed major, if you inspect only the last patch of each minor, those representative results are monotone over increasing minor.
Across majors, if you inspect only the last version of each major, those representative results are monotone over increasing major.

Versions are sorted lexicographically by (major, minor, patch). Return the lexicographically smallest compatible version, or None if no version works.

#### Examples

##### Example 1

Input: `([(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1), (2, 0, 0), (2, 0, 1), (2, 1, 0), (2, 1, 1), (3, 0, 0), (3, 0, 1)], [False, True, False, True, False, False, False, True, True, True])`

Output: `(1, 0, 1)`

Notes: The overall sequence is not globally monotone, but the layered representative checks still lead to major 1, minor 0, patch 1.

##### Example 2

Input: `([(1, 0, 0), (1, 0, 1), (2, 0, 0), (2, 0, 1), (2, 1, 0), (2, 1, 1), (3, 0, 0), (3, 0, 1)], [False, False, False, True, True, True, True, True])`

Output: `(2, 0, 1)`

Notes: Major 1 has no compatible version, so the minimum compatible version is found in major 2.

#### Constraints

- `0 <= len(versions) <= 200000`
- `len(versions) == len(compatible)`
- `versions` is sorted lexicographically and contains distinct tuples
- Patch-level monotonicity holds inside each fixed `(major, minor)` block
- Minor-representative monotonicity holds inside each `major`
- Major-representative monotonicity holds across majors

Function reference (as displayed):

`def solution(versions: list[list[int]], compatible: list[bool]) -> list[int]:`

## 中文翻译 — Read

给定一个按数值升序排列的软件版本列表，以及一个代价高昂的判定函数 `is_compatible(version)`。返回满足要求的最小版本；若没有可用版本，则返回 `None`。

面试通常分为三个部分：

1. 基础版本
   - 判定函数具有全局单调性：较早的版本均返回 `False`；一旦某个版本返回 `True`，所有后续版本也都返回 `True`。
   - 找到第一个兼容版本。
2. 调用次数受限版本
   - 与第一部分采用相同的单调性假设。
   - 面试官会记录调用 `is_compatible` 的次数，因此应尽量减少 API 调用。
3. 分层单调版本
   - 整个版本序列不一定单调。
   - 版本表示为三元组 `(major, minor, patch)`。
   - 对固定的 `(major, minor)`，兼容性随 `patch` 单调变化。
   - 在主版本和次版本层级，可通过代表版本的检查对候选分组进行二分搜索。
   - 利用这种分层单调性，以较少的判定函数调用找到最小兼容版本。

核心考点为二分搜索、谨慎处理版本排序，以及当单调性仅在部分区间内成立时调整搜索策略。

## 中文翻译 — Practice

### 页面概述（三部分相同）

本题考查二分搜索、单调判定函数、准确的版本排序，以及对昂贵兼容性检查的调用成本优化。它常见于 Coding & Algorithms 类面试，用于考查单调性推理、减少 API 调用，以及当单调性只在子区间中成立时调整搜索策略的能力；题目结合了对单调性质的概念理解和高效搜索技术的实际应用。

各部分的公司均为 OpenAI，岗位均为 Machine Learning Engineer。

### 第一部分：第一个兼容版本（Easy）

给定一个已排序、元素互不相同的整数软件版本列表 `versions`，以及一个等长的布尔列表 `compatible`。`compatible[i]` 表示昂贵判定函数 `is_compatible(versions[i])` 的结果。

判定函数具有全局单调性：`compatible` 的值排列为 `False, False, ..., False, True, True, ..., True`。

返回最小的兼容版本；若没有任何版本可用，则返回 `None`。

函数签名：`def solution(versions: list[int], compatible: list[bool]) -> int | None:`

#### 示例

1. 输入：`([100, 101, 102, 103, 104], [False, False, True, True, True])`
   输出：`102`
   说明：第一个兼容项位于索引 2，因此答案是版本 102。
2. 输入：`([5, 7, 9], [False, False, False])`
   输出：`None`
   说明：没有兼容版本。

#### 约束

- `0 <= len(versions) <= 200000`
- `len(versions) == len(compatible)`
- `versions` 严格递增。
- `compatible` 的形式为 `False...False, True...True`。

### 第二部分：调用次数受限时的第一个兼容索引（Medium）

版本目录中的版本仅由索引 `0` 到 `n - 1` 标识，按递增顺序排列。检查一个版本是否兼容的代价很高。

在此编程题中，昂贵 API 的结果通过布尔列表 `compatible` 提供，其中 `compatible[i]` 是检查版本 `i` 的结果。该列表单调：所有 `False` 都位于所有 `True` 之前。

返回最小的兼容索引；若没有兼容版本，则返回 `-1`。题目期望使用二分搜索，以减少检查次数。

函数签名：`def solution(compatible: list[bool]) -> int:`

#### 示例

1. 输入：`([False, False, True, True, True],)`
   输出：`2`
   说明：第一个兼容索引为 2。
2. 输入：`([False, False, False],)`
   输出：`-1`
   说明：不存在值为 `True` 的项。

#### 约束

- `0 <= len(compatible) <= 1000000`
- `compatible` 单调非递减。
- 算法应在 `O(log n)` 时间内运行。

### 第三部分：分层单调性下的最小兼容语义版本（Hard）

给定一个已排序的软件版本列表，版本表示为三元组 `(major, minor, patch)`，以及等长的布尔列表 `compatible`。`compatible[i]` 是对 `versions[i]` 执行昂贵判定函数的结果。

整个列表不一定具有全局单调性，因此对整个数组执行一次二分搜索可能失败。不过，数据满足分层单调性：

- 对固定的 `(major, minor)`，兼容性随递增的 `patch` 单调变化。
- 在固定的 `major` 内，若仅检查每个 `minor` 的最后一个补丁版本，这些代表版本的结果随递增的 `minor` 单调变化。
- 在不同的 `major` 之间，若仅检查每个主版本的最后一个版本，这些代表版本的结果随递增的 `major` 单调变化。

版本按 `(major, minor, patch)` 的字典序排列。返回字典序最小的兼容版本；若没有版本可用，则返回 `None`。

页面显示的函数签名：`def solution(versions: list[list[int]], compatible: list[bool]) -> list[int]:`

#### 示例

1. 输入：`([(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1), (2, 0, 0), (2, 0, 1), (2, 1, 0), (2, 1, 1), (3, 0, 0), (3, 0, 1)], [False, True, False, True, False, False, False, True, True, True])`
   输出：`(1, 0, 1)`
   说明：整体序列不具有全局单调性，但分层代表版本的检查仍然会找到主版本 1、次版本 0、补丁版本 1。
2. 输入：`([(1, 0, 0), (1, 0, 1), (2, 0, 0), (2, 0, 1), (2, 1, 0), (2, 1, 1), (3, 0, 0), (3, 0, 1)], [False, False, False, True, True, True, True, True])`
   输出：`(2, 0, 1)`
   说明：主版本 1 中没有兼容版本，因此最小兼容版本位于主版本 2 中。

#### 约束

- `0 <= len(versions) <= 200000`
- `len(versions) == len(compatible)`
- `versions` 按字典序排列，且各元组互不相同。
- 每个固定的 `(major, minor)` 分组内均满足补丁层级的单调性。
- 每个 `major` 内均满足次版本代表项的单调性。
- 跨主版本满足主版本代表项的单调性。
