import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import merkle_index
from merkle_index import MerkleTree


class IndexedMerkleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, root, name, data=b"before"):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_update_equals_rebuild_across_fanouts_and_boundaries(self):
        for fanout in [2, 3, 4, 16]:
            for count in [1, fanout, fanout + 1, fanout * fanout + 1]:
                with self.subTest(fanout=fanout, count=count):
                    root = self.root / f"{fanout}-{count}"
                    root.mkdir()
                    for index in range(count):
                        self.write(root, f"sub/file-{index:04}")
                    self.write(root, "unchanged/leaf")
                    service = MerkleTree(fanout)
                    original = service.build(root)
                    updated = service.build(root)
                    unaffected = updated.children["unchanged"].content
                    for position in [0, count - 1]:
                        name = f"sub/file-{position:04}"
                        self.write(root, name, f"new-{position}".encode())
                        service.update_file(name, updated)
                        self.assertEqual(updated.content, service.build(root).content)
                        self.assertEqual(updated.children["unchanged"].content, unaffected)
                    expected_names = sorted({f"sub/file-{i:04}" for i in [0, count - 1]})
                    self.assertEqual(service.diff(original, updated),
                                     [(name, "modified") for name in expected_names])

    def test_4096_entries_update_only_three_virtual_groups(self):
        # Real on-disk fixture: 4,096 filesystem entries inside one directory.
        for index in range(4096):
            self.write(self.root, f"file-{index:04}")
        service = MerkleTree(16)
        tree = service.build(self.root)
        old_root = tree.content
        unchanged_leaf = tree.children["file-4095"].entry_leaf
        untouched_group = unchanged_leaf.parent
        old_group_hash = untouched_group.content
        self.write(self.root, "file-0000", b"after")
        with patch("merkle_index._group_hash", wraps=merkle_index._group_hash) as hash_group:
            service.update_file("file-0000", tree)
            self.assertEqual(hash_group.call_count, 3)
        self.assertNotEqual(tree.content, old_root)
        self.assertEqual(untouched_group.content, old_group_hash)
        self.assertEqual(tree.content, service.build(self.root).content)

    def test_deterministic_names_order_and_empty_directory(self):
        a, b = self.root / "a", self.root / "b"
        a.mkdir()
        b.mkdir()
        names = ["z", "a", "newline\n雪", "space name", "nested/file"]
        for name in names:
            self.write(a, name)
        for name in reversed(names):
            self.write(b, name)
        (a / "empty").mkdir()
        (b / "empty").mkdir()
        service = MerkleTree(3)
        left, right = service.build(a), service.build(b)
        self.assertEqual(left.content, right.content)
        self.assertEqual(service.diff(left, right), [])
        self.assertEqual(service.get_hash(".", left), left.content)
        self.assertEqual(left.children["empty"].index_root.children, ())

    def test_noop_update_does_not_hash_groups(self):
        self.write(self.root, "sub/file")
        service = MerkleTree()
        tree = service.build(self.root)
        with patch("merkle_index._group_hash", wraps=merkle_index._group_hash) as hash_group:
            self.assertEqual(service.update_file("sub/file", tree), tree.content)
            hash_group.assert_not_called()

    def test_replaced_type_symlink_and_invalid_path_do_not_mutate(self):
        self.write(self.root, "file")
        service = MerkleTree()
        tree = service.build(self.root)
        original_hash = tree.content
        (self.root / "file").unlink()
        (self.root / "file").mkdir()
        with self.assertRaises(ValueError):
            service.update_file("file", tree)
        self.assertEqual(tree.content, original_hash)
        (self.root / "file").rmdir()
        self.write(self.root, "target")
        (self.root / "file").symlink_to("target")
        with self.assertRaises(ValueError):
            service.update_file("file", tree)
        self.assertEqual(tree.content, original_hash)
        with self.assertRaises(KeyError):
            service.update_file("missing", tree)
        for name in ["../file", "/file"]:
            with self.assertRaises(ValueError):
                service.get_hash(name, tree)

    def test_diff_membership_and_replacement(self):
        a, b = self.root / "a", self.root / "b"
        a.mkdir()
        b.mkdir()
        self.write(a, "removed/child")
        self.write(b, "added/child")
        self.write(a, "replace")
        (b / "replace").mkdir()
        service = MerkleTree()
        self.assertEqual(service.diff(service.build(a), service.build(b)),
                         [("added", "added"), ("removed", "removed"),
                          ("replace", "modified")])

    def test_fanout_validation_and_incompatible_diff(self):
        for value in [0, 1, True, 2.5]:
            with self.assertRaises(ValueError):
                MerkleTree(value)
        small = MerkleTree(2).build(self.root)
        large = MerkleTree(16).build(self.root)
        with self.assertRaises(ValueError):
            MerkleTree().diff(small, large)


if __name__ == "__main__":
    unittest.main()
