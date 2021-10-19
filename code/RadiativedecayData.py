import pfac.fac


class RadiativedecayData:
    def __init__(self):
        self.upper_level_index              = -1
        self.upper_level_statistical_weight = 0
        self.lower_level_index              = -1
        self.lower_level_statistical_weight = 0
        self.transition_energy              = 0.0
        self.oscillator_strength            = 0.0
        self.radiative_decay_rate           = 0.0
    

    def write(self, atomic_number, electron_number):
        with open("../database01/{0:s}/{0:s}{1:02d}a.tr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            with open("../database02/{0:s}/{0:s}{1:02d}.rd".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for line in fin.readlines():
                    data = line.split()
                    
                    if len(data)==8:
                        if 1e-03<=float(data[5])/(1+int(data[3])):
                            self.upper_level_index              =   int(data[0])
                            self.upper_level_statistical_weight = 1+int(data[1])
                            self.lower_level_index              =   int(data[2])
                            self.lower_level_statistical_weight = 1+int(data[3])
                            self.transition_energy              = float(data[4])
                            self.oscillator_strength            = float(data[5])/(1+int(data[3]))
                            self.radiative_decay_rate           = float(data[6])
                            fout.write("{0:6d} {1:4d}   {2:6d} {3:4d}     {4:12.6e}  {5:12.6e}  {6:12.6e}\n".format(self.upper_level_index, self.upper_level_statistical_weight, self.lower_level_index, self.lower_level_statistical_weight, self.transition_energy, self.oscillator_strength, self.radiative_decay_rate))