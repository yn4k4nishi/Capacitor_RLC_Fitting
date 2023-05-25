import numpy as np
import skrf as rf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def parallel_RLC(freq, param : np.ndarray):
    p = np.split(param, 3)

    R = p[0]
    L = p[1]
    C = p[2]

    line = rf.media.DefinedGammaZ0(frequency=freq, z0=50)
    res = line.resistor(R, name='R')
    cap = line.capacitor(L, name='C')
    ind = line.inductor(C, name='L')

    port1 = rf.Circuit.Port(freq, name='port1', z0=50)
    port2 = rf.Circuit.Port(freq, name='port2', z0=50)

    connections = [
        [(port1, 0), (res, 0), (cap, 0), (ind, 0)],
        [(port2, 0), (res, 1), (cap, 1), (ind, 1)]
    ]

    cir = rf.Circuit(connections)
    ntw = cir.network
    ntw.name = 'lumped circuit'

    return ntw.s


if __name__ == '__main__':
    simsurfing = rf.Network('data/GJM1555C1HR50BB01_DC0V_25degC_series.s2p')
    simsurfing.frequency.unit = 'ghz'

    freq = simsurfing.frequency

    R = np.full(freq.f.size, 1e4)
    L = np.full(freq.f.size, 1e-12)
    C = np.full(freq.f.size, 1e-9)

    param = np.concatenate([R, L, C], axis=0)
    s = parallel_RLC(freq, param)

    simsurfing.plot_s_db(n=0, m=0, c='r' ,linestyle='dashed')
    simsurfing.plot_s_db(n=0, m=1, c='b' ,linestyle='dashed')

    plt.plot(freq.f, 10*np.log10(s[:,0,0].real), c='r', label='opt, S11')
    plt.plot(freq.f, 10*np.log10(s[:,1,0].real), c='b', label='opt, S21')

    plt.xlim(1e9, 20e9)
    plt.ylim(-30, 0)
    plt.legend()
    plt.savefig('a.png')
