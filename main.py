import hub75
from logo import logo
from planets import earth, saturn
import bouncer

config = hub75.Hub75SpiConfiguration()
matrix = hub75.Hub75Spi(config)

# Show Python Logo
matrix.SetPixels(0, 16, logo)
    
for i in range(100):
    matrix.DisplayData()

# Show bouncing objects
earth_bounce = bouncer.Bouncer(0, 0, len(earth), len(earth[0]), 63, 31, dx=2)
saturn_bounce = bouncer.Bouncer(20, 10, len(saturn), len(saturn[0]), 63, 31, dx=-2)

while True:
    
    earth_bounce.Update()
    saturn_bounce.Update()
    
    matrix.ClearDirtyBytes()
    matrix.SetPixels(earth_bounce.y, earth_bounce.x, earth)
    matrix.SetPixels(saturn_bounce.y, saturn_bounce.x, saturn)
    matrix.DisplayData()

