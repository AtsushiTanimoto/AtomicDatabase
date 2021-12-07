import pandas
import pfac.fac


class PhotoexcitationData:
    def __init__(self):
        self.exist_level_index              = set()
        self.upper_level_index              = []
        self.upper_level_statistical_weight = []
        self.lower_level_index              = []
        self.lower_level_statistical_weight = []
        self.transition_energy              = []
        self.oscillator_strength            = []
        self.radiative_decay_rate           = []
    

    def write(self, atomic_number, electron_number, temperatures, densities):
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open("../database02/{0:s}/{0:s}{1:02d}_pop/{0:s}{1:02d}_t{2:02d}d{3:02d}i02.pop".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    for line in fin.readlines():
                        data = line.split()
                        self.exist_level_index.update({int(data[0])})

        with open("../database01/{0:s}/{0:s}{1:02d}a.tr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data = line.split()

                if len(data)==8:
                    if int(data[2]) in self.exist_level_index and 1e-03<=float(data[5])/(1+int(data[3])):
                        self.upper_level_index              += [int(data[0])]
                        self.upper_level_statistical_weight += [1+int(data[1])]
                        self.lower_level_index              += [int(data[2])]
                        self.lower_level_statistical_weight += [1+int(data[3])]
                        self.transition_energy              += [float(data[4])]
                        self.oscillator_strength            += [float(data[5])/(1+int(data[3]))]
                        self.radiative_decay_rate           += [float(data[6])]
        
        df = pandas.DataFrame({"upper_level_index":self.upper_level_index, "upper_level_statistical_weight":self.upper_level_statistical_weight, "lower_level_index":self.lower_level_index, "lower_level_statistical_weight":self.lower_level_statistical_weight, "transition_energy":self.transition_energy, "oscillator_strength":self.oscillator_strength, "radiative_decay_rate":self.radiative_decay_rate})
        df.sort_values("upper_level_index", inplace=True)
        df.reset_index(drop=True, inplace=True)

        with open("../database02/{0:s}/{0:s}{1:02d}.px".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(df.index)):
                fout.write("{0:6d} {1:4d}   {2:6d} {3:4d}     {4:12.6e}  {5:12.6e}  {6:12.6e}\n".format(df.upper_level_index[i], df.upper_level_statistical_weight[i], df.lower_level_index[i], df.lower_level_statistical_weight[i], df.transition_energy[i], df.oscillator_strength[i], df.radiative_decay_rate[i]))