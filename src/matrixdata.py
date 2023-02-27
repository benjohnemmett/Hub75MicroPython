BLUE_VALUE = 1
GREEN_VALUE = 2
RED_VALUE = 4

class MatrixData:
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size

        self.col_bytes = col_size // 8

        self.red_matrix_data = [bytearray(self.col_bytes) for x in range(row_size)]
        self.green_matrix_data = [bytearray(self.col_bytes) for x in range(row_size)]
        self.blue_matrix_data = [bytearray(self.col_bytes) for x in range(row_size)]
        
        self.dirty_bytes_array = []

    def set_pixels(self, row, col, array):
        for r in range(len(array)):
            for c in range(len(array[0])):
                if array[r][c]:
                    self.set_pixel_value(row + r, col + c, array[r][c])

    def set_pixel_value(self, row, col, val):
        if (self.is_out_of_bounds(row, col)):
            return
        
        cIndex = col // 8
        byteIndex = 7 - (col % 8)

        if val & RED_VALUE:
            self.red_matrix_data[row][cIndex] |= (1 << byteIndex)
        if val & GREEN_VALUE:
            self.green_matrix_data[row][cIndex] |= (1 << byteIndex)
        if val & BLUE_VALUE:
            self.blue_matrix_data[row][cIndex] |= (1 << byteIndex)
        
        self.dirty_bytes_array.append((row,col//8))
    
    def is_out_of_bounds(self, row, col):
        return (row < 0 or row >= self.row_size or col < 0 or col >= self.col_size)

    def clear_dirty_bytes(self):
        for index in self.dirty_bytes_array:
            self.red_matrix_data[index[0]][index[1]] = 0
            self.green_matrix_data[index[0]][index[1]] = 0
            self.blue_matrix_data[index[0]][index[1]] = 0
            
        self.dirty_bytes_array = []
