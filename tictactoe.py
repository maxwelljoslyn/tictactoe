"""Tic-Tac-Toe with a command line interface."""
import textwrap

row_lines = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
]

# the first list in columns is read from top left to bottom left on the game board
column_lines = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
]
diagonal_lines = [
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]


class Board:
    def __init__(self, row0=None, row1=None, row2=None):
        self.tokens = ("x", "y")
        self.rows = []
        self.rows.append(row0 if row0 else [None, None, None])
        self.rows.append(row1 if row1 else [None, None, None])
        self.rows.append(row2 if row2 else [None, None, None])

    def __str__(self):
        def h(thing):
            return thing.upper() if thing in self.tokens else "-"

        # for convenience in f-string
        r0 = self.rows[0]
        r1 = self.rows[1]
        r2 = self.rows[2]
        return textwrap.dedent(
            f"""\
    {h(r0[0])}|{h(r0[1])}|{h(r0[2])}
    {h(r1[0])}|{h(r1[1])}|{h(r1[2])}
    {h(r2[0])}|{h(r2[1])}|{h(r2[2])}"""
        )

    @property
    def next_move(self):
        if self.game_over:
            return None
        elif len(self.open_spots) == sum([len(r) for r in self.rows]):
            return self.tokens[0]
        else:
            moves = self.each_player_moves_so_far
            if len(moves[self.tokens[0]]) > len(moves[self.tokens[1]]):
                return self.tokens[1]
            else:
                return self.tokens[0]

    @property
    def each_player_moves_so_far(self):
        result = {t: [] for t in self.tokens}
        for row in (0, 1, 2):
            for col in (0, 1, 2):
                who = self.rows[row][col]
                if who in self.tokens:
                    result[who].append((row, col))
        return result

    @property
    def open_spots(self):
        # TODO smarter way to implement this as "inverse" of self.rows?
        return [(x, y) for x in (0, 1, 2) for y in (0, 1, 2) if self.rows[x][y] is None]

    @property
    def moves_so_far(self):
        # TODO redundancy with each_player_moves_so_far; rewrite
        return [
            (x, y) for x in (0, 1, 2) for y in (0, 1, 2) if self.rows[x][y] is not None
        ]

    @property
    def end_with_winner(self):
        for win_type in row_lines + column_lines + diagonal_lines:
            contents = [self.rows[x][y] for (x, y) in win_type]
            if not all(contents):
                # there's a None present
                continue
            elif contents[0] == contents[1] == contents[2]:
                # winner!
                return win_type, contents[0]
            else:
                continue
        return False

    @property
    def end_with_stalemate(self):
        return (not self.end_with_winner) and (not self.open_spots)

    @property
    def game_over(self):
        return self.end_with_winner or self.end_with_stalemate

    def make_move(self, token, spot):
        if token not in self.tokens:
            raise ValueError
        if spot not in self.open_spots:
            raise ValueError


def main():
    board = Board()
    print("Tic-Tac-Toe ... for One")
    while not board.game_over:
        print()
        print(board)
        print()
        player = board.next_move
        print("Open spots are: ", "; ".join([f"{a}, {b}" for a, b in board.open_spots]))
        move = input(player.upper() + "'s move: ")
        if "," not in move:
            print("Please enter your move in this format: ROW, COL")
            continue
        try:
            move = [int(q) for q in move.strip(", \n\t").split(",")]
        except ValueError:
            print("You seem to have entered a non-number. Please try again.")
            continue
        if len(move) != 2:
            print("Please enter your move in this format: ROW, COL")
            continue
        x, y = move
        if (x, y) not in board.open_spots:
            print("Sorry, that's an invalid move. Please try again.")
            continue
        else:
            board.rows[x][y] = player
    print(board)
    if board.end_with_stalemate:
        print("Stalemate.")
    else:
        print(f"{board.end_with_winner[1].upper()} wins.")


if __name__ == "__main__":
    main()
