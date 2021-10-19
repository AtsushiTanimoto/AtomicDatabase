import numpy
import pfac.fac
import scipy.optimize


class PhotoionizationData:
    def __init__(self):
        self.exist_level_index    = set()
        self.bound_level_index    = -1
        self.bound_level_twoj     = 0
        self.ionized_level_index  = -1
        self.ionized_level_twoj   = 0
        self.l                    = 0
        self.ionization_potential = 0.0      
        self.sigma                = 0.0
        self.gamma                = 0.0
        self.tau                  = 0.0
    

    def residual(self, param, x, y):
        return y - param[0]*((x/self.ionization_potential)**param[1])*numpy.exp(-x/param[2])

 
    def write(self, atomic_number, electron_number, temperatures, densities):
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open("../database02/{0:s}/{0:s}{1:02d}_pop/{0:s}{1:02d}_t{2:02d}d{3:02d}i02.pop".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    for line in fin.readlines():
                        data = line.split()
                        self.exist_level_index.update({int(data[0])})

        with open("../database01/{0:s}/{0:s}{1:02d}a.rr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            with open("../database02/{0:s}/{0:s}{1:02d}.pi".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for line in fin.readlines():
                    data   = line.split()

                    if len(data)==4:
                        if data[1]!="Z" and self.bound_level_index in self.exist_level_index:
                            energy = numpy.append(energy, 1e+00*float(data[0])+self.ionization_potential)
                            cross  = numpy.append(cross , 1e-20*float(data[2]))

                            if len(energy)==7:
                                energy     = energy[1:]
                                cross      = cross[1:]
                                param      = [1e-20, -2e+00, 1e+05]
                                parameter  = scipy.optimize.leastsq(func=self.residual, x0=param, maxfev=1000000, args=(energy,cross))[0]
                                self.sigma = parameter[0]
                                self.gamma = parameter[1]
                                self.tau   = parameter[2]
                                fout.write("{0:6d} {1:3d}   {2:6d} {3:3d}  {4:6d}      {5:11.5e}   {6:10.4e}  {7:10.4e}   {8:10.4e}\n".format(self.bound_level_index, self.bound_level_twoj, self.ionized_level_index, self.ionized_level_twoj, self.l, self.ionization_potential, self.sigma, self.gamma, self.tau))
 
                    elif len(data)==6:
                        energy                    = numpy.array([])
                        cross                     = numpy.array([])
                        self.bound_level_index    =   int(data[0])
                        self.bound_level_twoj     =   int(data[1])
                        self.ionized_level_index  =   int(data[2])
                        self.ionized_level_twoj   =   int(data[3])
                        self.l                    =   int(data[5])
                        self.ionization_potential = float(data[4])