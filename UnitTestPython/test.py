import pytest
import sys


def add(a, b):

    assert isinstance(a, int)
    assert isinstance(b, int)
    return a + b


def test_add():

    assert add(1,2) == 3
    assert isinstance(add(1, 2), int)
    with pytest.raises(Exception):
        add('1', 2)
    assert add(1,4) == 3


def test_add2():

    assert add(1,2) == 3
    assert isinstance(add(1, 2), int)
    with pytest.raises(Exception):
        add('1', 2)


def test_add3():

    value = add(1,2)
    assert value == 3
    assert isinstance(value, int)
    with pytest.raises(Exception):
        add('1', 2)
    assert value == 6


def test_myoutput(capsys):  # or use "capfd" for fd-level
    print("hello")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert captured[0] == "hello\n"
    assert captured[1] == "world\n"
    print("next")
    captured = capsys.readouterr()
    assert captured[0] == "next\n"
