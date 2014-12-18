import scipy as sp

class FishermanVaryHarvest:
    def __init__(self, x , y, price_perception, harvest_fraction=0.3, threshold=0, greed=0):
        #not sensible default values at the moment
        self.x = x
        self.y = y
        self.harvest_fraction = harvest_fraction
        self.harvest_count = 2
        self.greed = greed          #Makes use of this in a new sence
        self.catch = (0,0)          #(spice,amount)
        self.wealth = 0
        self.wealthpre1 = 0
        self.wealthpre2 = 0
        self.maximum_yield = 1 #we don't use this yet
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
    def percived_value(self,catch):
        return catch[1]*self.price_perception[catch[0]]
        #return catch[1]
    def moneyDiff(self,update = False):
        money_diff = (self.wealth-self.wealthpre1) - (self.wealthpre1-self.wealthpre2)
        if update:
            self.updateMoneyDiff()
        return money_diff
    def updateMoneyDiff(self):
        self.wealthpre2 = self.wealthpre1
        self.wealthpre1 = self.wealth

    def gotMoreMoney(self,update=False):
        got_more_money = (self.wealth - self.wealthpre1 >= self.wealthpre1-self.wealthpre2)
        if update:
            self.updateMoneyDiff()
        return got_more_money
    def throw_net(self, site_fish_population):
        #Greedy always want to fish at the best location!
        #bestFishingSite = self.move_to_best()

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
        if self.harvest_count==0:           #Don't change two times in row
            self.harvest_count = 2
            if self.gotMoreMoney():
                self.harvest_fraction *= 1+1e-1
            else:                                                                       #Hmm, got less maybe stuff are dying, reduce
                self.harvest_fraction *= 1-1e-1
        else:
                self.harvest_count -= 1
        self.updateMoneyDiff()
        if sp.rand()<self.greed:                                                    #Sometimes i like to increase my harvest rate for no reason
            self.harvest_fraction *= 1+5e-2
        #if sp.rand()<0.13:                                                     #Sometimes i like to decrease my harvest rate for no reason
        #    self.harvest_fraction *= 1-1e-2

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
