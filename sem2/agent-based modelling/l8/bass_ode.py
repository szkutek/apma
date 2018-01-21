import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def model(F, t):
    dF_dt = (1 - F) * (p + q * F)
    return dF_dt


P = [0.01, 0.02, 0.03, 0.1]
q = 0.4
plt.figure()

for p in P:
    # initial condition
    F0 = 0

    # time points
    t = np.linspace(0, 20)

    # solve ODE
    F = odeint(model, F0, t)

    # plot results
    plt.plot(t, F, label='p = ' + str(p))
    plt.xlabel('time')
    plt.ylabel('F(t)')
    plt.legend()

Q = [0.3, 0.4, 0.5]
plt.figure()
p = 0.03

for q in Q:
    # initial condition
    F0 = 0

    # time points
    t = np.linspace(0, 20)

    # solve ODE
    F = odeint(model, F0, t)

    # plot results
    plt.plot(t, F, label='q = ' + str(q))
    plt.xlabel('time')
    plt.ylabel('F(t)')
    plt.legend()

plt.show()
