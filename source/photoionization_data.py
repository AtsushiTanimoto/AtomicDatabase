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
    

    def generate(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol        = pfac.fac.ATOMICSYMBOL[atomic_number]
        photoionization_data = []
        exist_level_index    = set()

        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_pop/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.pop", mode="r") as fin:
                    for line in fin.readlines():
                        data = line.split()
                        exist_level_index.update({int(data[0])})

        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.rr", mode="r") as fin:
            for line in fin.readlines():
                data   = line.split()

                if len(data)==4:
                    if data[1]!="Z" and self.bound_level_index in exist_level_index:
                        energy = numpy.append(energy, 1e+00*float(data[0])+self.ionization_potential)
                        cross  = numpy.append(cross , 1e-20*float(data[2]))

                        if len(energy)==7:
                            energy     = energy[1:]
                            cross      = cross[1:]
                            p0         = [cross[0], energy[-1]]
                            parameter  = scipy.optimize.curve_fit(f=self.residual, xdata=energy, ydata=cross, p0=p0)[0]
                            self.sigma = parameter[0]
                            self.gamma = -3.0
                            self.tau   = parameter[1]
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


    def residual(self, x, sigma, tau):
        return sigma*numpy.power(x/self.ionization_potential, -3)*numpy.exp(-x/tau)


    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol        = pfac.fac.ATOMICSYMBOL[atomic_number]
        photoionization_data = self.generate(atomic_number, electron_number, temperatures, densities)
        
        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.pi", mode="w") as fout:
            for i in range(len(photoionization_data)):
                fout.write(f"{photoionization_data[i]['bound_level_index']:6d} {photoionization_data[i]['bound_level_twoj']:3d}   {photoionization_data[i]['ionized_level_index']:6d} {photoionization_data[i]['ionized_level_twoj']:3d}  {photoionization_data[i]['l']:6d}      {photoionization_data[i]['ionization_potential']:11.5e}   {photoionization_data[i]['sigma']:10.4e}  {photoionization_data[i]['gamma']:10.4e}   {photoionization_data[i]['tau']:10.4e}\n")           