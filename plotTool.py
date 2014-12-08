import scipy as sp
import matplotlib.pyplot as plt
extinction_limit =1e-5

def is_extinct(fish_population):
    days = fish_population.shape[0]
    for day in range(days):
        if fish_population[day]<extinction_limit:
            return day+1
    return days

def plot_fishpop(fish_populations):
    if len(fish_populations.shape) == 2:
        days = fish_populations.shape[1]
        avg_fishpop = sp.mean(fish_populations, axis=0)
        std_fishpop = sp.power(sp.std(fish_populations, axis = 0),2)
        low_fishpop = sp.subtract(avg_fishpop,std_fishpop)
        high_fishpop = sp.add(avg_fishpop,std_fishpop)
        plt.figure()
        t = sp.arange(0, days)

        plt.fill_between(t,high_fishpop,avg_fishpop, alpha = 0.3)
        plt.fill_between(t,low_fishpop,avg_fishpop, alpha = 0.3)

        plt.plot(t, avg_fishpop,'k', label = 'Average population')
    elif len(fish_populations.shape) == 3:
        n_speices = fish_populations.shape[0]
        n_pops = fish_populations.shape[1]
        days = fish_populations.shape[2]

        plt.figure()
        for i in range(n_speices):
            for pop in range(n_pops):
                if fish_populations[i][pop][days-1] < extinction_limit:
                    plt.scatter(is_extinct(fish_populations[i][pop]),0)


            avg_fishpop = sp.mean(fish_populations[i], axis=0)
            std_fishpop = sp.power(sp.std(fish_populations[i], axis = 0),2)
            low_fishpop = sp.subtract(avg_fishpop,std_fishpop)
            high_fishpop = sp.add(avg_fishpop,std_fishpop)
            t = sp.arange(0, days)

            plt.fill_between(t,high_fishpop,avg_fishpop, alpha = 0.3)
            plt.fill_between(t,low_fishpop,avg_fishpop, alpha = 0.3)
            plt.plot(t, avg_fishpop, label = 'Specie ' + str(i+1))
    plt.xlabel('Time')
    plt.ylabel('Fish population size')
    plt.legend()

