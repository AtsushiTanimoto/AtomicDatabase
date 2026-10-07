import pfac.fac


class PopulationData:
    def __init__(self):
        self.level       = -1
        self.possibility = 0.0
        self.threshold   = 1.0e-03


    def generate(self, atomic_number, electron_number, temperature_index, density_index):
        population_data = []

        with open("../database01/{0:s}/{0:s}{1:02d}_spec/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.sp".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, temperature_index, density_index), mode="r") as fin:
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
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                population_data = self.generate(atomic_number, electron_number, i, j)

                with open("../database02/{0:s}/{0:s}{1:02d}_pop/{0:s}{1:02d}_t{2:02d}d{3:02d}i02.pop".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="w") as fout:
                    for k in range(len(population_data)):
                        fout.write("{0:6d}     {1:10.4e}\n".format(population_data[k]["level"], population_data[k]["possibility"]))                   