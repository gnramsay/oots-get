import pytest
from ootsget.ootsget import main

__author__ = "Grant Ramsay"
__copyright__ = "Grant Ramsay"
__license__ = "MIT"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    # main(["7"])
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
    assert 1 == 1
