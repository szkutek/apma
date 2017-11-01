"""
Agnieszka Szkutek, 208619
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pylab as p

b = 3  # birth rate (of uninfected ppl)
B = 3  # infection spread
k = 3  # rate of death


# solve the system dy/dt = f(y, t)
def f(y, t=0):
    Si = y[0]  # susceptible
    Ii = y[1]  # infected
    # the equations
    f0 = b * Si - B * Ii * Si
    f1 = B * Ii * Si - k * Ii
    return [f0, f1]


def plot_change_in_population(t, S0, S, I0, I):
    plt.figure()
    plt.plot(t, S, label='Susceptible')
    plt.plot(t, I, label='Infected')
    plt.xlabel('time')
    plt.ylabel('population')
    plt.title('Plague model for S(0)=' + str(S0) + ' and I(0)=' + str(I0))
    plt.legend(loc='best')
    plt.show()


def phase_portrait(a, b, c, d):
    # Plotting direction fields and trajectories in the phase plane

    y1 = np.linspace(a, b, 20)
    y2 = np.linspace(c, d, 20)
    Y1, Y2 = np.meshgrid(y1, y2)
    t = 0
    u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)
    NI, NJ = Y1.shape
    for i in range(NI):
        for j in range(NJ):
            x = Y1[i, j]
            y = Y2[i, j]
            yprime = f([x, y], t)
            u[i, j] = yprime[0]
            v[i, j] = yprime[1]
    plt.quiver(Y1, Y2, u, v, color='r')
    plt.xlabel('')
    plt.ylabel('')
    plt.show()


if __name__ == "__main__":
    for I0 in [0.1, 0.5, 1.3]:
        # initial conditions
        S0 = 1.  # initial population
        # I0 = 0.1  # 0.1, 0.5, 1.3
        y0 = [S0, I0]  # initial condition vector
        t = np.linspace(0, 5., 1000)  # time grid

        # solve the DEs
        soln = odeint(f, y0, t)
        S = soln[:, 0]
        I = soln[:, 1]

        plot_change_in_population(t, S0, S, I0, I)

    phase_portrait(-10, 10, -10, 10)
