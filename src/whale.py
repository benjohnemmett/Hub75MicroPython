import bouncer

class SquirtyTheWhale():

    def __init__(self, matrix, hub75):
        self.matrix = matrix
        self.hub75 = hub75
        
        whale_left = [x.copy() for x in whale]
        whale_right = [x.copy() for x in whale]
        [x.reverse() for x in whale_right]
        self.whale_sprites = [whale_left, whale_right]
        
        initial_row = 10
        initial_col = 0
        self.whale_bounce = bouncer.Bouncer(initial_col, 
                                            initial_row, 
                                            len(whale[0]), 
                                            len(whale), 
                                            self.matrix.col_size-1, 
                                            self.matrix.row_size-1, 
                                            dx=2)
        self.frames_until_update = 0
        self.animation_frame = 0

    def update(self):
        if self.frames_until_update == 10:
            self.whale_bounce.update()
            self.frames_until_update = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        self.matrix.clear_dirty_bytes()
        
        whale_row = self.whale_bounce.y
        whale_col = self.whale_bounce.x
        whale_is_going_right = self.whale_bounce.dx > 0
        
        water_row = whale_row - 5
        if whale_is_going_right:
            water_col = whale_col + 6
        else:
            water_col = whale_col
        
        self.matrix.set_pixels(whale_row, whale_col, self.whale_sprites[whale_is_going_right])
        self.matrix.set_pixels(water_row, water_col, water_spout_anim[self.animation_frame])
        
        self.frames_until_update += 1

    def run_loop(self):
        while True:
            self.update()
            self.hub75.display_data()


whale = [
    [1,1,1,1,1,1,0,0,0,1,1],
    [1,7,1,1,1,1,1,1,0,1,1],
    [1,1,1,1,1,1,1,1,1,0,0],
]

water_spout_anim = [
    [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,3,0,0,0],
    ],
    [
    [0,0,0,0,0,0],
    [0,0,0,3,0,0],
    [0,3,3,0,0,0],
    [0,0,3,0,0,0],
    [0,0,3,0,0,0],
    ],
    [
    [0,0,0,0,3,0],
    [0,3,0,3,3,0],
    [3,0,3,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    ],
    [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,3,0,3,0],
    [3,0,0,0,3,0],
    [0,3,0,0,0,3],
    ]
]
