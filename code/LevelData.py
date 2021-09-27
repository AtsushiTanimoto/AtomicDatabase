import pfac.fac


class LevelData:
    def __init__(self):
        self.num_electrons          = -1
        self.level_index            = -1
        self.level_index_of_ionized = -1
        self.level_energy           = 0.0
        self.parity                 = 0
        self.nl                     = 0
        self.twoj                   = 0
        self.configuration          = ""
    

    def write(self, atomic_number, electron_number):
        with open("/Users/tanimoto/github/AtomicDatabase/database01/{0:s}/{0:s}{1:02d}a.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as infile:
            with open("/Users/tanimoto/github/AtomicDatabase/database02/{0:s}/{0:s}{1:02d}.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as outfile:
                for line in infile.readlines():
                    data     = line.split()
                    
                    if len(data)==3:
                        if str(data[0])=="NELE":
                            electron_number = int(data[2])
                    elif len(data)==9:
                        self.num_electrons          = electron_number
                        self.level_index            =   int(data[0])
                        self.level_index_of_ionized =   int(data[1])
                        self.level_energy           = float(data[2])
                        self.parity                 =   int(data[3])
                        self.nl                     =   int(data[4])
                        self.twoj                   =   int(data[5])
                        self.configuration          =   str(data[6])+" "+str(data[7])+" "+str(data[8])
                        outfile.write("{0:2d}   {1:6d} {2:6d}    {3:14.8e}    {4:d}   {5:4d}   {6:3d}   \t{7:s}\n".format(self.num_electrons, self.level_index, self.level_index_of_ionized, self.level_energy, self.parity, self.nl, self.twoj, self.configuration))