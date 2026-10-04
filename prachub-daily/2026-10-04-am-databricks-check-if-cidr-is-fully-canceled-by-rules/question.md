# Check if CIDR is fully canceled by rules

- Company: Databricks
- Category: Coding & Algorithms
- Difficulty: MEDIUM
- Question date: Dec 8, 2025
- Solved by: 253 people
- Company page: https://prachub.com/companies/databricks

- Role: Software Engineer
- Interview round: Technical Screen
- Detail page: https://prachub.com/coding-questions/check-if-cidr-is-fully-canceled-by-rules
- Page last updated: Apr 19, 2026
- Verified: Oct 4, 2026, in local Chrome; full-question section expanded.
- Metadata provenance: Question date and solved count above are preserved from the existing file; the detail page did not re-confirm them.
- Text provenance: English below is a complete requirements paraphrase, not a verbatim reproduction of the webpage. Chinese translates that paraphrase. / 下文英文为覆盖全部要求的改述，并非网页逐字原文；中文翻译该改述。

## English problem statement — paraphrased

Given an IPv4 target CIDR `T` and an ordered list of `(type, CIDR)` rules, decide whether the rules completely cancel the target. A rule type is either `allow` or `deny`; CIDRs have the form `a.b.c.d/x`. For example, the target may be `10.0.0.0/16`.

Initially, every address in `T` remains to be canceled. Visit rules in their input order:

1. An `allow` rule cancels the intersection of its CIDR with the region still remaining. Addresses removed this way are considered handled elsewhere.
2. A `deny` rule causes immediate failure if its CIDR contains even one address that still remains. It does not cause failure merely because it intersects an already-canceled part of the original target.
3. After the rules finish, succeed exactly when no addresses remain; otherwise fail.

Return a boolean. The page's Python function reference is `solution(target: str, rules: list[tuple[str, str]]) -> bool`.

### Requirements and clarifications

- Use ordinary IPv4 CIDR interpretation: prefix length `x` selects all addresses with the same first `x` bits as the supplied address.
- An address with host bits set still denotes its whole network. Thus `10.0.1.5/24` and `10.0.1.0/24` describe the same block.
- Keep the rule order. Intersection means sharing at least one IP address.
- Canceling a portion of the target may leave several disjoint pieces. Every subsequent rule must account for every remaining piece.
- The target and rule CIDR strings are syntactically valid IPv4 inputs.
- Describe a correct, reasonably efficient approach, including the representation of ranges, their subtraction, and the time and space costs.

### Constraints

- Number of rules: 0 through 2000, inclusive.
- CIDR prefix lengths: 0 through 32, inclusive.
- Rules are sequential; correctly support an allow operation that splits the remaining region into disjoint intervals.

### Examples from the page

1. Target: `10.0.0.0/24`. Rules: `[("allow", "10.0.0.0/25"), ("allow", "10.0.0.128/25")]`. Result: `True`. Each rule cancels a different half; together they remove all target addresses.
2. Target: `10.0.0.0/24`. Rules: `[("allow", "10.0.0.0/25")]`. Result: `False`. The second half remains uncanceled.

### Page hints — paraphrased

- Represent CIDR blocks as integer intervals with both endpoints included.
- Keep an ordered collection of non-overlapping remaining intervals. Allow rules subtract addresses; deny rules check for intersection.

## 中文题面 — 英文改述的翻译

给定 IPv4 目标 CIDR `T` 和按顺序排列的 `(type, CIDR)` 规则列表，判断这些规则能否完全取消目标地址块。规则类型为 `allow` 或 `deny`，CIDR 格式为 `a.b.c.d/x`。例如，目标可以是 `10.0.0.0/16`。

最初，`T` 中的所有地址都属于尚待取消的区域。按照输入顺序依次处理规则：

1. `allow` 规则取消其 CIDR 与当前剩余区域的交集。被移除的地址视为已由其他地方处理。
2. 如果 `deny` 规则的 CIDR 包含任何一个仍然剩余的地址，立即判定失败。仅与原目标中已经取消的部分相交，不会导致失败。
3. 全部规则处理结束后，只有剩余区域为空才成功，否则失败。

返回布尔值。页面的 Python 函数接口为 `solution(target: str, rules: list[tuple[str, str]]) -> bool`。

### 要求与澄清

- 使用标准 IPv4 CIDR 语义：前缀长度 `x` 表示所有前 `x` 位与给定地址相同的 IP。
- 即使输入地址的主机位非零，它也表示整个对应网络。因此 `10.0.1.5/24` 与 `10.0.1.0/24` 表示同一个地址块。
- 保持规则顺序。只要共享至少一个 IP 地址，就算重叠。
- 取消目标的一部分可能留下多个互不相交的片段。后续每条规则都必须考虑所有剩余片段。
- 目标及规则 CIDR 字符串都是语法有效的 IPv4 输入。
- 给出正确且合理高效的方案，说明区间表示、区间减法以及时间和空间开销。

### 约束

- 规则数量为 0 到 2000，包含两端。
- CIDR 前缀长度为 0 到 32，包含两端。
- 按顺序执行规则；正确支持 allow 操作把剩余区域切成多个不相交区间。

### 页面示例

1. 目标：`10.0.0.0/24`。规则：`[("allow", "10.0.0.0/25"), ("allow", "10.0.0.128/25")]`。结果：`True`。两条规则分别取消一半，合起来移除目标中的所有地址。
2. 目标：`10.0.0.0/24`。规则：`[("allow", "10.0.0.0/25")]`。结果：`False`。目标的后一半仍未取消。

### 页面提示 — 改述

- 把 CIDR 地址块表示为包含左右端点的整数区间。
- 按顺序维护互不重叠的剩余区间集合。Allow 规则执行区间减法，deny 规则检查是否相交。
