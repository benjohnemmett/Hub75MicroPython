import hub75
import matrixdata
from logo import logo
from whale import whale, water_spout_anim
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

# Squirty the whale
whale_bounce = bouncer.Bouncer(30, 10, len(whale[0]), len(whale), 63, 31, dx=2)

frames_until_update = 0
animation_frame = 0

while True:
    
    if frames_until_update == 10:
        whale_bounce.update()
        frames_until_update = 0
        animation_frame = (animation_frame + 1) % 4
    
    matrix.clear_dirty_bytes()
    matrix.set_pixels(whale_bounce.y, whale_bounce.x, whale)
    matrix.set_pixels(whale_bounce.y-1, whale_bounce.x+3, water_spout_anim[animation_frame])
    hub75spi.display_data()
    
    frames_until_update += 1
