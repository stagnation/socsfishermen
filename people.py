class People:

    def __init__(self, x, y, threshhold):
        self.x = x
        self.y = y
        self.taget_x = 0
        self.target_y = 0
        self.threshhold = threshhold
        self.catch = 0

    def move(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "person with %s catch at %s, %s" %(self.catch, self.x, self.y)


