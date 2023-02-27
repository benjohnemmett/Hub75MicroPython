import hub75
import matrixdata
from logo import logo
from whale import SquirtyTheWhale

ROW_SIZE = 32
COL_SIZE = 64

config = hub75.Hub75SpiConfiguration()
matrix = matrixdata.MatrixData(ROW_SIZE, COL_SIZE)
hub75spi = hub75.Hub75Spi(matrix, config)

# Show Python Logo
matrix.set_pixels(0, 16, logo)
    
for i in range(100):
    hub75spi.display_data()

# Squirty the whale
squirty = SquirtyTheWhale(matrix, hub75spi)
squirty.run_loop()
