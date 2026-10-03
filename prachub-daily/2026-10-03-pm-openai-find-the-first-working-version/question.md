# Find the First Working Version

- Company / 公司: OpenAI
- Role / 职位: Machine Learning Engineer / 机器学习工程师
- Category / 分类: Coding & Algorithms / 编程与算法
- Difficulty / 总体难度: medium / 中等
- Interview Round / 面试轮次: Onsite / 现场面试
- Listed date / 列表日期: Feb 1, 2026
- Last updated / 详情更新日期: Apr 21, 2026
- Source / 题目详情: https://prachub.com/coding-questions/find-the-first-working-version
- Company page / 公司页: https://prachub.com/companies/openai
- Retrieved / 读取日期: 2026-10-03, authenticated local Chrome, Description tab, both parts
- Solved count / 已解人数: search result showed 0; the previous placeholder said 55. This dynamic counter is not a problem constraint. / 当前搜索结果显示 0，旧占位文件为 55；动态统计不属于题目约束。

## English — original statement

### Overview

This question evaluates understanding of search algorithms, version normalization, and monotonic predicates, along with competency in parsing and ordering semantic version components.

### Part 1: Earliest Working Version in a Flat Sorted List

**Part 1: Medium · OpenAI Machine Learning Engineer**

#### Quick Overview

This question evaluates understanding of search algorithms, version normalization, and monotonic predicates, along with competency in parsing and ordering semantic version components. You are given a sorted list of version strings, `versions`, and a version string `works_from`. Imagine an API `works(version)` such that every version earlier than `works_from` returns `False`, and every version equal to or later than `works_from` returns `True`. Version strings may have 1, 2, or 3 numeric components: `major`, `major.minor`, or `major.minor.patch`. Missing components count as `0`, so `12 == 12.0 == 12.0.0` and `7.3 == 7.3.0`. The list is already sorted by this normalized `(major, minor, patch)` order. Return the earliest element from `versions` that works, or `None` if no listed version works. Your solution should be efficient for large inputs.

#### Examples

**Example 1**

- Input: `(['1', '1.2', '1.2.5', '2'], '1.2')`
- Output: `'1.2'`
- Notes: `1.2` is the first version in the sorted list that is at least `1.2.0`.

**Example 2**

- Input: `(['1', '1.0.1', '1.1', '2'], '1.0.2')`
- Output: `'1.1'`
- Notes: `1.0.1` is too early, and `1.1` is the first normalized version greater than or equal to `1.0.2`.

#### Constraints

- `0 <= len(versions) <= 200000`
- Each version string has 1 to 3 dot-separated non-negative integers
- Each numeric component is in the range `[0, 10^9]`
- Missing minor or patch components are treated as 0 for comparison
- The input list is sorted by normalized `(major, minor, patch)` order

#### Function reference (displayed by the site)

`def solution(versions: list[str], works_from: str) -> str:`

Sample call: `solution(['1', '1.2', '1.2.5', '2'], '1.2')`

### Part 2: Earliest Working Version in a Grouped Version Catalog

**Part 2: Hard · OpenAI Machine Learning Engineer**

#### Quick Overview

This question evaluates understanding of search algorithms, version normalization, and monotonic predicates, along with competency in parsing and ordering semantic version components. Now the versions are not given as one flat list. Instead, they are grouped as `catalog = [(major, minors), ...]`, where each `minors` is a sorted list of `(minor, patches)`, and each `patches` is a sorted list of existing patch numbers for that `(major, minor)` pair. Each listed triple `(major, minor, patch)` is an existing version. You are also given `works_from`, the first version value for which an imaginary API `works(version)` would return `True`. Missing components in `works_from` count as `0`. Return the earliest existing version in the catalog that works, formatted as a normalized string `major.minor.patch`, or `None` if no existing version works. Do not flatten the entire catalog into one long list first.

#### Examples

**Example 1**

- Input: `([(1, [(0, [0, 2]), (2, [1])]), (2, [(0, [0]), (1, [0, 3])])], '1.2.0')`
- Output: `'1.2.1'`
- Notes: In major `1` and minor `2`, the first patch at least `0` is `1`.

**Example 2**

- Input: `([(1, [(0, [0, 5]), (2, [0])]), (2, [(0, [0])])], '1.0.6')`
- Output: `'1.2.0'`
- Notes: There is no patch in `1.0.*` that is at least `6`, so the answer moves to the next available minor in the same major.

#### Constraints

- `0 <= len(catalog) <= 100000`
- Major groups are sorted by unique major number
- Within each major group, minor groups are sorted by unique minor number and are non-empty
- Within each `(major, minor)` group, patches are sorted, unique, and non-empty
- All major, minor, and patch values are integers in the range `[0, 10^9]`
- The `works_from` string has 1 to 3 dot-separated numeric components; missing components count as 0

#### Function reference (displayed by the site)

`def solution(catalog: list[tuple[int, list[tuple[int, list[int]]]]], works_from: str) -> str:`

