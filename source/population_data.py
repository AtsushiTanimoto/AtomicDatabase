import pfac.fac


class PopulationData:
    def __init__(self):
        self.level       = -1
        self.possibility = 0.0
        self.threshold   = 1.0e-03


    def generate(self, atomic_number, electron_number, temperature_index, density_index):
        atomic_symbol   = pfac.fac.ATOMICSYMBOL[atomic_number]
        population_data = []

        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec/{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d{density_index:d}i2.sp", mode="r") as fin:
            for line in fin.readlines():
                data = line.split()
                
                if len(data)==6:
                    if int(data[0])==0:
                        if str(data[3])=="NAN":
                            #print("population data is nan")
                            self.level       = int(data[0])
                            self.possibility = 1.0
                            population_data.append({"level":self.level, "possibility":self.possibility})
                        elif float(data[3])<=0.0:
                            #print("population data is smaller than 0.0")
                            self.level       = int(data[0])
                            self.possibility = 1.0
                            population_data.append({"level":self.level, "possibility":self.possibility})
                        elif 1.0<float(data[3]):
                            #print("population data is larger than 1.0")
                            self.level       = int(data[0])
                            self.possibility = 1.0
                            population_data.append({"level":self.level, "possibility":self.possibility})
                        else:
                            self.level       =   int(data[0])
                            self.possibility = float(data[3])
                            population_data.append({"level":self.level, "possibility":self.possibility})
                    else:
                        if self.threshold<=float(data[3])<=1.0:
                            self.level       =   int(data[0])
                            self.possibility = float(data[3])
                            population_data.append({"level":self.level, "possibility":self.possibility})
                        else:
                            break

        return population_data


    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]

        for i in range(len(temperatures)):
            for j in range(len(densities)):
                population_data = self.generate(atomic_number, electron_number, i, j)

                with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_pop/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.pop", mode="w") as fout:
                    for k in range(len(population_data)):
                        fout.write(f"{population_data[k]['level']:6d}     {population_data[k]['possibility']:10.4e}\n")                   