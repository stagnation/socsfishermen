import scipy as sp

class Fisherman:
    def __init__(self, x , y, price_perception, harvest_fraction, threshold, greed, level):
        self.level = level
        self.x = x
        self.y = y
        self.harvest_fraction = harvest_fraction
        self.greed = greed
        self.catch = (0,0)          #(spice,amount)
        self.wealth = 0
        self.price_perception = price_perception
        self.threshold = threshold
        self.perception_of_fishpopulation_value = [((x,y),0,0)]
        self.current_fishing_tactic = ((x,y),0,0)
        #List of the estimation made by the fisherman of which location and fish spice would  yeild a certain results

    def move(self, pos_tup):
        self.x = pos_tup[0]
        self.y = pos_tup[1]

    def gain_knowledge(self, pos_tup, site_fish_population, specie):
        #Remove old knowledge
        precived_value = site_fish_population * self.price_perception[specie]
        for item in self.perception_of_fishpopulation_value:
            if (item[0]==pos_tup) & (item[1]==specie) :
                self.perception_of_fishpopulation_value.remove(item)
                break
            #Add new knowledge
        self.perception_of_fishpopulation_value.append((pos_tup, specie, precived_value))

    def throw_net(self, site_fish_population):
        specie = self.current_fishing_tactic[1]



        #only fish from one fish species
        caught = 0
        nets = 0
        max_throws = 1 #Placeholder #only once not sure if we want greed.
        for nets in range( max_throws ):
            caught += site_fish_population[specie] * self.harvest_fraction
            if caught > self.greed:
                break

        #caught = min(caught, 0.15)           #Removes the minimum for simpler model
        self.catch = (specie, caught)

        #handle more than one species
        vec_caught = sp.zeros_like(site_fish_population)
        vec_caught[specie] = caught

        return vec_caught

    def move_to_best(self):
        if len(self.perception_of_fishpopulation_value) > 0:
            bestFishingSite = max(self.perception_of_fishpopulation_value, key=lambda item:item[2])
            #If he thinks the current location is best he will remain, is this correct???
            self.move(bestFishingSite[0])
            self.current_fishing_tactic = bestFishingSite
            return bestFishingSite





    def __str__(self):
        return('position x: ' + str(self.x) + ' position y: ' + str(self.y) + ' catch: ' + str(self.catch) + ' harvest rate: ' + str(self.harvest_fraction))
