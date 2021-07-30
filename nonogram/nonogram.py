from typing import List, Tuple


class Nonogram:
    def __init__(
        self, row_clues: List[Tuple[int]], col_clues: List[Tuple[int]]
    ) -> None:
        self.row_clues = row_clues
        self.col_clues = col_clues

    def __str__(self) -> str:
        output = ""
        output += "Row clues: \n"
        for clue in self.row_clues:
            output += " ".join(list(map(str, clue))) + "\n"

        output += "Column clues: \n"
        for clue in self.col_clues:
            output += " ".join(list(map(str, clue))) + "\n"

        return output
