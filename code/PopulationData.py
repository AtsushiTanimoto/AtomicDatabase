import pfac.fac


class PopulationData:
    def __init__(self):
        self.level       = -1
        self.possibility = 0.0
        self.threshold   = 1.0e-03


    def write(self, atomic_number, electron_number, temperatures, densities):
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open("../database02/{0:s}/{0:s}{1:02d}_spec/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.sp".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    with open("../database02/{0:s}/{0:s}{1:02d}_pop/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.pop".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="w") as fout:
                        for line in fin:
                            data = line.split()
                            if len(data)==6:
                                if int(data[0])==0:
                                    if float(data[3])<=0.0 or 1.0<=float(data[3]) or str(data[3])=="INF":
                                        self.level       =   int(data[0])
                                        self.possibility =   1.0
                                        fout.write("{0:6d}     {1:10.4e}\n".format(self.level, self.possibility))
                                    else:
                                        self.level       =   int(data[0])
                                        self.possibility = float(data[3])
                                        fout.write("{0:6d}     {1:10.4e}\n".format(self.level, self.possibility))
                                else:
                                    if self.threshold<=float(data[3])<=1.0:
                                        self.level       =   int(data[0])
                                        self.possibility = float(data[3])
                                        fout.write("{0:6d}     {1:10.4e}\n".format(self.level, self.possibility))
                                    else:
                                        break