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
    

    def generate(self, atomic_number, electron_number):
        leveldata = []

        with open("../database01/{0:s}/{0:s}{1:02d}a.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="r") as fin:
            for line in fin.readlines():
                data = line.split()
                    
                if len(data)==3:
                    if str(data[0])=="NELE":
                        electron_number = int(data[2])
                elif len(data)==9:
                    self.num_electrons          = electron_number
                    self.level_index            = int(data[0])
                    self.level_index_of_ionized = -1
                    self.level_energy           = float(data[2])
                    self.parity                 = int(data[3])
                    self.nl                     = int(data[4])
                    self.twoj                   = int(data[5])
                    self.configuration          = str(data[6])+" "+str(data[7])+" "+str(data[8])+" "
                    leveldata.append({"num_electrons":self.num_electrons, "level_index":self.level_index, "level_index_of_ionized":self.level_index_of_ionized, "level_energy":self.level_energy, "parity":self.parity, "nl":self.nl, "twoj":self.twoj, "configuration":self.configuration})
        
        return leveldata

    
    def write(self, atomic_number, electron_number):
        leveldata = self.generate(atomic_number, electron_number)
        with open("../database02/{0:s}/{0:s}{1:02d}.en".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            for i in range(len(leveldata)):
                fout.write("{0:2d}   {1:6d} {2:6d}    {3:14.8e}    {4:d}   {5:4d}   {6:3d}   \t{7:s}\n".format(leveldata[i]["num_electrons"], leveldata[i]["level_index"], leveldata[i]["level_index_of_ionized"], leveldata[i]["level_energy"], leveldata[i]["parity"], leveldata[i]["nl"], leveldata[i]["twoj"], leveldata[i]["configuration"]))