import pfac.fac


class PhotoexcitationData:
    def __init__(self):
        self.upper_level_index              = -1
        self.upper_level_statistical_weight = 0
        self.lower_level_index              = -1
        self.lower_level_statistical_weight = 0
        self.transition_energy              = 0.0
        self.oscillator_strength            = 0.0
        self.radiative_decay_rate           = 0.0
    

    def generate(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol        = pfac.fac.ATOMICSYMBOL[atomic_number]
        exist_level_index    = set()
        photoexcitation_data = []

        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_pop/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.pop", mode="r") as fin:
                    for line in fin.readlines():
                        data = line.split()
                        exist_level_index.update({int(data[0])})

        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.tr", mode="r") as fin:
            for line in fin.readlines():
                data = line.split()

                if len(data)==8:
                    if int(data[2]) in exist_level_index and 1e-03<=float(data[5])/(1+int(data[3])):
                        self.upper_level_index              = int(data[0])
                        self.upper_level_statistical_weight = 1+int(data[1])
                        self.lower_level_index              = int(data[2])
                        self.lower_level_statistical_weight = 1+int(data[3])
                        self.transition_energy              = float(data[4])
                        self.oscillator_strength            = float(data[5])/(1+int(data[3]))
                        self.radiative_decay_rate           = float(data[6])
                        photoexcitation_data.append({"upper_level_index":self.upper_level_index, "upper_level_statistical_weight":self.upper_level_statistical_weight, "lower_level_index":self.lower_level_index, "lower_level_statistical_weight":self.lower_level_statistical_weight, "transition_energy":self.transition_energy, "oscillator_strength":self.oscillator_strength, "radiative_decay_rate":self.radiative_decay_rate})
    
        return photoexcitation_data
    

    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol        = pfac.fac.ATOMICSYMBOL[atomic_number]
        photoexcitation_data = self.generate(atomic_number, electron_number, temperatures, densities)

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.px.tr", mode="w") as fout:
            for i in range(len(photoexcitation_data)):
                fout.write(f"{photoexcitation_data[i]['upper_level_index']:6d} {photoexcitation_data[i]['upper_level_statistical_weight']:4d}   {photoexcitation_data[i]['lower_level_index']:6d} {photoexcitation_data[i]['lower_level_statistical_weight']:4d}     {photoexcitation_data[i]['transition_energy']:12.6e}  {photoexcitation_data[i]['oscillator_strength']:12.6e}  {photoexcitation_data[i]['radiative_decay_rate']:12.6e}\n")