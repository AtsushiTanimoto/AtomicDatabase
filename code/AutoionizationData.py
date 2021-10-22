import pandas
import pfac.fac


class AutoionizationData:
    def __init__(self):
        self.maximum_level_index = 0
        self.bound_level_index   = []
        self.bound_level_twoj    = []
        self.ionized_level_index = []
        self.ionized_level_twoj  = []
        self.transition_energy   = []
        self.autoionization_rate = []
    

    def write(self, atomic_number, electron_number):
        if electron_number==1:
            pass
        else:
            with open("../database02/{0:s}/{0:s}{1:02d}.px".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
                for line in fin.readlines():
                    data               = line.split()
                    self.maximum_level_index = max(self.maximum_level_index, int(data[0]))

            with open("../database01/{0:s}/{0:s}{1:02d}a.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
                for line in fin.readlines():
                        data = line.split()

                        if len(data)==7:
                            if int(data[0])<=self.maximum_level_index:
                                self.bound_level_index   += [int(data[0])]
                                self.bound_level_twoj    += [int(data[1])]
                                self.ionized_level_index += [int(data[2])]
                                self.ionized_level_twoj  += [int(data[3])]
                                self.transition_energy   += [float(data[4])]
                                self.autoionization_rate += [float(data[5])]
                
            df = pandas.DataFrame({"bound_level_index":self.bound_level_index, "bound_level_twoj":self.bound_level_twoj, "ionized_level_index":self.ionized_level_index, "ionized_level_twoj":self.ionized_level_twoj, "transition_energy":self.transition_energy, "autoionization_rate":self.autoionization_rate})
            df.sort_values("bound_level_index", inplace=True)
            df.reset_index(drop=True, inplace=True)
            
        if electron_number==1:
            with open("../database02/{0:s}/{0:s}{1:02d}.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                pass
        else:
            with open("../database02/{0:s}/{0:s}{1:02d}.ai".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
                for i in range(len(df.index)):
                    fout.write("{0:6d} {1:3d}   {2:6d} {3:3d}       {4:10.4e}    {5:10.4e}\n".format(self.bound_level_index[i], self.bound_level_twoj[i], self.ionized_level_index[i], self.ionized_level_twoj[i], self.transition_energy[i], self.autoionization_rate[i]))