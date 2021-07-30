import collections
from enum import Enum
from typing import Dict, List, Tuple
from nonogram.nonogram import Nonogram

class CellValue(Enum):
    WHITE = 0
    BLACK = 1

def _generate_hints(row: List[CellValue]):
    clues = []

    next_idx = 0
    while next_idx < len(row):
        try:
            next_black_index = row[next_idx:].index(CellValue.BLACK) + next_idx

            try:
                next_white_index = row[next_black_index:].index(CellValue.WHITE)
                clues.append(next_white_index)
                next_idx = next_black_index + next_white_index

            except ValueError:
                remaining_length = len(row[next_black_index:])
                clues.append(remaining_length)

                break
        except ValueError:
            next_idx = len(row)

    return tuple(clues)


def generate_nonogram(pixel_data: Dict[int, List[CellValue]]) -> Nonogram:
    """Generates nonograms based on a dict of pixeldata.

    Accepts a dict representing a black and white image. For example:
        {
            0: [CellValue.BLACK, CellValue.WHITE]
            1: [CellValue.WHITE, CellValue.BLACK]
        }
    represents a 2x2 checkerboard pattern.
    """
    cols = collections.defaultdict(list)
    for y, _ in enumerate(pixel_data):  # pylint: disable=invalid-name
        for x, _ in enumerate(pixel_data[y]):  # pylint: disable=invalid-name
            cols[x].append(pixel_data[y][x])

    row_clues: List[Tuple[int]] = [
        _generate_hints(row) for row in pixel_data.values()
    ]  # type: ignore
    col_clues: List[Tuple[int]] = [
        _generate_hints(col) for col in cols.values()
    ]  # type: ignore

    nonogram = Nonogram(row_clues=row_clues, col_clues=col_clues)

    print(nonogram)

    return nonogram
