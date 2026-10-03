# Compute Balances and Minimize Settlements

- Company: Affirm
- Role: Software Engineer
- Category: Coding & Algorithms
- Difficulty: HARD
- Interview Round: Onsite
- Date: Feb 27, 2026 (company listing)
- Solved: 111 (original metadata); 112 (company listing observed 2026-10-03)
- Last updated: Jun 26, 2026 (detail page)
- Company page: https://prachub.com/companies/affirm
- Question page: https://prachub.com/coding-questions/compute-balances-and-minimize-settlements
- Source verified: 2026-10-03, local Chrome, Description → Part 1 and Part 2; unlocked content.

## English original statement

### Overview / Quick Overview

This question evaluates transactional data aggregation and net-balance computation skills alongside combinatorial optimization for minimizing settlement transfers, testing competencies in data structures, numeric aggregation, and algorithmic reasoning.

### Part 1: Easy — End-of-Day Net Balances

You are building a daily ledger service.

Each transaction record has three fields: `timestamp`, `user_id`, and `delta_amount`. `delta_amount` is an integer (positive or negative) representing how that user's balance changes during the day. Every user's starting balance is 0.

Given a list of transaction records for a single day, compute each user's end-of-day **net** balance (the sum of all their `delta_amount` values). Return a mapping from `user_id` to net balance.

Users whose final net balance is 0 should be **omitted** from the result (they are settled and need no entry).

Input: a list of records, where each record is `[timestamp, user_id, delta_amount]`. Output: a dict mapping each user with a non-zero balance to that balance.

#### Examples

**Example 1**

- Input: `([[1, 'alice', 100], [2, 'bob', -50], [3, 'alice', -30], [4, 'carol', 20]],)`
- Output: `{'alice': 70, 'bob': -50, 'carol': 20}`
- Notes: alice nets 100-30=70, bob -50, carol 20. All non-zero, all kept.

**Example 2**

- Input: `([],)`
- Output: `{}`
- Notes: No transactions means no balances.

#### Constraints

- delta_amount is an integer and may be negative, positive, or zero.
- A user may appear in many records; sum all their deltas.
- Omit any user whose final net balance equals 0.
- The input list may be empty (return an empty mapping).

#### Function reference

Signature: `def computeBalances(transactions: list[tuple[int, str, int]]) -> dict[str, int]:`

Sample call: `computeBalances([[1, 'alice', 100], [2, 'bob', -50], [3, 'alice', -30], [4, 'carol', 20]])`

### Part 2: Hard — Minimum-Transfer Settlement Plan

Continuing the ledger service: you are given the users' net balances (the output of part 1) as a mapping from `user_id` to balance. Positive balances are **creditors** (must receive money); negative balances are **debtors** (must pay money). The sum of all balances is 0.

Produce a settlement that brings everyone to 0 using the **minimum possible number of transfers**, where each transfer moves money from one debtor to one creditor. Return that minimum **number of transfers**.

This is the Optimal Account Balancing problem: greedily pairing the largest creditor with the largest debtor does NOT always give the minimum. The optimum requires finding subsets of users whose balances cancel exactly. The prompt permits an exponential-search solution because the number of users with non-zero balance is small.

Key insight: if the non-zero accounts can be partitioned into `G` disjoint groups that each sum to 0, a group of `k` accounts settles in `k - 1` transfers. With `n` non-zero accounts, total transfers = `sum(k_g - 1) = n - G`, so minimizing transfers means **maximizing** the number of zero-sum groups.

Input: a dict mapping user_id to a (possibly zero) balance. Output: an integer, the minimum number of transfers.

#### Examples

**Example 1**

- Input: `({},)`
- Output: `0`
- Notes: No non-zero balances means no transfers are needed.

**Example 2**

- Input: `({'a': 10, 'b': -10},)`
- Output: `1`
- Notes: b pays a 10 in a single transfer.

#### Constraints

- The number of users with non-zero balance is small (an exponential-time solution is acceptable).
- The sum of all balances is exactly 0.
- Users with a balance of 0 are ignored and do not appear in any transfer.
- Greedy largest-creditor/largest-debtor pairing is NOT guaranteed optimal; subsets that cancel exactly must be found.

#### Function reference

Signature: `def minTransfers(balances: dict[str, int]) -> int:`

Sample call: `minTransfers({})`

## 中文翻译

### 概述

