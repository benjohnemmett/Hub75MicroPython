
class Bouncer():

    def __init__(self, x, y, height, width, max_x, max_y, dx=1, dy=1):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.dx = dx
        self.dy = dy

        self.max_x = max_x
        self.max_y = max_y

    def Update(self):
        self.x += self.dx
        self.y += self.dy

        if (self.y > (self.max_y - self.height)):
            self.dy *= -1
            self.y = self.max_y
        elif (self.y < 0):
            self.dy *= -1
            self.y = 0

        if (self.x > (self.max_x - self.width)):
            self.dx *= -1
            self.x = self.max_x
        elif (self.x < 0):
            self.dx *= -1
            self.x = 0
