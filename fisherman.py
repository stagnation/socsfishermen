class Fisherman:
    def __init__(self, x, xmax , y, ymax, harvest_proportion=0.3, threshold=0):
        #not sensible default values at the moment
        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
        self.harvest_proportion = harvest_proportion
        self.catch = 0
        self.maximum_yield = 1
        self.perception_of_fishpopulation = []   #Sorted list according to precived population size
        #can be easier to just append to list and grab the max with max methods,
        #that way order can be disregarded. complexity should not be an issue
        #list of tuples (x, y, size) of fish
        #better to have these set by some thing else than let the fishmeran himself walk around
        #this leads to very interconntected classes.
        self.threshold = threshold

    def move(self, x, y):
        self.x = x
        self.y = y

    def gain_knowledge(self, x, y, site_fish_population):
        #Remove old knowledge
        for item in self.perception_of_fishpopulation:
            if (item[0]==x) & (item[1]==y):
                self.perception_of_fishpopulation.remove(item)
                break
        for i in range(len(self.perception_of_fishpopulation)):
            if self.perception_of_fishpopulation[i][2] < site_fish_population :
                self.perception_of_fishpopulation.insert(i, (x, y, site_fish_population))
                return
        self.perception_of_fishpopulation.append((x, y, site_fish_population))

    def throw_net(self, site_fish_population):
        caught = site_fish_population *self.harvest_proportion
        caught = min(caught, self.maximum_yield)
        self.catch +=caught;
        if caught < self.threshold:  #If fisherman is unhappy he riskes to change fish location to best "known" or a random
            self.move_to_best()
        return caught

    def move_to_best(self):
        if len(self.perception_of_fishpopulation) > 0:
            moveto = self.perception_of_fishpopulation.pop(0)   #If he thinks the current location is best he will remain, is this correct???
            self.move(moveto[0], moveto[1])
        else:
            self.move(rnd.choice(range(xmax)), rnd.choice(range(ymax)))


    def __str__(self):
        return('position x: ' + str(self.x) + ' position y: ' + str(self.y) + ' catch: ' + str(self.catch) + ' harvest rate: ' + str(self.harvest_proportion))
