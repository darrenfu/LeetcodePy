from collections import deque, defaultdict
from typing import List, Dict

from pygtrie import Trie

def components(path: str) -> List[str]:
    tokens = path.split('/')
    stack = deque()
    for tok in tokens:
        if tok ==  '' or tok == '.':
            continue
        if tok == "..":
            if not stack:
                raise ValueError("invalid .. operation. Already under root dir")
            stack.pop()
        else:
            stack.append(tok)
    return list(stack)

def normalize_home_prefix(path: str, homeDir: str) -> str:
    if path == '~':
        return homeDir
    if path.startswith('~/'):
        return homeDir + path[1:]
    return path

def normalize_path_into_parts(currentDir: str, newDir: str, homeDir: str | None) -> List[str]:
    currentDir = normalize_home_prefix(currentDir, homeDir)
    newDir = normalize_home_prefix(newDir, homeDir)

    baseDir = '/' if newDir.startswith("/") else currentDir
    return components(baseDir + '/' + newDir) # e.g. "/foo/bar" -> ["foo", "bar"]

def normalize_path(currentDir: str, newDir: str) -> str:
    parts = normalize_path_into_parts(currentDir, newDir)
    return "/" + '/'.join(parts)

def normalize_single_path(dir: str) -> List[str]:
    dir = normalize_home_prefix(dir)
    return components(dir)

def normalize_path_with_symlinks(currentDir: str, newDir: str, trie: Trie) -> str:
    parts = tuple(normalize_path_into_parts(currentDir, newDir))
    uncommon_parts = []
    while True:
        prefix = trie.longest_prefix(parts)
        # print(parts, prefix)
        if prefix.key is None:
            uncommon_parts = list(parts) + uncommon_parts
            break

        N = len(prefix.key)
        if N < len(parts):
            # there is a suffix after symlink
            uncommon_parts = list(parts[N:]) + uncommon_parts
        # jump to the target
        parts = prefix.value

    return '/' + '/'.join(uncommon_parts)

def resolve_symlinks(symlinks: Dict[str, str]) -> Trie:
    # If the final path has one or more prefixes that are keys in symlinks,
    # rewrite the path using the longest matching prefix.
    # Use Trie so that '/a/b/c/' always precedes '/a/b/'
    trie = Trie()
    for src_path, dest_path in symlinks.items():
        src_parts = normalize_single_path(src_path)
        dest_parts = normalize_single_path(dest_path)
        trie[tuple(src_parts)] = tuple(dest_parts)
    return trie

def detect_symlink_cycle(trie: Trie) -> None:
    in_degree = defaultdict(int)
    rev_deps = {}
    for src, dest in trie.items():
        in_degree.setdefault(src, 0)
        in_degree[dest] += 1
        rev_deps[src] = dest
    # print("in_degree: ", in_degree)
    # print("rev_deps: ", rev_deps)

    q = deque([n for n, deg in in_degree.items() if deg == 0])
    tupo_order = []
    while q:
        n = q.popleft()
        tupo_order.append(n)
        if n not in rev_deps:
            continue
        downstream = rev_deps[n]
        in_degree[downstream] -= 1
        if in_degree[downstream] == 0:
            q.append(downstream)

    if len(tupo_order) != len(in_degree):
        raise ValueError("Cycle detected in symlink dependencies")

def cd(currentDir: str,
       newDir: str,
       symlinks: Dict[str, str] | None = None,
       homeDir: str | None = None) -> str | None:
    parts = normalize_path_into_parts(currentDir, newDir, homeDir)
    if parts is None:
        return None
    if not symlinks:
        return "/" + "/".join(parts)

    trie = resolve_symlinks(symlinks)
    detect_symlink_cycle(trie)
    # print(trie)
    return normalize_path_with_symlinks(currentDir, newDir, trie)


# print(normalize_path("/tmp/", "a/../b/../c/./d/"))
# print(normalize_path("/tmp/", "/mnt/a/..//../b/./c/./d/"))
# print(normalize_path("~/tmp/", "~/a/b"))
# print(normalize_path("~", "a"))
# print(normalize_path("~~/", "~/a"))
# cd("/", "/a", {
#     '/foo/bar': '/baz', '/foo/bar/baz': '/bar/baz', '/foo/baz/': '/far'
# })
print("cd to ", cd("/", "/a/b/c/d/e/f", {
    '/a/b/c/d/e': '/aa/bb/cc/dd', '/aa/bb/cc': '/aaa/bbb', '/aaa': '/aaaa'
}))
