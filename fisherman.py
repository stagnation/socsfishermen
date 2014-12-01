class Fisherman:
    def __init__(self, x,xmax , y, ymax, harvest_proportion,threshold):
        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
        self.harvest_proportion = harvest_proportion
        self.catch = 0
        self.maximum_yield = 1
        self.preseption_of_fishpopulation = []   #Sorted list according to precived population size
        self.threshold = threshold

    def move(self, x, y):
        self.x = x
        self.y = y

    def gain_knowledge(self,x,y,local_fish_population):
        #Remove old knowledge
        for item in self.preseption_of_fishpopulation:
            if (item[0]==x) & (item[1]==y):
                self.preseption_of_fishpopulation.remove(item)
                break
        for i in range(len(self.preseption_of_fishpopulation)):
            if self.preseption_of_fishpopulation[i][2] < local_fish_population :
                self.preseption_of_fishpopulation.insert(i,(x,y,local_fish_population))
                return
        self.preseption_of_fishpopulation.append((x,y,local_fish_population))

    def throw_net(self,local_fish_population):
        caught = local_fish_population *self.harvest_proportion
        caught = min(caught,self.maximum_yield)
        self.catch +=caught;

        if caught < self.threshold:  #If fisherman is unhappy he riskes to change fish location to best "known" or a random
            if len(self.preseption_of_fishpopulation) > 0:
                moveto = self.preseption_of_fishpopulation.pop(0)   #If he thinks the current location is best he will remain, is this correct???
                self.move(moveto[0],moveto[1])
            else:
                self.move(rnd.choice(range(xmax)),rnd.choice(range(ymax)))

        return caught

    def print(self):
        print('position x: ' + str(self.x) + ' position y: ' + str(self.y) + ' catch: ' + str(self.catch) + ' harvest rate: ' + str(self.harvest_proportion))