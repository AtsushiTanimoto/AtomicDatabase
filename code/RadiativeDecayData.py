from os import minor
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
    

    def generate(self, atomic_number, electron_number):
        radiative_decay_data         = []
        reduced_radiative_decay_data = []
        maximum_level_index          = 0
        minor_transition             = set()

        with open("../database02/{0:s}/{0:s}{1:02d}.px".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data                = line.split()
                maximum_level_index = max(maximum_level_index, int(data[0]))

        with open("../database01/{0:s}/{0:s}{1:02d}a.tr".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data = line.split()
                    
                if len(data)==8:
                    if int(data[0])<=maximum_level_index:
                        self.upper_level_index              = int(data[0])
                        self.upper_level_statistical_weight = 1+int(data[1])
                        self.lower_level_index              = int(data[2])
                        self.lower_level_statistical_weight = 1+int(data[3])
                        self.transition_energy              = float(data[4])
                        self.oscillator_strength            = float(data[5])/(1+int(data[3]))
                        self.radiative_decay_rate           = float(data[6])
                        radiative_decay_data.append({"upper_level_index": self.upper_level_index, "upper_level_statistical_weight": self.upper_level_statistical_weight, "lower_level_index": self.lower_level_index, "lower_level_statistical_weight": self.lower_level_statistical_weight, "transition_energy": self.transition_energy, "oscillator_strength": self.oscillator_strength, "radiative_decay_rate": self.radiative_decay_rate})
        
        radiative_decay_data = sorted(radiative_decay_data, key=lambda x:x["upper_level_index"])
        
        for i in range(1+maximum_level_index):
            total_rate = 0

            for j in range(len(radiative_decay_data)):
                if radiative_decay_data[j]["upper_level_index"]==i:
                    total_rate+=radiative_decay_data[j]["radiative_decay_rate"]

            for j in range(len(radiative_decay_data)):
                if radiative_decay_data[j]["upper_level_index"]==i:
                    if radiative_decay_data[j]["radiative_decay_rate"]<=1e-03*total_rate:
                        minor_transition.update([j])

        for i in range(len(radiative_decay_data)):
            if i not in minor_transition:
                reduced_radiative_decay_data.append(radiative_decay_data[i])

        return reduced_radiative_decay_data


    def write(self, atomic_number, electron_number):
        radiative_decay_data = self.generate(atomic_number, electron_number)

        with open("../database02/{0:s}/{0:s}{1:02d}.rd".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(radiative_decay_data)):
                fout.write("{0:6d} {1:4d}   {2:6d} {3:4d}     {4:12.6e}  {5:12.6e}  {6:12.6e}\n".format(radiative_decay_data[i]["upper_level_index"], radiative_decay_data[i]["upper_level_statistical_weight"], radiative_decay_data[i]["lower_level_index"], radiative_decay_data[i]["lower_level_statistical_weight"], radiative_decay_data[i]["transition_energy"], radiative_decay_data[i]["oscillator_strength"], radiative_decay_data[i]["radiative_decay_rate"]))