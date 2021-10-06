import numpy
import pfac.fac
import scipy.optimize


class PhotoionizationData:
    def __init__(self):
        self.bound_level_index    = -1
        self.bound_level_twoj     = 0
        self.ionized_level_index  = -1
        self.ionized_level_twoj   = 0
        self.l                    = 0
        self.ionization_potential = 0.0      
        self.sigma                = 0.0
        self.gamma                = 0.0
        self.tau                  = 0.0
    

    def func(self, x, sigma, gamma, tau):
        return sigma*((x/self.ionization_potential)**gamma)*numpy.exp(-x/tau)


    def write(self, atomic_number, electron_number):
        with open("../database01/{0:s}/{0:s}{1:02d}a.rr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            with open("../database02/{0:s}/{0:s}{1:02d}.pi".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for line in fin.readlines():
                    data   =  line.split()
                    cross  = []
                    energy = []

                    if len(data)==4:
                        energy += [      float(data[0])]
                        cross  += [1e-20*float(data[2])]

                        if len(energy)==6:
                            parameter  = scipy.optimize.curve_fit(func, energy, cross)[0]
                            self.sigma = parameter[0]
                            self.gamma = parameter[1]
                            self.tau   = parameter[2]

                    
                    elif len(data)==6:
                        self.bound_level_index    =   int(data[0])
                        self.bound_level_twoj     =   int(data[1])
                        self.ionized_level_index  =   int(data[2])
                        self.ionized_level_twoj   =   int(data[3])
                        self.l                    = float(data[5])
                        self.ionization_potential = float(data[4])