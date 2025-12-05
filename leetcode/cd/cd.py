from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from pygtrie import Trie


# ---------- 1. Basic path normalization helpers ----------

def _expand_home(path: str, home_dir: Optional[str]) -> str:
    """
    Expand '~' or '~/' at the beginning of path using home_dir.
    If home_dir is None or path doesn't start with '~', return path unchanged.
    """
    if not home_dir:
        return path
    if path == "~":
        return home_dir
    if path.startswith("~/"):
        return home_dir + path[1:]  # drop '~'
    return path


def _normalize_join(base_parts: List[str], path: str) -> Optional[List[str]]:
    """
    Normalize path components relative to base_parts.
    - If path is absolute, base_parts is ignored and we start from root.
    - If a '..' would go above root, return None to signal invalid path.
    """
    if path.startswith("/"):
        parts: List[str] = []
        tokens = path.split("/")
    else:
        parts = list(base_parts)
        tokens = path.split("/")

    for tok in tokens:
        if tok == "" or tok == ".":
            continue
        if tok == "..":
            if not parts:
                # would go above root: invalid
                return None
            parts.pop()
        else:
            parts.append(tok)

    return parts


def _normalize_path_to_parts(
        current_dir: str,
        new_dir: str,
        home_dir: Optional[str],
) -> Optional[List[str]]:
    """
    Resolve current_dir + new_dir → normalized absolute path parts.
    Returns None if path goes above root.
    """
    cur = _expand_home(current_dir, home_dir)
    new = _expand_home(new_dir, home_dir)

    if not cur.startswith("/"):
        raise ValueError("currentDir must be an absolute path")

    base_parts = _normalize_join([], cur)  # normalize current_dir itself
    if base_parts is None:
        return None

    return _normalize_join(base_parts, new)


def _normalize_absolute_path_to_parts(
        path: str,
        home_dir: Optional[str],
) -> Optional[List[str]]:
    """
    Normalize an absolute path (used for symlink keys/targets).
    Throws if given a non-absolute path.
    """
    expanded = _expand_home(path, home_dir)
    if not expanded.startswith("/"):
        raise ValueError(f"Symlink path must be absolute: {path!r}")
    return _normalize_join([], expanded)


def _parts_to_path(parts: List[str]) -> str:
    """Convert path parts back to an absolute path string."""
    return "/" if not parts else "/" + "/".join(parts)


# ---------- 2. Symlink trie building ----------

def _build_symlink_trie(
        symlinks: Dict[str, str],
        home_dir: Optional[str],
) -> Trie:
    """
    Build a Trie where:
      key   = tuple of source path components (absolute, normalized)
      value = tuple of target path components (absolute, normalized)
    """
    trie = Trie()
    for src, dst in symlinks.items():
        src_parts = _normalize_absolute_path_to_parts(src, home_dir)
        dst_parts = _normalize_absolute_path_to_parts(dst, home_dir)
        if src_parts is None or dst_parts is None:
            raise ValueError(f"Invalid symlink: {src} -> {dst}")
        trie[tuple(src_parts)] = tuple(dst_parts)
    return trie


# ---------- 3. Apply symlinks with longest-prefix logic ----------

def _apply_symlinks_from_parts(
        path_parts: List[str],
        trie: Trie,
) -> Optional[List[str]]:
    """
    Given a normalized absolute path (as parts) and a symlink Trie,
    repeatedly apply *longest-prefix* symlink rewrites.

    Returns:
      - final path parts if successful
      - None if a symlink cycle is detected
    """
    parts = list(path_parts)
    visited_keys: set[Tuple[str, ...]] = set()

    while True:
        result = trie.longest_prefix(tuple(parts))
        if not result or result.key is None:
            # no matching symlink prefix
            return parts

        key = result.key           # tuple of src parts
        target = list(result.value)  # tuple of dst parts

        if key in visited_keys:
            # cycle in symlink expansion
            return None
        visited_keys.add(key)

        # suffix after the matched prefix
        suffix = parts[len(key):]  # may be empty
        # since both key and target are already normalized component lists,
        # and suffix is from a normalized path, we can just concatenate:
        parts = target + suffix


# ---------- 4. Public API ----------

def cd(
        current_dir: str,
        new_dir: str,
        symlinks: Optional[Dict[str, str]] = None,
        home_dir: Optional[str] = None,
) -> Optional[str]:
    """
    Simulate 'cd' with:
      - current_dir: absolute path
      - new_dir: absolute or relative, may use '~' at start
      - symlinks: mapping from absolute path → absolute path (both may contain '~')
      - home_dir: absolute path for '~' expansion

    Returns:
      - final absolute path as string
      - None if path is invalid (e.g. goes above root or symlink cycle)
    """
    # 1) Basic resolution + normalization
    parts = _normalize_path_to_parts(current_dir, new_dir, home_dir)
    if parts is None:
        return None

    # 2) No symlinks: we are done
    if not symlinks:
        return _parts_to_path(parts)

    # 3) Build symlink trie (keys/values normalized & absolute)
    trie = _build_symlink_trie(symlinks, home_dir)

    # 4) Apply longest-prefix symlink rewrites with cycle detection
    final_parts = _apply_symlinks_from_parts(parts, trie)
    if final_parts is None:
        return None

    return _parts_to_path(final_parts)