import hub75

config = hub75.Hub75SpiConfiguration()
matrix = hub75.Hub75Spi(config)

row = 0
col = 0  

while True:
    matrix.DisplayData()

    matrix.ClearPixelValue(row, col)
    
    row = row + 1
    if row > (config.ROWS - 1):
        row = 0
        col += 1
    if col > (config.COLS - 1):
        col = 0
        
    matrix.SetPixelValue(row, col)
    

