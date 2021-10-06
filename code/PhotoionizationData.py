import pfac.fac


class PhotoionizationData:
    def __init__(self):
        self.bound_level_index    = -1
        self.bound_level_twoj     = 0
        self.ionized_level_index  = -1
        self.ionized_level_twoj   = 0
        self.ionization_potential = 0.0
        self.l                    = 0
        self.sigma                = 0.0
        self.gamma                = 0.0
        self.tau                  = 0.0
    

    def write(self, atomic_number, electron_number):
        with open("../database01/{0:s}/{0:s}{1:02d}a.rr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            with open("../database02/{0:s}/{0:s}{1:02d}.pi".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for line in fin.readlines():
                    data = line.split()
                    if len(data)==3:
                        if data[0]=="NEGRID":
                            pass
                    
                    elif len(data)==6:
                        self.bound_level_index    =   int(data[0])
                        self.bound_level_twoj     =   int(data[1])
                        self.ionized_level_index  =   int(data[2])
                        self.ionized_level_twoj   =   int(data[3])
                        self.ionization_potential = float(data[4])
                        self.l                    = float(data[5])