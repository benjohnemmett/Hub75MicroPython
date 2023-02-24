import unittest
from src import matrixdata

"""
Run with 
 >  python -m unittest test/test_matrixdata.py
"""

class TestMatrixData(unittest.TestCase):

    def test_is_out_of_bounds(self):
        row_size = 32
        col_size = 64

        uut = matrixdata.MatrixData(row_size, col_size)

        self.assertFalse(uut.is_out_of_bounds(0, 0))
        self.assertFalse(uut.is_out_of_bounds(row_size-1, 0))
        self.assertFalse(uut.is_out_of_bounds(0, col_size-1))
        self.assertFalse(uut.is_out_of_bounds(row_size-1, col_size-1))
        self.assertTrue(uut.is_out_of_bounds(-1, 0))
        self.assertTrue(uut.is_out_of_bounds(0, -1))
        self.assertTrue(uut.is_out_of_bounds(row_size, 0))
        self.assertTrue(uut.is_out_of_bounds(0, col_size))
        self.assertTrue(uut.is_out_of_bounds(row_size, col_size))

    def test_set_pixel_value_red(self):
        row_size = 32
        col_size = 64
        uut = matrixdata.MatrixData(row_size, col_size)

        uut.set_pixel_value(0, 0, matrixdata.RED_VALUE)

        self.assertEqual(uut.red_matrix_data[0][0], 128)
        self.assertEqual(uut.green_matrix_data[0][0], 0)
        self.assertEqual(uut.blue_matrix_data[0][0], 0)

    def test_set_pixel_value_green(self):
        row_size = 32
        col_size = 64
        uut = matrixdata.MatrixData(row_size, col_size)

        uut.set_pixel_value(0, 1, matrixdata.GREEN_VALUE)

        self.assertEqual(uut.red_matrix_data[0][0], 0)
        self.assertEqual(uut.green_matrix_data[0][0], 64)
        self.assertEqual(uut.blue_matrix_data[0][0], 0)

    def test_set_pixel_value_blue(self):
        row_size = 32
        col_size = 64
        uut = matrixdata.MatrixData(row_size, col_size)

        uut.set_pixel_value(0, 2, matrixdata.BLUE_VALUE)

        self.assertEqual(uut.red_matrix_data[0][0], 0)
        self.assertEqual(uut.green_matrix_data[0][0], 0)
        self.assertEqual(uut.blue_matrix_data[0][0], 32)

    def test_set_right_most_pixel_value_blue(self):
        row_size = 32
        col_size = 64
        uut = matrixdata.MatrixData(row_size, col_size)
        row_to_set = 0
        uut.set_pixel_value(row_to_set, 63, matrixdata.BLUE_VALUE)

        self.assertEqual(uut.blue_matrix_data[row_to_set][7], 1)
        for row in range(row_size):
            if row == row_to_set:
                continue
            for col in range(col_size // 8):
                self.assertEqual(uut.blue_matrix_data[row][col], 0)
    
    def test_set_right_most_pixel_value_red(self):
        row_size = 32
        col_size = 64
        uut = matrixdata.MatrixData(row_size, col_size)
        row_to_set = 1
        uut.set_pixel_value(row_to_set, 63, matrixdata.RED_VALUE)

        self.assertEqual(uut.red_matrix_data[row_to_set][7], 1)
        for row in range(row_size):
            if row == row_to_set:
                continue
            for col in range(col_size // 8):
                self.assertEqual(uut.red_matrix_data[row][col], 0)


if __name__ == '__main__':
    unittest.main()