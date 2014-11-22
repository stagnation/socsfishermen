class Fish:
    #groups of fish are bundled
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.count = count
        growth_rate = 1

    def grow(self, capacity):
        growth = ( 1 - self.count / capacity )
        self.count += growth * growth_rate * self.count

    def net(self):
        caught_fish_count = 0.3 * self.count
        self.count -= caught_fish_count
        return caught_fish_count

    def add(self, num):
        print("adding",num,"to",self.count)
        self.count = self.count + num
        print(self.count)

    def __str__(self):
        return "%s fish at %s, %s" %(self.count, self.x, self.y)

    def fish_caught(self):
        #this should probably be some lienar return rate in fish size.
        thresh = 10
        catch = 0.1 * self.count if self.count > thresh else 0
        self.count -= catch
        return catch

