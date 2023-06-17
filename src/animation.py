
class AnimationPlayer():

    def __init__(self, matrix, hub75, frames, row, col):
        self.matrix = matrix
        self.hub75 = hub75

        self.frames_until_update = 0
        self.frame_index = 0
        self.frames = frames
        self.row = row
        self.col = col

    def update(self, row, col):
        if self.frames_until_update == 10:
            self.frames_until_update = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.matrix.clear_dirty_bytes()
            self.matrix.set_pixels(row, col, self.frames[self.frame_index])
        
        self.frames_until_update += 1

    def run_loop(self):
        while True:
            self.update(self.row, self.col)
            self.hub75.display_data()