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
    

    def function(self, x, sigma, gamma, tau):
        return sigma*((x/self.ionization_potential)**gamma)*numpy.exp(-x/tau)


    def write(self, atomic_number, electron_number):
        with open("../database01/{0:s}/{0:s}{1:02d}a.rr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            with open("../database02/{0:s}/{0:s}{1:02d}.pi".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for line in fin.readlines():
                    data   = line.split()

                    if len(data)==4 and data[0]!="Fe":
                        energy = numpy.append(energy, float(data[0])+self.ionization_potential)
                        cross  = numpy.append(cross , 1e-20*float(data[2]))

                        if len(energy)==7:
                            energy     = energy[1:]
                            cross      = cross[1:]
                            parameter  = scipy.optimize.curve_fit(self.function, energy, cross, p0=[1e-20, -2e+00, 1e+00], maxfev=1000000)[0]
                            self.sigma = parameter[0]
                            self.gamma = parameter[1]
                            self.tau   = parameter[2]
 
                    elif len(data)==6:
                        energy                    = numpy.array([])
                        cross                     = numpy.array([])
                        self.bound_level_index    =   int(data[0])
                        self.bound_level_twoj     =   int(data[1])
                        self.ionized_level_index  =   int(data[2])
                        self.ionized_level_twoj   =   int(data[3])
                        self.l                    = float(data[5])
                        self.ionization_potential = float(data[4])