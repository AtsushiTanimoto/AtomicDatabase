import pfac.fac


class TemperatureDensityGrid:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures, densities):
        with open("../database02/{0:s}/{0:s}{1:02d}.grid".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            fout.write("# {0:02d} {1:02d}\n".format(len(temperatures), len(densities)))
            
            for i in range(len(temperatures)):
                fout.write(" kT   {0:02d}     {1:11.5e}\n".format(i, temperatures[i]))
            
            for i in range(len(densities)):
                fout.write(" ne   {0:02d}     {1:11.5e}\n".format(i, densities[i]))
