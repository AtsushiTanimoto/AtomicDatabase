import pfac.fac


class TemperatureDensityGrid:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures, densities):
        with open("../database02/{0:s}/{0:s}{1:02d}.grid".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
