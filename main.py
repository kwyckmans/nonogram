import collections

from PIL import Image

from generator.generator import CellValue, NonogramGenerator

NONOGRAM_WIDTH = 25
NONOGRAM_HEIGHT = 25

def get_aspect_ratio(image: Image.Image) -> float:
    width, height = image.size
    return width / height


def resize_to_nonogram_size(image: Image.Image) -> Image.Image:
    width, height = image.size
    rescaled_nonogram_height = round((height / width) * NONOGRAM_HEIGHT)
    return image.resize((NONOGRAM_WIDTH, rescaled_nonogram_height))


if __name__ == "__main__":
    with Image.open("turing.jpeg") as source_image:
        resized_im = resize_to_nonogram_size(source_image)
        black_white_im = resized_im.convert(mode="1")
        # black_white_im.show()
        resized_width, resized_height = black_white_im.size
        pixel_data = black_white_im.load()

        rows = collections.defaultdict(list)

        for y in range(0, resized_height - 1):
            for x in range(0, resized_width - 1):
                rows[y].append(
                    CellValue.BLACK
                    if pixel_data[x, y] == 0 # type: ignore
                    else CellValue.WHITE
                )

        generator = NonogramGenerator(rows)
        generator.generate()
