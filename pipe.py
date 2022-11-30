import random

hole_size = 100
speed = 1


class Pipe:
    def __init__(self, width, height):
        self.counted = False

        self.x = width

        self.hole_pos = random.randint(60, height - 60)
        self.hole = [height - (self.hole_pos + (hole_size / 2)), self.hole_pos - (hole_size / 2)]

    def update(self):
        self.x -= speed

        if self.x < -50:
            return False

        return True

    def collide(self, y, width, height):
        same_x = (self.x < (width / 3) + 30 and self.x + 50 > (width / 3))  # Check if on the same x as the bird
        in_hole = (self.hole_pos + (hole_size / 2) > y + 20 and y > self.hole_pos - (hole_size / 2))

        return same_x and not in_hole

    def same_x(self, width):
        if self.x < (width / 3) and not self.counted:
            self.counted = True
            return True
        else:
            return False
