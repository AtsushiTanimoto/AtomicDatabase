import pfac.fac


class AutoionizationData:
    def __init__(self):
        self.bound_level_index   = -1
        self.bound_level_twoj    = 0
        self.ionized_level_index = -1
        self.ionized_level_twoj  = 0
        self.transition_energy   = 0.0
        self.autoionization_rate = 0.0
    

    def generate(self, atomic_number, electron_number):
        atomic_symbol       = pfac.fac.ATOMICSYMBOL[atomic_number]
        autoionization_data = []
        maximum_level_index = 0

        if electron_number==1:
            pass
        else:
            with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.px.tr", mode="r") as fin:
                for line in fin.readlines():
                    data                = line.split()
                    maximum_level_index = max(maximum_level_index, int(data[0]))

            with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.ai", mode="r") as fin:
                for line in fin.readlines():
                    data = line.split()

                    if len(data)==7:
                        if int(data[0])<=maximum_level_index:
                            self.bound_level_index   = int(data[0])
                            self.bound_level_twoj    = int(data[1])
                            self.ionized_level_index = int(data[2])
                            self.ionized_level_twoj  = int(data[3])
                            self.transition_energy   = float(data[4])
                            self.autoionization_rate = float(data[5])
                            autoionization_data.append({"bound_level_index":self.bound_level_index, "bound_level_twoj":self.bound_level_twoj, "ionized_level_index":self.ionized_level_index, "ionized_level_twoj":self.ionized_level_twoj, "transition_energy":self.transition_energy, "autoionization_rate":self.autoionization_rate})
        
        return autoionization_data
        

    def write(self, atomic_number, electron_number):
        atomic_symbol       = pfac.fac.ATOMICSYMBOL[atomic_number]
        autoionization_data = self.generate(atomic_number, electron_number)

        if electron_number==1:
            with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.ai", mode="w") as fout:
                pass
        else:
            with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.ai", mode="w") as fout:
                for i in range(len(autoionization_data)):
                    fout.write(f"{autoionization_data[i]['bound_level_index']:6d} {autoionization_data[i]['bound_level_twoj']:3d}   {autoionization_data[i]['ionized_level_index']:6d} {autoionization_data[i]['ionized_level_twoj']:3d}       {autoionization_data[i]['transition_energy']:10.4e}    {autoionization_data[i]['autoionization_rate']:10.4e}\n")