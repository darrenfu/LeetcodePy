# First-Match CIDR Firewall: Status of an IP Address or a Whole CIDR Block

- Company / 公司: Databricks
- Role / 岗位: Software Engineer / 软件工程师
- Category / 分类: Coding & Algorithms / 编程与算法
- Topic / 主题: Bit Manipulation / 位运算（公司列表标签）
- Difficulty / 难度: MEDIUM / 中等
- Interview round / 面试轮次: Onsite / 现场面试
- Listed date / 列表日期: Sep 11, 2026
- Last updated / 页面更新时间: Sep 28, 2026
- Solved / 已解人数: 32（读取时公司列表显示；搜索结果显示 0，不作为稳定题目属性）
- Company page / 公司页: https://prachub.com/companies/databricks
- Source / 题目详情: https://prachub.com/coding-questions/first-match-cidr-firewall-status-of-an-ip-address-or-a-whole-cidr-block
- Read view / 阅读页: https://prachub.com/interview-questions/first-match-cidr-firewall-status-of-an-ip-address-or-a-whole-cidr-block?view=text
- Verified / 核对日期: 2026-10-03, local Chrome, signed-in Premium session
- Practice-view title / 练习视图标题: First-Match Firewall Status for an IPv4 Address or CIDR Block

> Editorial note / 编写说明: The English section below is a complete semantic restatement of the observed task, not a verbatim reproduction of the copyrighted website prose. The Chinese section translates this restatement. The source link retains access to the original wording. / 以下英文完整重述已核对的题意，并非网站受版权保护正文的逐字复制；中文翻译对应本重述。原始措辞请查看来源链接。

## English problem statement (semantic restatement)

### Task and interface

Implement `get_status(rules, target)` for an IPv4 firewall. The input `rules` is one ordered list of `(pattern, action)` pairs. First handle an individual address; the follow-up extends the same function to a CIDR target containing multiple addresses.

A pattern can be a dotted IPv4 address alone or an address followed by `/p`. A bare address means `/32`. Interpret the four octets in network order as an unsigned 32-bit value, with the first octet occupying the most significant bits. For a prefix of length `p`, membership depends only on the first `p` bits; discard the remaining host bits when interpreting either rules or targets. Prefix `/0` includes the entire IPv4 space.

For each address, choose the action of its earliest matching rule, identified by the smallest input index. If nothing matches, use `DENY`. The original-report text explicitly labels this default as an assumption absent from the interview report; the current practice statement adopts it as the contract.

The target accepts the same address/prefix forms. Produce `ALLOW` exactly when every address represented by the target individually evaluates to `ALLOW`; any denied or unmatched address makes the result `DENY`. Several earlier allow rules may collectively allow the block; one rule spanning the entire block is unnecessary.

The source report uses this signature:

```text
get_status(rules: list[tuple[str, str]], target: str) -> str
```

The practice function reference uses `list[list[str]]` for `rules`. Both describe two-element pattern/action pairs. Other language representations shown are arrays in JavaScript, `java.util.List<java.util.List<String>>` in Java, and `std::vector<std::vector<std::string>>` in C++.

### Input limits and output

- Rule count is between 1 and 100,000 inclusive.
- Prefix lengths are integers in `[0, 32]`; omitted prefixes mean 32.
- Addresses consist of four dot-separated decimal octets, each in `[0, 255]`. Inputs contain neither leading zeros nor whitespace.
- Actions and the returned string use exactly `ALLOW` or `DENY`.
- The largest address value is 4,294,967,295. A target may represent 4,294,967,296 addresses. Both exceed a signed 32-bit maximum; the practice page calls for 64-bit address arithmetic in Java (`long`) and C++ (`long long`).

### Observed examples and variants

