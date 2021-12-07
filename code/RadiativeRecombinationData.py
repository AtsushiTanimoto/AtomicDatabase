import numpy
import pfac.fac
import scipy.optimize


class RadiativeRecombinationData:
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
    

    def generate(self, atomic_number, electron_number, temperatures, densities):
        photoionization_data = []
        
        with open("../database01/{0:s}/{0:s}{1:02d}a.rr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data   = line.split()

                if len(data)==4:
                    if data[1]!="Z" and self.bound_level_index<=84:
                        energy = numpy.append(energy, 1e+00*float(data[0])+self.ionization_potential)
                        cross  = numpy.append(cross , 1e-20*float(data[2]))

                        if len(energy)==7:
                            energy     = energy[1:]
                            cross      = cross[1:]
                            p0         = [cross[0], -2e+00, energy[-1]]
                            parameter  = scipy.optimize.curve_fit(f=self.residual, xdata=energy, ydata=cross, p0=p0)[0]
                            self.sigma = parameter[0]
                            self.gamma = parameter[1]
                            self.tau   = parameter[2]
                            photoionization_data.append({"bound_level_index":self.bound_level_index, "bound_level_twoj":self.bound_level_twoj, "ionized_level_index":self.ionized_level_index, "ionized_level_twoj":self.ionized_level_twoj, "l":self.l, "ionization_potential":self.ionization_potential, "sigma":self.sigma, "gamma":self.gamma, "tau":self.tau})

                elif len(data)==6:
                    energy                    = numpy.array([])
                    cross                     = numpy.array([])
                    self.bound_level_index    =   int(data[0])
                    self.bound_level_twoj     =   int(data[1])
                    self.ionized_level_index  =   int(data[2])
                    self.ionized_level_twoj   =   int(data[3])
                    self.l                    =   int(data[5])
                    self.ionization_potential = float(data[4])
        
        return photoionization_data


    def residual(self, x, sigma, gamma, tau):
        return sigma*numpy.power(x/self.ionization_potential,gamma)*numpy.exp(-x/tau)


    def write(self, atomic_number, electron_number, temperatures, densities):
        photoionization_data = self.generate(atomic_number, electron_number, temperatures, densities)
        
        with open("../database02/{0:s}/{0:s}{1:02d}.pi".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(photoionization_data)):
                fout.write("{0:6d} {1:3d}   {2:6d} {3:3d}  {4:6d}      {5:11.5e}   {6:10.4e}  {7:10.4e}   {8:10.4e}\n".format(photoionization_data[i]["bound_level_index"], photoionization_data[i]["bound_level_twoj"], photoionization_data[i]["ionized_level_index"], photoionization_data[i]["ionized_level_twoj"], photoionization_data[i]["l"], photoionization_data[i]["ionization_potential"], photoionization_data[i]["sigma"], photoionization_data[i]["gamma"], photoionization_data[i]["tau"]))           