Sample call: `solution([(1, [(0, [0, 2]), (2, [1])]), (2, [(0, [0]), (1, [0, 3])])], '1.2.0')`

## 中文 — 完整翻译

### 概述

本题考察搜索算法、版本号规范化、单调谓词，以及解析和排序语义版本号各分量的能力。

### 第一部分：在已排序的扁平列表中找到最早可用版本

**第一部分：中等 · OpenAI 机器学习工程师**

#### 题目概述

本题考察搜索算法、版本号规范化、单调谓词，以及解析和排序语义版本号各分量的能力。给定已排序的版本字符串列表 `versions` 和版本字符串 `works_from`。设想存在 API `works(version)`：所有早于 `works_from` 的版本返回 `False`，所有等于或晚于 `works_from` 的版本返回 `True`。版本字符串可以包含 1、2 或 3 个数字分量，格式分别为 `major`、`major.minor`、`major.minor.patch`。缺省分量视为 `0`，因此 `12 == 12.0 == 12.0.0`，`7.3 == 7.3.0`。输入列表已经按规范化后的 `(major, minor, patch)` 顺序排序。返回 `versions` 中最早可用的元素；若列表中没有可用版本，返回 `None`。解法应能高效处理大规模输入。

#### 示例

**示例 1**

- 输入：`(['1', '1.2', '1.2.5', '2'], '1.2')`
- 输出：`'1.2'`
- 说明：`1.2` 是已排序列表中第一个不小于 `1.2.0` 的版本。

**示例 2**

- 输入：`(['1', '1.0.1', '1.1', '2'], '1.0.2')`
- 输出：`'1.1'`
- 说明：`1.0.1` 太早，`1.1` 是第一个规范化后大于或等于 `1.0.2` 的版本。

#### 约束

- `0 <= len(versions) <= 200000`
- 每个版本字符串含 1 至 3 个以点分隔的非负整数
- 每个数字分量的范围为 `[0, 10^9]`
- 比较时，缺省的 minor 或 patch 分量视为 0
- 输入列表已经按规范化后的 `(major, minor, patch)` 顺序排序

#### 网站函数参考

`def solution(versions: list[str], works_from: str) -> str:`

示例调用：`solution(['1', '1.2', '1.2.5', '2'], '1.2')`

### 第二部分：在分组版本目录中找到最早可用版本

**第二部分：困难 · OpenAI 机器学习工程师**

#### 题目概述

本题考察搜索算法、版本号规范化、单调谓词，以及解析和排序语义版本号各分量的能力。现在版本不再作为一个扁平列表给出，而是按 `catalog = [(major, minors), ...]` 分组。其中每个 `minors` 是已排序的 `(minor, patches)` 列表，每个 `patches` 是对应 `(major, minor)` 下已存在的 patch 编号的有序列表。每个列出的三元组 `(major, minor, patch)` 都对应一个已存在的版本。另给定 `works_from`，它是使假想 API `works(version)` 返回 `True` 的最早版本值。`works_from` 中缺省的分量视为 `0`。返回目录中最早可用的已存在版本，格式为规范化字符串 `major.minor.patch`；若没有已存在的可用版本，返回 `None`。不要先将整个目录展开成一个长列表。

#### 示例

**示例 1**

- 输入：`([(1, [(0, [0, 2]), (2, [1])]), (2, [(0, [0]), (1, [0, 3])])], '1.2.0')`
- 输出：`'1.2.1'`
- 说明：major 为 `1`、minor 为 `2` 时，第一个不小于 `0` 的 patch 是 `1`。

**示例 2**

- 输入：`([(1, [(0, [0, 5]), (2, [0])]), (2, [(0, [0])])], '1.0.6')`
- 输出：`'1.2.0'`
- 说明：`1.0.*` 下不存在不小于 `6` 的 patch，因此答案移至同一 major 下的下一个可用 minor。

#### 约束

- `0 <= len(catalog) <= 100000`
- major 分组按互不重复的 major 编号排序
- 每个 major 分组内，minor 分组按互不重复的 minor 编号排序，且 minor 分组列表非空
- 每个 `(major, minor)` 分组内，patch 列表有序、无重复且非空
- 所有 major、minor、patch 值均为 `[0, 10^9]` 范围内的整数
- `works_from` 含 1 至 3 个以点分隔的数字分量，缺省分量视为 0

#### 网站函数参考

`def solution(catalog: list[tuple[int, list[tuple[int, list[int]]]]], works_from: str) -> str:`

示例调用：`solution([(1, [(0, [0, 2]), (2, [1])]), (2, [(0, [0]), (1, [0, 3])])], '1.2.0')`

> Editorial note / 编者注：The site's function references annotate `str`, while both statements explicitly permit `None`. Preserve the stated no-answer behavior; an implementation's annotation should account for it. / 网站函数参考标注返回 `str`，但两部分题面均明确允许 `None`；实现时应遵循题面，并让返回类型覆盖无答案情形。
