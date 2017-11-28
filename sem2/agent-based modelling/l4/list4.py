import timeit

from schelling import *


def ex2():
    for i in range(5):
        starting_grid, final_grid, cycles, agents_coord = schelling(100, 500, 250, jb=.5, mb=11, jr=.5, mr=11)
        save_schelling_plot(starting_grid, 'Schelling - starting positions of agents', 'ex1-' + str(i) + '-begin')
        save_schelling_plot(final_grid, 'Schelling - final positions of agents', 'ex1-' + str(i) + '-end')


def ex3():
    population_size = np.arange(250, 4050, 50)
    number_of_iterations = np.zeros(len(population_size))
    execution_times = np.zeros(len(population_size))

    for i, Nb in enumerate(population_size):
        N = 2 * Nb
        start = timeit.default_timer()
        number_of_iterations[i] = schellings_number_of_iterations(100, N, Nb, jb=.5, mb=1, jr=.5, mr=1)
        execution_times[i] = timeit.default_timer() - start

    plt.scatter(population_size, number_of_iterations)
    plt.title('Number of iterations as a function of population size')
    plt.ylabel('number of iterations')
    plt.xlabel('population size')
    plt.savefig('ex3-number-of-iterations.png')
    plt.clf()

    plt.scatter(population_size, execution_times)
    plt.title('Execution time as a function of population size')
    plt.ylabel('execution time')
    plt.xlabel('population size')
    plt.savefig('ex3-execution-times.png')
    plt.close()


def ex4():
    Jt = np.arange(.1, .8, .1)
    segregation_index = np.zeros(len(Jt))
    for i, jt in enumerate(Jt):
        print('ex4: ' + str(jt))
        start = timeit.default_timer()
        segregation_index[i] = schellings_segregation_index(100, 500, 250, jb=jt, mb=1, jr=jt, mr=1)
        print(timeit.default_timer() - start)

    plt.scatter(Jt, segregation_index)
    plt.title('Segregation index as a function of j_t')
    plt.ylabel('segregation index')
    plt.xlabel('j_t')
    plt.savefig('ex4-segregation-index-jt.png')
    plt.close()


def ex5():
    Mt = np.arange(1, 12)  # corresponding to 8,24,48,80 and 120 neighbours
    segregation_index = np.zeros(len(Mt))
    for i, mt in enumerate(Mt):
        print('ex5: ' + str(mt))
        start = timeit.default_timer()
        segregation_index[i] = schellings_segregation_index(100, 500, 250, jb=.5, mb=mt, jr=.5, mr=mt)
        print(timeit.default_timer() - start)

    plt.scatter(Mt, segregation_index)
    plt.title('Segregation index as a function of m_t')
    plt.ylabel('segregation index')
    plt.xlabel('m_t')
    plt.savefig('ex5-segregation-index-mt.png')
    plt.close()


def ex6():
    for i in range(5):
        starting_grid, final_grid, cycles, agents_coord = schelling(100, 2000, 1000, jb=3 / 8, mb=1, jr=6 / 8, mr=1)
        save_schelling_plot(starting_grid, 'Schelling - starting positions of agents', 'ex6-' + str(i) + '-begin')
        save_schelling_plot(final_grid, 'Schelling - final positions of agents', 'ex6-' + str(i) + '-end')


if __name__ == '__main__':
    # ex2()
    # ex3()
    ex4()
    print('-------------')
    ex5()
