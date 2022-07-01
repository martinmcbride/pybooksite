import unittest
import filecmp

"""
Running pybooksite on the sample site creates a collection of all the files needed for deployment, in the public folder.

There is also a set of known good files in the reference-public folder.

This test does a full recursive comapre of every file in every subfolder of these two folders. This is a quick way to 
check that nothing has changed.

It is necessary to run pybooksite to recreate all the files in the public area before executing this test.

If the code changes in such a way that the outpiut files are expected to have changed, you should check that the new
files are correct, then update the reference files in the reference-public folder, and check them in.
"""

_errors = []

def _report_recursive(dcmp):
    for name in dcmp.diff_files:
        s = "DIFF file {} found in {} and {}".format(name, dcmp.left, dcmp.right)
        _errors.append(s)
    for name in dcmp.left_only:
        s = "ONLY LEFT file {} found in {}".format(name, dcmp.left)
        _errors.append(s)
    for name in dcmp.right_only:
        s = "ONLY RIGHT file {} found in {}".format(name, dcmp.right)
        _errors.append(s)
    for sub_dcmp in dcmp.subdirs.values():
        _report_recursive(sub_dcmp)

class TestPublic(unittest.TestCase):

    def test_compare_files(self):
        c = filecmp.dircmp("../sample-site/reference-public", "../sample-site/public")
        _report_recursive(c)
        for e in _errors:
            print(e)
        self.assertEquals([], _errors)

