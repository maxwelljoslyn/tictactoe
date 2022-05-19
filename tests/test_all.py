from tictac import Board
import textwrap
import pytest

# @pytest.mark.xfail("")


# TODO programmatically check all 2^9 possible boards w/ brute force... only 512 states


def test_beginning_of_game():
    b = Board(
        [None, None, None],
        [None, None, None],
        [None, None, None],
    )
    # all spots are open
    assert len(b.open_spots) == sum([len(r) for r in b.rows])
    # first move is 'x'
    assert b.next_move == "x"


def test_next_move_y():
    b = Board(
        [None, "x", None],
        [None, None, None],
        [None, None, None],
    )
    assert b.next_move == "y"


def test_not_over_yet():
    b = Board(
        ["y", "x", "x"],
        ["x", "y", "x"],
        ["y", "x", None],
    )
    assert not b.game_over


def test_stalemate():
    b = Board(
        ["x", "y", "x"],
        ["y", "x", "x"],
        ["y", "x", "y"],
    )
    assert b.game_over and b.end_with_stalemate


def test_x_win_row1():
    b = Board(
        ["x", "x", "x"],
        ["y", "y", "x"],
        ["y", "x", "y"],
    )

    assert (
        b.game_over
        and (b.end_with_winner[0] == [(0, 0), (0, 1), (0, 2)])
        and (b.end_with_winner[1] == "x")
    )


def test_y_win_diag_ltr():
    b = Board(
        ["y", "x", "x"],
        ["x", "y", "x"],
        ["y", "x", "y"],
    )
    assert (
        b.game_over
        and (b.end_with_winner[0] == [(0, 0), (1, 1), (2, 2)])
        and (b.end_with_winner[1] == "y")
    )


def test_stringify():
    """Just to make sure a test hollers if I change __str__ on accident."""
    b = Board(
        [None, None, None],
        [None, None, None],
        [None, None, None],
    )
    assert str(b) == textwrap.dedent(
        """\
-|-|-
-|-|-
-|-|-"""
    )
