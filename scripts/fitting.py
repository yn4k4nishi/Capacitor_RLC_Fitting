import skrf as rf
import matplotlib.pyplot as plt

if __name__ == '__main__':
    simsurfing = rf.Network('data/GJM1555C1HR50BB01_DC0V_25degC_series.s2p')
    simsurfing.frequency.unit = 'ghz'

    freq = simsurfing.frequency

    # modeling 
    line = rf.media.DefinedGammaZ0(frequency=freq, z0=50)
    res = line.resistor(1e4, name='R')
    cap = line.capacitor(1e-12, name='C')
    ind = line.inductor(1e-9, name='L')

    port1 = rf.Circuit.Port(freq, name='port1', z0=50)
    port2 = rf.Circuit.Port(freq, name='port2', z0=50)

    connections = [
        [(port1, 0), (res, 0), (cap, 0), (ind, 0)],
        [(port2, 0), (res, 1), (cap, 1), (ind, 1)]
    ]

    cir = rf.Circuit(connections)
    ntw = cir.network
    ntw.name = 'lumped circuit'

    simsurfing.plot_s_db(n=0, m=0, c='r' ,linestyle='dashed')
    simsurfing.plot_s_db(n=0, m=1, c='b' ,linestyle='dashed')
    ntw.plot_s_db(n=0, m=0, c='r')
    ntw.plot_s_db(n=0, m=1, c='b')

    # plt.xlim(1e9, 10e9)
    plt.ylim(-30, 0)
    plt.savefig('a.png')
