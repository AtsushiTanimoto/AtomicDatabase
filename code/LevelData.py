import pandas
import pfac.fac


class LevelData:
    def __init__(self):
        self.num_electrons          = []
        self.level_index            = []
        self.level_index_of_ionized = []
        self.level_energy           = []
        self.parity                 = []
        self.nl                     = []
        self.twoj                   = []
        self.configuration          = []
    

    def write(self, atomic_number, electron_number):
        with open("../database01/{0:s}/{0:s}{1:02d}a.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data = line.split()
                    
                if len(data)==3:
                    if str(data[0])=="NELE":
                        electron_number = int(data[2])
                elif len(data)==9:
                    self.num_electrons          += [electron_number]
                    self.level_index            += [int(data[0])]
                    self.level_index_of_ionized += [-1]
                    self.level_energy           += [float(data[2])]
                    self.parity                 += [int(data[3])]
                    self.nl                     += [int(data[4])]
                    self.twoj                   += [int(data[5])]
                    self.configuration          += [str(data[6])+" "+str(data[7])+" "+str(data[8])+" "]

        df = pandas.DataFrame({"num_electrons":self.num_electrons, "level_index":self.level_index, "level_index_of_ionized":self.level_index_of_ionized, "level_energy":self.level_energy, "parity":self.parity, "nl":self.nl, "twoj":self.twoj, "configuration":self.configuration})
        df.sort_values("level_index", inplace=True)
        df.reset_index(drop=True, inplace=True)

        with open("../database02/{0:s}/{0:s}{1:02d}.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(df.index)):
                fout.write("{0:2d}   {1:6d} {2:6d}    {3:14.8e}    {4:d}   {5:4d}   {6:3d}   \t{7:s}\n".format(df.num_electrons[i], df.level_index[i], df.level_index_of_ionized[i], df.level_energy[i], df.parity[i], df.nl[i], df.twoj[i], df.configuration[i]))