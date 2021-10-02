import hub75

config = hub75.Hub75SpiConfiguration()
matrix = hub75.Hub75Spi(config)

earth = [[0,0,3,3,7,3,0,0],
        [0,2,1,2,2,3,3,0],
        [1,2,2,2,2,2,2,1],
        [1,1,2,2,2,2,1,2],
        [1,1,2,2,1,1,1,2],
        [1,1,1,2,1,1,1,1],
        [0,3,3,3,2,1,2,0],
        [0,0,3,3,7,3,0,0]
        ]

row = 23
col = 0
drow = 1
dcol = 2

while True:
    
    matrix.ClearDirtyBytes()
    matrix.SetPixels(row, col, earth)
    
    col += dcol
    if (col > (config.COLS - 1 - 8)) or (col < 0):
        dcol = -1 * dcol
        col += dcol
        
    row += drow
    if (row > (config.ROWS - 1 - 8)) or (row < 0):
        drow = -1 * drow
        row += drow
    
    matrix.DisplayData()
