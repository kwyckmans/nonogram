import collections
from generator.generator import NonogramGenerator, CellValue
from PIL import Image

NONOGRAM_WIDTH = 25
NONOGRAM_HEIGHT = 25

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