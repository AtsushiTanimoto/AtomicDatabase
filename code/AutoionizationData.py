import pfac.fac


class AutoionizationData:
    def __init__(self):
        self.bound_level_index   = -1
        self.bound_level_twoj    = 0
        self.ionized_level_index = -1
        self.ionized_level_twoj  = 0
        self.transition_energy   = 0.0
        self.autoionization_rate = 0.0
    

    def write(self, atomic_number, electron_number):
        if electron_number==1:
            with open("../database02/{0:s}/{0:s}{1:02d}.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as outfile:
                pass
        else:
            with open("../database01/{0:s}/{0:s}{1:02d}a.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as infile:
                with open("../database02/{0:s}/{0:s}{1:02d}.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as outfile:
                    for line in infile.readlines():
                        data = line.split()

                        if len(data)==7:
                            self.bound_level_index   =   int(data[2])
                            self.bound_level_twoj    =   int(data[3])
                            self.ionized_level_index =   int(data[0])
                            self.ionized_level_twoj  =   int(data[1])
                            self.transition_energy   = float(data[4])
                            self.autoionization_rate = float(data[5])
                            outfile.write("{0:6d} {1:3d}   {2:6d} {3:3d}       {4:10.4e}    {5:10.4e}\n".format(self.bound_level_index, self.bound_level_twoj, self.ionized_level_index, self.ionized_level_twoj, self.transition_energy, self.autoionization_rate))
