import pfac.crm
import pfac.fac


class RecombinationRate:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures):
        with open("../database02/{0:s}/{0:s}{1:02d}.rates".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(temperatures)):
                recombination_rate              = pfac.crm.Recomb(atomic_number, electron_number-1, temperatures[i], 1)
                radiative_recombination_rate    = 1e-10*recombination_rate[1]
                dielectronic_recombination_rate = 1e-10*recombination_rate[2]
                fout.write(" {0:02d}     {1:11.5e}     {2:11.5e}   {3:11.5e}\n".format(i, temperatures[i], radiative_recombination_rate, dielectronic_recombination_rate))