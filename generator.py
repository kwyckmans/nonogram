from enum import Enum
from typing import Dict, List

import collections
from PIL import Image

NONOGRAM_WIDTH = 25
NONOGRAM_HEIGHT = 25

class CellValue(Enum):
    WHITE = 0
    BLACK = 1

class NonogramGenerator:
    def __init__(self, pixel_data: Dict[int, List[CellValue]]) -> None:
        self._clues = []

        # TODO: I don't want this class to be connected to pillow at all.
        #   I want it to accept just a 2D list of {0, 255} values.
        #   Something like:
        #      [
        #        [0,   0,   0]
        #        [255, 255, 0]    
        #      ]
        #   This would allow me to easily test this class and to replace pillow 
        #   if I ever wanted to
        # I did this, but capture it in a comment
        self._pixel_data = pixel_data

    def _generate_hints(self, row: List[CellValue]):
        print(f"generating hints for {row}")
        clues = []
        
        next_idx = 0
        while next_idx < len(row):
            try:
                next_black_index = row[next_idx:].index(CellValue.BLACK) + next_idx
                print(f"next black index: {next_black_index}")
                try:
                    next_white_index = row[next_black_index:].index(CellValue.WHITE)
                    print(f"next white index: {next_white_index}")
                    clues.append(next_white_index)
                    next_idx = next_black_index + next_white_index
                    print(f"next index: {next_idx}")
                except ValueError:
                    remaining_length = len(row[next_black_index:])
                    clues.append(remaining_length)
                    next_idx = remaining_length
            except ValueError:
                next_idx = len(row)

        print(f"generated clues: {clues}")

    def generate(self):
        cols = collections.defaultdict(list)
        for y in range(0, len(self._pixel_data)):
            for x in range(0, len(self._pixel_data[y])):
                cols[x].append(self._pixel_data[y][x])
                            
        self._generate_hints([CellValue.WHITE,CellValue.WHITE,CellValue.BLACK,CellValue.WHITE])

def get_aspect_ratio(im: Image.Image) -> float:
    width, height = im.size
    return width / height

def resize_to_nonogram_size(im: Image.Image) -> Image.Image:
    width, height = im.size
    rescaled_nonogram_height = round((height / width) * NONOGRAM_HEIGHT)
    return im.resize((NONOGRAM_WIDTH, rescaled_nonogram_height))

with Image.open("turing.jpeg") as im:
    resized_im = resize_to_nonogram_size(im)
    black_white_im = resized_im.convert(mode='1')
    black_white_im.show()
    width, height = black_white_im.size
    print(width, height)
    pixel_data = black_white_im.load()

    rows = collections.defaultdict(list)

    for y in range(0, height - 1):
        for x in range(0 , width - 1):
            rows[y].append(CellValue.BLACK if pixel_data[x, y] == 0 else CellValue.WHITE) #type: ignore

    generator = NonogramGenerator(rows)
    generator.generate()

