import pandas
import pfac.fac


class LineProbability:
    def __init__(self):
        self.coefficient                = []
        self.num_electrons              = []
        self.lower_level_index          = []
        self.upper_level_index          = []
        self.transition_quantum_numbers = []
        self.transition_energy          = []
        self.probability                = []
    

    def write(self, atomic_number, electron_number, temperatures, densities):
        for i in range(len(temperatures)):
            for j in range(len(densities)):           
                with open("../database02/{0:s}/{0:s}{1:02d}.rates".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
                    for line in fin.readlines():
                        data              = line.split()
                        self.coefficient += [float(data[2])]

                with open("../database01/{0:s}/{0:s}{1:02d}_line/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    for line in fin.readlines():
                        data = line.split()
                        #if 1e+02<=float(data[4]) and 1e-03<=float(data[6])/(self.coefficient[i]*densities[j]):
                        if 1e+02<=float(data[4]):
                            self.num_electrons              += [int(data[0])]
                            self.lower_level_index          += [min(int(data[1]), int(data[2]))]
                            self.upper_level_index          += [max(int(data[1]), int(data[2]))]
                            self.transition_quantum_numbers += [int(data[3])]
                            self.transition_energy          += [float(data[4])]
                            self.probability                += [float(data[6])/self.coefficient[i]/densities[j]]
                
                df = pandas.DataFrame({"num_electrons": self.num_electrons, "lower_level_index": self.lower_level_index, "upper_level_index": self.upper_level_index, "transition_quantum_numbers": self.transition_quantum_numbers, "transition_energy": self.transition_energy, "probability": self.probability})
                df.sort_values("transition_energy", inplace=True)
                df.reset_index(drop=True, inplace=True)

                with open("../database02/{0:s}/{0:s}{1:02d}_ln/{0:s}{1:02d}_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="w") as fout:
                    for k in range(len(df.index)):
                        fout.write("{0:2d}  {1:6d}  {2:6d}    {3:4d}       {4:12.6e}     {5:10.4e}\n".format(df.num_electrons[k], df.lower_level_index[k], df.upper_level_index[k], df.transition_quantum_numbers[k], df.transition_energy[k], df.probability[k]))