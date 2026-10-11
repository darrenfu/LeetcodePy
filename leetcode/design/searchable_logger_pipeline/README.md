# Implement a Searchable Logger Pipeline

> Source: PracHub — Rippling, Software Engineer, Technical Screen
> Original: https://prachub.com/coding-questions/implement-a-searchable-logger-pipeline
> Category: Coding & Algorithms · Difficulty: Hard
> Exported: 2026-10-02

This question evaluates proficiency in software design, data structures, and
algorithmic text search by requiring a transformation pipeline, ordered
in-memory log storage with unique increasing identifiers, and efficient
keyword lookup.

## Function Reference

```python
def solution(operations: list[list[str]]) -> list[list[str]]:
    ...
```

Sample call:

```python
solution([
    ['add_handler', 'upper'],
    ['add_log', 'hello hello world'],
    ['add_log', 'world'],
    ['search', 'HELLO'],
    ['search', 'WORLD'],
    ['search', 'hello'],
    ['get_logs'],
])
```

Supported operations (both parts):

| Operation | Format | Produces output? |
|---|---|---|
| `add_handler` | `['add_handler', <handler>]` or `['add_handler', <handler>, <param>]` | No |
| `add_log` | `['add_log', <message>]` | No |
| `get_logs` | `['get_logs']` | Yes — all stored logs |
| `search` | `['search', <keyword>]` | Yes — matching stored logs |

Rules shared by both parts:

- Handlers are registered and applied to every subsequently added log
  **in the order they were added**.
- Handlers added later only affect logs added after them.
- Each stored log receives a unique increasing id starting at 1,
  formatted as `"<id>:<transformed_message>"`.
- `search` takes a keyword and returns stored logs whose
  **transformed** message contains that keyword as an exact
  whitespace-separated word. Matching is **case-sensitive**.
- Search returns logs in increasing id order.

---

## Part 1: In-Memory Logger Pipeline with Transformation Handlers

Handlers are one of: `upper`, `lower`, `reverse`.

- `upper` — uppercase the message.
- `lower` — lowercase the message.
- `reverse` — reverse the full message, including spaces.

### Example 1

Input:

```python
[['add_handler', 'upper'],
 ['add_log', 'Hello World'],
 ['add_log', 'another LOG entry'],
 ['get_logs'],
 ['search', 'World'],
 ['search', 'WORLD'],
 ['search', 'LOG']]
```

Output:

```python
[['1:HELLO WORLD', '2:ANOTHER LOG ENTRY'],
 [],
 ['1:HELLO WORLD'],
 ['2:ANOTHER LOG ENTRY']]
```

Notes: Search is case-sensitive and matches whole words in the
transformed text.

### Example 2

Input:

```python
[['add_handler', 'reverse'],
 ['add_log', 'abc def'],
 ['add_log', 'hello'],
 ['search', 'fed'],
 ['search', 'cba'],
 ['get_logs']]
```

Output:

```python
[['1:fed cba'],
 ['1:fed cba'],
 ['1:fed cba', '2:olleh']]
```

Notes: Reverse is applied to the full message, including spaces.

### Constraints

- `0 <= len(operations) <= 10000`
- Each operation is valid and follows one of the formats described above.
- `0 <= len(message), len(text), len(keyword) <= 1000`
- Total length of all added raw log messages is at most `1000000`.
- Handlers added later only affect logs added after them.
- Search returns logs in increasing id order.

### Hints (from PracHub)

1. Store handlers in an ordered list so that each new log can be
   transformed by applying them from first to last.
2. For search, split each transformed message on whitespace and check
   whether the keyword appears as a complete token.

---

## Part 2: In-Memory Logger Pipeline with Inverted Index Search

Implement the same in-memory logger pipeline, but optimize keyword
search using an **inverted index**. Handlers transform each message
before storage and are applied in the order they were added. Supported
handlers are: `upper`, `prefix`, and `suffix`.

- `upper` — uppercase the message.
- `prefix` — prepend the given text: `['add_handler', 'prefix', <text>]`.
- `suffix` — append the given text: `['add_handler', 'suffix', <text>]`.

Each stored log receives a unique increasing id starting at 1. Maintain
an index from each whitespace-separated word to the ids of logs
containing that word, so search does not scan every stored log. Search
is case-sensitive and matches exact words in the transformed stored
message. **If a word appears multiple times in one log, that log id
should appear only once for that word.**

### Example 1

Input:

```python
[['add_handler', 'upper'],
 ['add_log', 'hello hello world'],
 ['add_log', 'world'],
 ['search', 'HELLO'],
 ['search', 'WORLD'],
 ['search', 'hello'],
 ['get_logs']]
```

Output:

```python
[['1:HELLO HELLO WORLD'],
 ['1:HELLO HELLO WORLD', '2:WORLD'],
 [],
 ['1:HELLO HELLO WORLD', '2:WORLD']]
```

Notes: The first log contains `HELLO` twice, but it appears once in the
search result. Search is case-sensitive.

### Example 2

Input:

```python
[['add_log', ''],
 ['search', 'anything'],
 ['search', ''],
 ['get_logs']]
```

Output:

```python
[[],
 [],
 ['1:']]
```

Notes: An empty log is stored but contributes no words to the index.
Empty keyword searches return an empty list.

### Constraints

- `0 <= len(operations) <= 10000`
- Each operation is valid and follows one of the formats described above.
- `0 <= len(message), len(text), len(keyword) <= 1000`
- Total length of all added raw log messages is at most `1000000`.
- Search is case-sensitive and matches exact whitespace-separated words
  after all handlers have transformed the log.
- Repeated words in the same transformed log must not create duplicate
  search results.

### Hints (from PracHub)

1. When adding a log, split the transformed message into words and
   update a dictionary from word to log ids.
2. Use a set of words from a single log before updating the index to
   avoid indexing the same log id multiple times for repeated words.
