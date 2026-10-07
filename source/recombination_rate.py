import pfac.crm
import pfac.fac


class RecombinationRate:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.rates", mode="w") as fout:
            for i in range(len(temperatures)):
                recombination_rate              = pfac.crm.Recomb(atomic_number, electron_number-1, temperatures[i], 1)
                radiative_recombination_rate    = 1e-10*recombination_rate[1]
                dielectronic_recombination_rate = 1e-10*recombination_rate[2]
                fout.write(f" {i:02d}     {temperatures[i]:11.5e}     {radiative_recombination_rate:11.5e}   {dielectronic_recombination_rate:11.5e}\n")