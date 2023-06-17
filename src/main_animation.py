import hub75
import matrixdata
from animation import AnimationPlayer
from flame_32_data import flame
from logo import logo

ROW_SIZE = 32
COL_SIZE = 64

config = hub75.Hub75SpiConfiguration()
matrix = matrixdata.MatrixData(ROW_SIZE, COL_SIZE)
hub75spi = hub75.Hub75Spi(matrix, config)

# Show Python Logo
matrix.set_pixels(0, 20, logo)
for i in range(100):
    hub75spi.display_data()

flame_player = AnimationPlayer(matrix, hub75spi, flame, 0, 26)
flame_player.run_loop()



