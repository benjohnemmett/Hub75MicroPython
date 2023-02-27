class Bouncer():
    '''
    Bouncing image object.
    
    Parameters
    ----------
    x : int
        Initial x position (left col) of image.
    y : int
        Initial y position (top row) of image.
    width : int
        Image width.
    height : int
        Image height.
    max_x : int
        Column limit right.
    max_y : int
        Row limit bottom.
    min_x : int
        Column limit left.
    min_y : int
        Row limit top.
    dx : int
        Initial x direction (in cols/cycle).
    dy : int
        Initial y direction (in rows/cycle).
    '''

    def __init__(self, x, y, width, height, max_x, max_y, min_x=0, min_y=0, dx=1, dy=1):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.dx = dx
        self.dy = dy

        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y

    def update(self):
        '''
        Update object positions (x,y) and directions (dx,dy).

        Returns
        -------
        None.
        '''
        self.x += self.dx
        self.y += self.dy

        if (self.y > (self.max_y - self.height)):
            self.dy *= -1
        elif (self.y <= self.min_y) and (self.dy < 0):
            self.dy *= -1

        if (self.x > (self.max_x - self.width)):
            self.dx *= -1
        elif (self.x <= self.min_x) and (self.dx < 0):
            self.dx *= -1
