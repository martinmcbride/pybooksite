import unittest
import filecmp
import os

_errors = []

def _report_recursive(dcmp):
    for name in dcmp.diff_files:
        s = "DIFF file %s found in %s and %s".format(name, dcmp.left, dcmp.right)
        _errors.append(s)
    for name in dcmp.left_only:
        s = "ONLY LEFT file %s found in %s".format(name, dcmp.left)
        _errors.append(s)
    for name in dcmp.right_only:
        s = "ONLY RIGHT file %s found in %s".format(name, cmp.right)
        _errors.append(s)
    for sub_dcmp in dcmp.subdirs.values():
        _report_recursive(sub_dcmp)

class TestPublic(unittest.TestCase):

    def test_compare_files(self):
        c = filecmp.dircmp("../sample-site/reference-public", "../sample-site/public")
        _report_recursive(c)
        for e in _errors:
            print(e)
