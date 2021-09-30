import hub75

config = hub75.Hub75SpiConfiguration()
matrix = hub75.Hub75Spi(config)

dude = [[0,0,1,1,0,0],
        [0,1,1,0,1,0],
        [0,1,1,1,0,0],
        [0,0,1,1,0,0],
        [1,1,1,1,1,1],
        [0,1,1,1,1,0],
        [0,1,0,0,1,0],
        [0,1,1,0,1,1]
        ]


row = 23
col = 0  


while True:
    
    matrix.ClearDirtyBytes()
    matrix.SetPixels(row, col, dude)
    
    col += 1
    if col > (config.COLS - 1):
        col = 0
    
    matrix.DisplayData()

