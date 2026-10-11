import hashlib
import tempfile
import unittest
from pathlib import Path
from merkle_tree import Inode, MerkleTree


class MerkleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.a = self.root / 'A'
        self.b = self.root / 'B'
        self.a.mkdir()
        self.b.mkdir()
        self.m = MerkleTree()

    def write(self, root, name, data=b'hello'):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_determinism_and_lookup(self):
        for name in ['z.txt', 'sub/a.txt', 'empty.txt', 'space newline\n雪']:
            self.write(self.a, name, b'' if name == 'empty.txt' else b'hello')
        for name in reversed(['z.txt', 'sub/a.txt', 'empty.txt', 'space newline\n雪']):
            self.write(self.b, name, b'' if name == 'empty.txt' else b'hello')
        a, b = self.m.build(self.a), self.m.build(self.b)
        self.assertEqual(a.content, b.content)
        self.assertEqual(self.m.diff(a, b), [])
        self.assertEqual(self.m.get_hash('.', a), a.content)
        expected = hashlib.sha256(b'file\0hello').hexdigest()
        self.assertEqual(self.m.get_hash('sub/a.txt', a), expected)
        for missing in ['missing', 'z.txt/child']:
            with self.assertRaises(KeyError):
                self.m.get_hash(missing, a)
        for invalid in ['/absolute', '../outside']:
            with self.assertRaises(ValueError):
                self.m.get_hash(invalid, a)
        self.write(self.a, 'sub/a.txt', b'changed')
        self.assertEqual(self.m.get_hash('sub/a.txt', a), expected)

    def test_add_remove_modify_and_replace(self):
        for root in [self.a, self.b]:
            self.write(root, 'nested/edit', b'before')
            self.write(root, 'root-edit', b'before')
        self.write(self.b, 'nested/edit', b'after')
        self.write(self.b, 'root-edit', b'after')
        self.write(self.a, 'removed-file')
        self.write(self.a, 'removed-dir/child')
        self.write(self.b, 'added-file')
        self.write(self.b, 'added-dir/child')
        self.write(self.a, 'file-to-dir')
        (self.b / 'file-to-dir').mkdir()
        (self.a / 'dir-to-file').mkdir()
        self.write(self.b, 'dir-to-file')
        expected = [('added-dir', 'added'), ('added-file', 'added'),
                    ('dir-to-file', 'modified'), ('file-to-dir', 'modified'),
                    ('nested/edit', 'modified'), ('removed-dir', 'removed'),
                    ('removed-file', 'removed'), ('root-edit', 'modified')]
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)), expected)

    def test_merkle_property(self):
        self.write(self.a, 'src/utils/helpers.py', b'before')
        self.write(self.a, 'assets/logo', b'unchanged')
        before = self.m.build(self.a)
        self.write(self.a, 'src/utils/helpers.py', b'after')
        after = self.m.build(self.a)
        for path in ['.', 'src', 'src/utils', 'src/utils/helpers.py']:
            self.assertNotEqual(self.m.get_hash(path, before), self.m.get_hash(path, after))
        for path in ['assets', 'assets/logo']:
            self.assertEqual(self.m.get_hash(path, before), self.m.get_hash(path, after))
        self.assertEqual(self.m.diff(before, after), [('src/utils/helpers.py', 'modified')])

    def test_empty_directory_and_rename(self):
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)), [])
        self.write(self.a, 'old')
        self.write(self.b, 'new')
        (self.b / 'empty').mkdir()
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)),
                         [('empty', 'added'), ('new', 'added'), ('old', 'removed')])

    def test_large_file(self):
        data = b'x' * (2 * 1024 * 1024 + 7)
        self.write(self.a, 'large', data)
        tree = self.m.build(self.a)
        self.assertEqual(self.m.get_hash('large', tree), hashlib.sha256(b'file\0' + data).hexdigest())

    def test_equal_subtrees_are_not_traversed(self):
        for root in [self.a, self.b]:
            self.write(root, 'assets/icons/home')
        self.write(self.a, 'src/main', b'before')
        self.write(self.b, 'src/main', b'after')
        a, b = self.m.build(self.a), self.m.build(self.b)

        class FailOnIteration(list):
            def __iter__(self):
                raise AssertionError('Visited children of an equal subtree')

        for tree in [a, b]:
            assets = next(c for c in tree.children if c.name == 'assets')
            assets.children = FailOnIteration(assets.children)
        self.assertEqual(self.m.diff(a, b), [('src/main', 'modified')])

    def test_symlink_rejected(self):
        self.write(self.a, 'file')
        (self.a / 'link').symlink_to('file')
        with self.assertRaises(ValueError):
            self.m.build(self.a)


if __name__ == '__main__':
    unittest.main()
