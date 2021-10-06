import pfac.fac


class LineProbability:
    def __init__(self):
        self.num_electrons              = 0
        self.lower_level_index          = -1
        self.upper_level_index          = -1
        self.transition_quantum_numbers = 0
        self.transition_energy          = 0.0
        self.probability                = 0.0
    

    def write(self, atomic_number, electron_number, temperatures, densities):
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                coefficient = []

                with open("../database02/{0:s}/{0:s}{1:02d}.rates", mode="r") as fin:
                    for line in fin.readlines():
                        data         = line.split()
                        coefficient += float(data[2])

                with open("../database01/{0:s}/{0:s}{1:02d}_line/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    with open("../database02/{0:s}/{0:s}{1:02d}_ln/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="w") as fout:
                        for line in fin.readlines():
                            data = line.split()

                            self.num_electrons              = int(data[0])
                            self.lower_level_index          = min(int(data[1]), int(data[2]))
                            self.upper_level_index          = max(int(data[1]), int(data[2]))
                            self.transition_quantum_numbers = int(data[3])
                            self.transition_energy          = float(data[4])
                            self.probability                = float(data[6])/(coefficient[i]*densities[j])
                            fout.write("{0:2d}  {1:6d}  {2:6d}    {3:4d}       {4:12.6e}     {5:10.4e}".format(self.num_electrons, self.lower_level_index, self.upper_level_index, self.transition_quantum_numbers, self.transition_energy, self.probability))