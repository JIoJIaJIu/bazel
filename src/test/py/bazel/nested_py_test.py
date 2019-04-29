import os
import unittest
from src.test.py.bazel import test_base
from datetime import datetime, timedelta

class NestedBazelTest(test_base.TestBase):
    def setUp(self):
        super(NestedBazelTest, self).setUp()
        self.ScratchFile('WORKSPACE', [
            'workspace(name = "nested_py_workspace")'
        ])
        self.ScratchFile('test.py', [
            'print("test")'
        ])
        self.ScratchFile('run.py', [
            'print("run")'
        ])

    def testNestedPyTest(self):
        self.ScratchFile('BUILD', [
            'py_test(',
            '   name = "test",',
            '   srcs = ["test.py"],',
            ')'
        ])
        s = datetime.now()

        exit_code, stdout, stderr = self.RunBazel([
            #'query', '--show_timestamps', 'deps(@nested_py_workspace//:test)'
            'run', '--show_timestamps', '@nested_py_workspace//:test'
        ])

        elapsed = datetime.now() - s

        self.assertEqual(exit_code, 0, os.linesep.join(stderr))
        self.assertFalse(elapsed > timedelta(minutes=1),
                "{}ms.\n{}".format(elapsed, os.linesep.join(stdout)) )

    def testNestedPyBinary(self):
        self.ScratchFile('BUILD', [
            'py_binary(',
            '   name = "run",',
            '   srcs = ["run.py"],',
            ')'
        ])
        s = datetime.now()

        exit_code, stdout, stderr = self.RunBazel([
            #'query', '--show_timestamps', 'deps(@nested_py_workspace//:run)'
            'run', '--show_timestamps', '@nested_py_workspace//:run'
        ])

        elapsed = datetime.now() - s

        self.assertEqual(exit_code, 0, os.linesep.join(stderr))
        self.assertFalse(elapsed > timedelta(minutes=1),
                "{}ms.\n{}".format(elapsed, os.linesep.join(stdout)) )


if __name__ == '__main__':
  unittest.main()
