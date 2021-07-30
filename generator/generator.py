from enum import Enum
from nonogram.nonogram import Nonogram
from typing import Dict, List

import collections
from PIL import Image

NONOGRAM_WIDTH = 25
NONOGRAM_HEIGHT = 25

class CellValue(Enum):
    WHITE = 0
    BLACK = 1

class NonogramGenerator:
    """Generates nonograms based on a dict of pixeldata.

    Accepts a dict representing a black and white image. For example:
        {
            0: [CellValue.BLACK, CellValue.WHITE]
            1: [CellValue.WHITE, CellValue.BLACK]
        }
    represents a 2x2 checkerboard pattern.
    """
    def __init__(self, pixel_data: Dict[int, List[CellValue]]) -> None:
        self._pixel_data = pixel_data
        self._clues = []

    def _generate_hints(self, row: List[CellValue]):
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

    def generate(self) -> Nonogram:
        cols = collections.defaultdict(list)
        for y in range(0, len(self._pixel_data)):
            for x in range(0, len(self._pixel_data[y])):
                cols[x].append(self._pixel_data[y][x])

        row_clues = [self._generate_hints(row) for row in self._pixel_data.values()]
        col_clues = [self._generate_hints(col) for col in cols.values()]

        nonogram = Nonogram(
            row_clues = row_clues,
            col_clues = col_clues
        )

        print(nonogram)

        return nonogram
        
def get_aspect_ratio(im: Image.Image) -> float:
    width, height = im.size
    return width / height

def resize_to_nonogram_size(im: Image.Image) -> Image.Image:
    width, height = im.size
    rescaled_nonogram_height = round((height / width) * NONOGRAM_HEIGHT)
    return im.resize((NONOGRAM_WIDTH, rescaled_nonogram_height))

if __name__=="__main__":
    with Image.open("turing.jpeg") as im:
        resized_im = resize_to_nonogram_size(im)
        black_white_im = resized_im.convert(mode='1')
        # black_white_im.show()
        width, height = black_white_im.size
        print(width, height)
        pixel_data = black_white_im.load()

        rows = collections.defaultdict(list)

        for y in range(0, height - 1):
            for x in range(0 , width - 1):
                rows[y].append(CellValue.BLACK if pixel_data[x, y] == 0 else CellValue.WHITE) #type: ignore

        generator = NonogramGenerator(rows)
        generator.generate()

