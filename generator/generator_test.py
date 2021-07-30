import unittest

from generator.generator import CellValue, generate_nonogram


class GeneratorTest(unittest.TestCase):
    """Tests generation of nonograms by providing the generator with various pixel configurations.

    TODO: add a single end-to-end test with a very simple image.
    """

    def test_generator_for_full_black_row(self):
        pixel_data = {0: [CellValue.BLACK, CellValue.BLACK]}
        nonogram = generate_nonogram(pixel_data=pixel_data)
        self.assertIsNotNone(nonogram)

        self.assertEqual(nonogram.row_clues, [(2,)])
        self.assertEqual(nonogram.col_clues, [(1,), (1,)])

    def test_generator_for_full_white_row(self):
        pixel_data = {0: [CellValue.WHITE, CellValue.WHITE]}
        nonogram = generate_nonogram(pixel_data=pixel_data)
        self.assertIsNotNone(nonogram)
        self.assertEqual(nonogram.row_clues, [()])
        self.assertEqual(nonogram.col_clues, [(), ()])

    def test_generator_for_black_in_back_sequence(self):
        pixel_data = {0: [CellValue.WHITE, CellValue.BLACK]}
        nonogram = generate_nonogram(pixel_data=pixel_data)
        self.assertIsNotNone(nonogram)
        self.assertEqual(nonogram.row_clues, [(1,)])
        self.assertEqual(nonogram.col_clues, [(), (1,)])

    def test_generator_for_black_in_front_sequence(self):
        pixel_data = {0: [CellValue.BLACK, CellValue.WHITE]}
        nonogram = generate_nonogram(pixel_data=pixel_data)
        self.assertIsNotNone(nonogram)
        self.assertEqual(nonogram.row_clues, [(1,)])
        self.assertEqual(nonogram.col_clues, [(1,), ()])


if __name__ == "__main__":
    unittest.main()
