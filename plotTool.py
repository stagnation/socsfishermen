import scipy as sp
import matplotlib.pyplot as plt
from utils import *
extinction_limit =1e-5


def plot_fishpop(fish_populations):
    avgplot = None
    specieplots = []
    if len(fish_populations.shape) == 2:
        #only one species
        days = fish_populations.shape[1]
        avg_fishpop = sp.mean(fish_populations, axis=0)
        std_fishpop = sp.power(sp.std(fish_populations, axis = 0),2)
        low_fishpop = sp.subtract(avg_fishpop,std_fishpop)
        high_fishpop = sp.add(avg_fishpop,std_fishpop)
        plt.figure()
        t = sp.arange(0, days)

        plt.fill_between(t,high_fishpop,avg_fishpop, alpha = 0.3)
        plt.fill_between(t,low_fishpop,avg_fishpop, alpha = 0.3)

        avgplot,  = plt.plot(t, avg_fishpop,'k', label = 'Average population')
    elif len(fish_populations.shape) == 3:
        #more than one species, likely
        n_species = fish_populations.shape[0]
        colvec = [plt.cm.winter(i) for i in sp.linspace(0, 0.9, n_species)]
        n_pops = fish_populations.shape[1]
        days = fish_populations.shape[2]

        plt.figure()
        for i in range(n_species):
            col = colvec[i]

            #avg_fishpop = sp.mean(fish_populations[i], axis=0)
            #std_fishpop = sp.power(sp.std(fish_populations[i], axis = 0),2)
            #low_fishpop = sp.subtract(avg_fishpop,std_fishpop)
            #high_fishpop = sp.add(avg_fishpop,std_fishpop)
            #t = sp.arange(0, days)
            #lab = 'Specie ' + str(i+1)
            #handle,  = plt.plot(t, avg_fishpop, label = lab, c=col)
            #col = handle.get_c()


            #plt.fill_between(t,high_fishpop,avg_fishpop, color=col, alpha = 0.3)
            #plt.fill_between(t,low_fishpop,avg_fishpop, color=col, alpha = 0.3)

            #extinction_mask = sp.ones_like(fish_populations[i])
            for pop in range(n_pops):
                if fish_populations[i][pop][days-1] < extinction_limit:
                    extinction_day = is_extinct(fish_populations[i][pop])
                    plt.scatter(extinction_day, 0, c=col)
            #        extinction_mask[pop][extinction_day:] = False
            #masked_pops = sp.ma.masked_array(data, mask
            masked_pops = sp.ma.masked_equal(fish_populations[i], 0)

            avg_fishpop = sp.mean(masked_pops, axis=0)
            std_fishpop = sp.power(sp.std(masked_pops, axis = 0),2)
            low_fishpop = sp.subtract(avg_fishpop,std_fishpop)
            high_fishpop = sp.add(avg_fishpop,std_fishpop)
            t = sp.arange(0, days)
            lab = 'Specie ' + str(i+1)
            handle,  = plt.plot(t, avg_fishpop, label = lab, c=col)
            col = handle.get_c()


            plt.fill_between(t,high_fishpop,avg_fishpop, color=col, alpha = 0.3)
            plt.fill_between(t,low_fishpop,avg_fishpop, color=col, alpha = 0.3)


            specieplots.append( (handle, lab) )



    plt.xlabel('Time')
    plt.ylabel('Fish population size')
    #handles, labels = zip(*specieplots)
   # if avgplot:
   #     plt.legend(handles=avgplot)
   # else:
   #     plt.legend(handles,labels)

