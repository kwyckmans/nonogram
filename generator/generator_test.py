from generator.generator import NonogramGenerator
from generator.generator import CellValue
from typing import Generator
import unittest

class GeneratorTest(unittest.TestCase):
    """Tests generation of nonograms by providing the generator with various pixel configurations.

    TODO: add a single end-to-end test with a very simple image.
    """
    def test_generator_for_full_black_row(self):
        pixel_data = {
            0: [CellValue.BLACK, CellValue.BLACK]
        }
        generator = NonogramGenerator(pixel_data=pixel_data)
        nonogram = generator.generate()
        self.assertIsNotNone(nonogram)

        self.assertEquals(nonogram.row_clues, [(2,)])
        self.assertEquals(nonogram.col_clues, [(1,), (1,)])

    def test_generator_for_full_white_row(self):
        pixel_data = {
            0: [CellValue.WHITE, CellValue.WHITE]
        }
        generator = NonogramGenerator(pixel_data=pixel_data)
        nonogram = generator.generate()
        self.assertIsNotNone(nonogram)
        self.assertEquals(nonogram.row_clues, [()])
        self.assertEquals(nonogram.col_clues, [(), ()])


    def test_generator_for_black_in_back_sequence(self):
        pixel_data = {
            0: [CellValue.WHITE, CellValue.BLACK]
        }
        generator = NonogramGenerator(pixel_data=pixel_data)
        nonogram = generator.generate()
        self.assertIsNotNone(nonogram)
        self.assertEquals(nonogram.row_clues, [(1,)])
        self.assertEquals(nonogram.col_clues, [(), (1,)])

    
    def test_generator_for_black_in_front_sequence(self):
        pixel_data = {
            0: [CellValue.BLACK, CellValue.WHITE]
        }
        generator = NonogramGenerator(pixel_data=pixel_data)
        nonogram = generator.generate()
        self.assertIsNotNone(nonogram)
        self.assertEquals(nonogram.row_clues, [(1,)])
        self.assertEquals(nonogram.col_clues, [(1, ), ()])

if __name__ == '__main__':
    unittest.main()