本题同时考查交易数据聚合、净余额计算，以及为减少结算转账次数而进行的组合优化，涉及数据结构、数值聚合和算法推理。

### 第一部分：简单 — 日终净余额

你正在构建一个每日账本服务。

每条交易记录有三个字段：`timestamp`（时间戳）、`user_id`（用户标识）和 `delta_amount`（余额变化量）。`delta_amount` 是整数（可正可负），表示该用户在当天的余额变化。每个用户的初始余额均为 0。

给定同一天的交易记录列表，计算每个用户的日终**净余额**，即该用户所有 `delta_amount` 的总和。返回从 `user_id` 到净余额的映射。

最终净余额为 0 的用户应从结果中**省略**，因为他们已经结清，不需要对应条目。

输入：记录列表，每条记录为 `[timestamp, user_id, delta_amount]`。输出：字典，将每个余额非零的用户映射到其余额。

#### 示例

**示例 1**

- 输入：`([[1, 'alice', 100], [2, 'bob', -50], [3, 'alice', -30], [4, 'carol', 20]],)`
- 输出：`{'alice': 70, 'bob': -50, 'carol': 20}`
- 说明：alice 的净余额为 100-30=70，bob 为 -50，carol 为 20。三者均非零，全部保留。

**示例 2**

- 输入：`([],)`
- 输出：`{}`
- 说明：没有交易，就没有余额条目。

#### 约束

- `delta_amount` 是整数，可以为负数、正数或零。
- 一个用户可以出现在多条记录中，必须累加其全部变化量。
- 省略最终净余额等于 0 的用户。
- 输入列表可以为空，此时返回空映射。

#### 函数参考

签名：`def computeBalances(transactions: list[tuple[int, str, int]]) -> dict[str, int]:`

示例调用：`computeBalances([[1, 'alice', 100], [2, 'bob', -50], [3, 'alice', -30], [4, 'carol', 20]])`

### 第二部分：困难 — 最少转账结算方案

继续构建账本服务：输入用户净余额（第一部分的输出），形式为从 `user_id` 到余额的映射。正余额表示**债权人**（必须收款），负余额表示**债务人**（必须付款）。所有余额之和为 0。

使所有用户余额归零，并使用**尽可能少的转账次数**。每笔转账从一个债务人向一个债权人转移资金。返回这一最少**转账次数**。

这是 Optimal Account Balancing（最优账户结算）问题：每次贪心地配对最大债权人与最大债务人，并不总能得到最少次数。最优方案需要找到余额恰好相互抵消的用户子集。由于非零余额用户数较少，题目允许指数时间搜索。

关键思路：如果可以把非零账户划分为 `G` 个互不重叠、各自余额之和为 0 的组，那么一个包含 `k` 个账户的组可以用 `k - 1` 笔转账结清。对于 `n` 个非零账户，总转账次数为 `sum(k_g - 1) = n - G`，因此最少转账次数对应于**最大化**零和组的数量。

输入：从 `user_id` 到余额（可能为零）的字典。输出：一个整数，表示最少转账次数。

#### 示例

**示例 1**

- 输入：`({},)`
- 输出：`0`
- 说明：没有非零余额，不需要转账。

**示例 2**

- 输入：`({'a': 10, 'b': -10},)`
- 输出：`1`
- 说明：b 向 a 支付 10，只需一笔转账。

#### 约束

- 非零余额用户数较少，允许指数时间解法。
- 所有余额之和恰好为 0。
- 忽略余额为 0 的用户，他们不参与任何转账。
- 贪心地配对最大债权人与最大债务人不能保证最优；必须找到能够恰好抵消的子集。

#### 函数参考

签名：`def minTransfers(balances: dict[str, int]) -> int:`

示例调用：`minTransfers({})`

### 来源说明 / Source notes

The page gives no numeric upper bounds for transaction count, user count, timestamps, or amounts. None have been added. The example input notation includes the site's outer one-argument tuple wrapper. Part 1's first example sums to 40, so it does not satisfy Part 2's separate zero-sum precondition. The original wording about `k - 1` is preserved above; the guide clarifies the optimal-partition reasoning.

页面未给出交易数、用户数、时间戳或金额的具体数值上限，本文件未自行补充。示例输入保留网站用于包装单个函数参数的外层元组。第一部分示例 1 的余额总和为 40，不满足第二部分独立规定的零和前提。上文保留了原题关于 `k - 1` 的措辞，引导报告会解释最优划分中的准确含义。
