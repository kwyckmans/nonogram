# Clues are something like

#       1     1
# 1 2   x     x
# 1 2   x     x

# So each row has row clues, each column has column clues.
# Ideally I can do something like clues[row][column] to get the clues. 
# That being said, if I do that, there's still two options: specifying a coordinate
# gives me both row and column clues, so, I need to specify that too.
# So either clues[row][column] returns both, or I add two methods
# get_row_clues(row), get_column_clues(col)


from typing import List, Tuple


class Nonogram:
    def __init__(self, row_clues: List[Tuple[int]], col_clues: List[Tuple[int]]) -> None:
        self.row_clues = row_clues
        self.col_clues = col_clues

    def __str__(self) -> str:
        output = ""
        output += "Row clues: \n"
        for clue in self.row_clues:
            output += ' '.join(list(map(lambda c: str(c),clue))) + '\n'

        output += "Column clues: \n"
        for clue in self.col_clues:
            output += ' '.join(list(map(lambda c: str(c),clue))) + '\n'

        return output