import numpy
import pfac.fac


class LineProbability:
    def __init__(self):
        self.num_electrons              = 0
        self.lower_level_index          = -1
        self.upper_level_index          = -1
        self.transition_quantum_numbers = 0
        self.transition_energy          = 0.0
        self.probability                = 0.0
    

    def generate(self, atomic_number, electron_number, temperature_index, density_index):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        coefficient   = []
        line_data     = []
        densities     = numpy.logspace(0,0,1)

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.rates", mode="r") as fin:
            for line in fin.readlines():
                data         = line.split()
                coefficient += [float(data[2])+float(data[3])] # RR + DR

        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_line/{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d{density_index:02d}i02.ln", mode="r") as fin:
            for line in fin.readlines():
                data = line.split()

                if 1e+02<=float(data[4]) and 1e-03<=float(data[6])/(coefficient[temperature_index]*densities[density_index]):
                    self.num_electrons              = int(data[0])
                    self.lower_level_index          = min(int(data[1]), int(data[2]))
                    self.upper_level_index          = max(int(data[1]), int(data[2]))
                    self.transition_quantum_numbers = int(data[3])
                    self.transition_energy          = float(data[4])
                    self.probability                = float(data[6])/(coefficient[temperature_index]*densities[density_index])
                    line_data.append({"num_electrons":self.num_electrons, "lower_level_index":self.lower_level_index, "upper_level_index":self.upper_level_index, "transition_quantum_numbers":self.transition_quantum_numbers, "transition_energy":self.transition_energy, "probability":self.probability})

        line_data = sorted(line_data, key=lambda x:x["transition_energy"])
        return line_data


    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]

        for i in range(len(temperatures)):
            for j in range(len(densities)):
                line_data = self.generate(atomic_number, electron_number, i, j)
                
                with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_ln/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.ln", mode="w") as fout:
                    for k in range(len(line_data)):
                        fout.write(f"{line_data[k]['num_electrons']:2d}  {line_data[k]['lower_level_index']:6d}  {line_data[k]['upper_level_index']:6d}    {line_data[k]['transition_quantum_numbers']:4d}       {line_data[k]['transition_energy']:12.6e}     {line_data[k]['probability']:10.4e}\n")