import pfac.fac


class TemperatureDensityGrid:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.grid", mode="w") as fout:
            fout.write(f"# {len(temperatures):02d} {len(densities):02d}\n")
            
            for i in range(len(temperatures)):
                fout.write(f" kT   {i:02d}     {temperatures[i]:11.5e}\n")
            
            for i in range(len(densities)):
                fout.write(f" ne   {i:02d}     {densities[i]:11.5e}\n")
