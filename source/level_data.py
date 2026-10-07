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
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        leveldata     = []

        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.en", mode="r") as fin:
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
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        leveldata     = self.generate(atomic_number, electron_number)
        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.en", mode="w") as fout:
            for i in range(len(leveldata)):
                fout.write(f"{leveldata[i]['num_electrons']:2d}   {leveldata[i]['level_index']:6d} {leveldata[i]['level_index_of_ionized']:6d}    {leveldata[i]['level_energy']:14.8e}    {leveldata[i]['parity']:d}   {leveldata[i]['nl']:4d}   {leveldata[i]['twoj']:3d}   \t{leveldata[i]['configuration']:s}\n")