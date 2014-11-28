class Fisherman:
    def __init__(self, x, y, harvest_proportion,threshold):   #Threshold determines if fisherman should move... this is for later
        self.x = x
        self.y = y
        self.harvest_proportion = harvest_proportion
        self.catch = 0
        self.maximum_yield = 1

    def move(self, x, y):
        self.x = x
        self.y = y

    def add_to_catch(self,amount):
        catch += amount

    def throw_net(self,local_fish_population):
        caught = local_fish_population *self.harvest_proportion
        caught = min(caught,self.maximum_yield)
        #caught = min(local_fish_population,self.maximum_yield)   #For simple model
        self.catch +=caught;
        return caught

    def print(self):
        print('position x: ' + str(self.x) + ' position y: ' + str(self.y) + ' catch: ' + str(self.catch) + ' harvest rate: ' + str(self.harvest_proportion))