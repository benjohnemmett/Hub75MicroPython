import hub75
import matrixdata
from logo import logo
from planets import earth, saturn
import bouncer

ROW_SIZE = 32
COL_SIZE = 64

config = hub75.Hub75SpiConfiguration()
matrix = matrixdata.MatrixData(ROW_SIZE, COL_SIZE)
hub75spi = hub75.Hub75Spi(matrix, config)

# Show Python Logo
matrix.set_pixels(0, 16, logo)
    
for i in range(100):
    hub75spi.display_data()

# Show bouncing objects
earth_bounce = bouncer.Bouncer(0, 0, len(earth), len(earth[0]), 63, 31, dx=2)
saturn_bounce = bouncer.Bouncer(20, 10, len(saturn), len(saturn[0]), 63, 31, dx=-2)

while True:
    
    earth_bounce.update()
    saturn_bounce.update()
    
    matrix.clear_dirty_bytes()
    matrix.set_pixels(earth_bounce.y, earth_bounce.x, earth)
    matrix.set_pixels(saturn_bounce.y, saturn_bounce.x, saturn)
    hub75spi.display_data()