| Ordered rules | Target | Result | Reason |
|---|---|---|---|
| `[("192.168.1.0/24", "ALLOW"), ("8.8.8.8", "DENY")]` | `192.168.1.5` | `ALLOW` | Rule 0 covers the address. |
| Same rules | `8.8.8.8` | `DENY` | Rule 1 is the first matching rule. |
| Same rules | `10.0.0.1` | `DENY` | No match; use the default. |
| `[("10.0.0.7", "DENY"), ("10.0.0.0/24", "ALLOW")]` | `10.0.0.0/28` | `DENY` | The block spans `.0` through `.15`; `.7` is denied by the earlier rule. |
| Same rules | `10.0.0.16/28` | `ALLOW` | The block spans `.16` through `.31`, outside the earlier denial. |
| `[("10.0.0.0/25", "ALLOW"), ("10.0.0.128/25", "ALLOW")]` | `10.0.0.0/24` | `ALLOW` | The two halves jointly cover the target. This third example appears in the original-report section; the current practice prose shows the first two. |

No additional runtime target or query-count bound was stated in the observed description.

## 中文题面（对应上文翻译）

### 任务与接口

为 IPv4 防火墙实现 `get_status(rules, target)`。`rules` 是作为一个参数传入的有序列表，每条规则是一组 `(pattern, action)`。基础问题处理单个地址；追问要求同一个函数也处理包含多个地址的 CIDR 目标块。

模式可以是单独的点分 IPv4 地址，也可以是地址加 `/p`。裸地址等价于 `/32`。按网络顺序把四个八位组解释为无符号 32 位数，第一个八位组占最高位。前缀长度为 `p` 时，只比较最高的 `p` 位；解释规则或目标时，忽略其余主机位。`/0` 包含整个 IPv4 地址空间。

对每个地址，选取输入下标最小的匹配规则，并使用其动作。没有匹配规则时，状态为 `DENY`。原始报告部分特别注明：默认拒绝是补充假设，原面试报告没有说明；当前练习版已把它纳入接口约定。

目标同样可以采用裸地址或 CIDR 表示法。只有目标表示的每个地址分别计算后都为 `ALLOW`，整个查询才返回 `ALLOW`；只要有一个地址被拒绝或未匹配，就返回 `DENY`。多条允许规则可以共同覆盖目标，无须存在一条覆盖整个块的规则。

原始报告签名为：

```text
get_status(rules: list[tuple[str, str]], target: str) -> str
```

练习页函数参考把 `rules` 标为 `list[list[str]]`，两者都表达由模式和动作组成的二元组列表。页面还列出 JavaScript 数组、Java 的 `java.util.List<java.util.List<String>>`、C++ 的 `std::vector<std::vector<std::string>>` 等对应表示。

### 输入限制与输出

- 规则数量在 1 到 100,000 之间，包含两端。
- 前缀长度是 `[0, 32]` 内的整数；省略前缀表示 32。
- 地址由四个用点分隔的十进制八位组组成，每组在 `[0, 255]` 内；没有前导零或空白。
- 动作和返回字符串只能是精确的 `ALLOW` 或 `DENY`。
- 最大地址值为 4,294,967,295；目标块最多含 4,294,967,296 个地址。两者都超过有符号 32 位整数上限；练习页要求 Java 使用 `long`、C++ 使用 `long long` 进行地址运算。

### 页面示例及其变体

| 有序规则 | 目标 | 结果 | 原因 |
|---|---|---|---|
| `[("192.168.1.0/24", "ALLOW"), ("8.8.8.8", "DENY")]` | `192.168.1.5` | `ALLOW` | 第 0 条规则匹配。 |
| 同上 | `8.8.8.8` | `DENY` | 第 1 条规则最先匹配。 |
| 同上 | `10.0.0.1` | `DENY` | 没有匹配规则，默认拒绝。 |
| `[("10.0.0.7", "DENY"), ("10.0.0.0/24", "ALLOW")]` | `10.0.0.0/28` | `DENY` | 范围为 `.0` 至 `.15`；其中 `.7` 先被第 0 条规则拒绝。 |
| 同上 | `10.0.0.16/28` | `ALLOW` | 范围为 `.16` 至 `.31`，不包含之前被拒绝的地址。 |
| `[("10.0.0.0/25", "ALLOW"), ("10.0.0.128/25", "ALLOW")]` | `10.0.0.0/24` | `ALLOW` | 两个半块共同覆盖整个目标。第 3 例来自页面原始报告部分；当前练习正文只列前两例。 |

已读取的题面没有另行指定运行时间目标或查询次数上限。
