import timeit

from schelling import *


def ex2(M):
    for i in range(5):
        starting_grid, final_grid, cycles, agents_coord = schelling(M, 500, 250, jb=.5, mb=1, jr=.5, mr=1)
        save_schelling_plot(starting_grid, 'Schelling - starting positions of agents', 'ex1-begin-' + str(i))
        save_schelling_plot(final_grid, 'Schelling - final positions of agents', 'ex1-end-' + str(i))


def ex3(M):
    population_size = np.arange(250, 4050, 50)
    number_of_iterations = np.zeros(len(population_size))
    for i, Nb in enumerate(population_size):
        N = 2 * Nb
        number_of_iterations[i] = schellings_number_of_iterations(M, N, Nb, jb=.5, mb=1, jr=.5, mr=1)

    plt.plot(population_size, number_of_iterations)
    plt.title('Number of iterations as a function of population size')
    plt.savefig('ex3-number-of-iterations.png')
    plt.close()


def ex5(M):
    Jt = np.arange(.1, .9, .1)
    segregation_index = np.zeros(len(Jt))
    for i, jt in enumerate(Jt):
        segregation_index[i] = schellings_segregation_index(M, 500, 250, jb=jt, mb=1, jr=jt, mr=1)

    plt.plot(Jt, segregation_index)
    plt.title('Segregation index as a function of j_t')
    plt.savefig('ex5-segregation-index.png')
    plt.close()


def ex6(M):
    Mt = np.arange(1, 12)
    segregation_index = np.zeros(len(Mt))
    for i, mt in enumerate(Mt):
        segregation_index[i] = schellings_segregation_index(M, 500, 250, jb=.5, mb=mt, jr=.5, mr=mt)

    plt.plot(Mt, segregation_index)
    plt.title('Segregation index as a function of m_t')
    plt.savefig('ex6-segregation-index.png')
    plt.close()


if __name__ == '__main__':
    m = 100
    imp = 'from __main__ import '
    num = 1

    fun = 'ex5'
    print(timeit.timeit(fun + '(' + str(m) + ')', imp + fun, number=num))
