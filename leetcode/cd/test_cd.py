from cd import cd


# ---------- 1. Basic normalization tests (no symlinks) ----------

def test_basic_relative():
    assert cd("/foo/bar", "baz") == "/foo/bar/baz"


def test_basic_absolute():
    assert cd("/x/y", "/a/b") == "/a/b"


def test_dot_and_dotdot():
    assert cd("/a/b/c", "../d") == "/a/b/d"
    assert cd("/a", "./b") == "/a/b"
    assert cd("/a/b/c", "../..") == "/a"


def test_dotdot_above_root_invalid():
    assert cd("/", "../x") is None
    assert cd("/", "../../..") is None


# ---------- 2. Home directory expansion (~) ----------

def test_home_only():
    assert cd("/x", "~", home_dir="/home/me") == "/home/me"


def test_home_subpath():
    assert cd("/x", "~/proj", home_dir="/home/me") == "/home/me/proj"


def test_home_no_expand_elsewhere():
    # '~' in the middle should not be expanded
    assert cd("/x", "foo/~", home_dir="/home/me") == "/x/foo/~"


# ---------- 3. Single symlink rewrite ----------

def test_single_symlink_prefix():
    symlinks = {
        "/foo/bar": "/abc",
    }
    # /foo/bar/baz --> longest prefix = /foo/bar --> /abc/baz
    assert cd("/foo/bar", "baz", symlinks=symlinks) == "/abc/baz"


# ---------- 4. Multiple symlinks, longest-prefix matching ----------

def test_longest_prefix_wins():
    symlinks = {
        "/foo/bar": "/abc",
        "/foo/bar/baz": "/xyz",
    }
    # /foo/bar/baz/qux matches /foo/bar/baz (longer), not /foo/bar
    assert cd("/foo/bar", "baz/qux", symlinks=symlinks) == "/xyz/qux"


# ---------- 5. Shorter prefix still matters ----------

def test_shorter_prefix_still_used_for_other_paths():
    symlinks = {
        "/foo/bar": "/A",
        "/foo/bar/baz": "/B",
    }
    # Longer prefix exists, but this path only matches the shorter one
    assert cd("/foo/bar", "qux", symlinks=symlinks) == "/A/qux"


# ---------- 6. Symlink chain expansion ----------

def test_symlink_chain():
    symlinks = {
        "/p": "/q",
        "/q": "/r",
        "/r/s": "/Z",
    }
    # /p/s --> /q/s --> /r/s --> /Z
    assert cd("/p", "s", symlinks=symlinks) == "/Z"


# ---------- 7. Chain with intermediate suffix components ----------

def test_symlink_chain_with_suffix():
    symlinks = {
        "/a/b": "/x",
        "/x/c": "/y",
    }
    # /a/b/c/d:
    #   prefix /a/b => /x/c/d
    #   prefix /x/c => /y/d
    assert cd("/a/b", "c/d", symlinks=symlinks) == "/y/d"


# ---------- 8. Exact match symlink (no infinite loop) ----------

def test_exact_match_symlink():
    symlinks = {
        "/foo": "/bar",
    }
    # cd("/foo", ".") should resolve /foo via symlink to /bar
    assert cd("/foo", ".", symlinks=symlinks) == "/bar"


# ---------- 9. Symlink cycle detection ----------

def test_symlink_cycle():
    symlinks = {
        "/a": "/b",
        "/b": "/a",
    }
    # Any path under /a or /b must detect cycle
    assert cd("/", "a", symlinks=symlinks) is None
    assert cd("/", "b", symlinks=symlinks) is None


# ---------- 10. Mixed case: home dir + symlink + relative path ----------

def test_home_and_symlink_and_relative():
    symlinks = {
        "/home/me/work": "/mnt/W",
    }
    # ~/work/src --> /home/me/work/src --> /mnt/W/src
    assert cd("/x", "~/work/src", symlinks=symlinks, home_dir="/home/me") == "/mnt/W/src"


# ---------- 11. Multi-level prefixes ----------

def test_multi_level_prefixes():
    symlinks = {
        "/a": "/A",
        "/a/b": "/B",
        "/a/b/c": "/C",
        "/a/b/c/d": "/D",  # deepest
    }
    # longest prefix applies
    assert cd("/a/b/c", "d/e", symlinks=symlinks) == "/D/e"
    # next shorter
    assert cd("/a/b/c", "x", symlinks=symlinks) == "/C/x"
    # even shorter
    assert cd("/a/b", "x/y", symlinks=symlinks) == "/B/x/y"