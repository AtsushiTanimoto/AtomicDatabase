from pandas import *
import os

class LevelInformation:
    def __init__(self):
        self.num_electrons          = -1
        self.level_index            = -1
        self.level_index_of_ionized = -1
        self.level_energy           = 0.0
        self.parity                 = -1
        self.nl                     = 0
        self.twoj                   = 0
        self.configuration          = ""

    def output(self, data, file):
        df = read_csv(data, sep="\t")
        for index in range(len(df.index)):
            self.num_electrons          = df["Electron"][index]
            self.level_index            = df["Level"][index]-1
            self.level_index_of_ionized = -1
            self.level_energy           = df["Energy"][index]
            self.parity                 = -1
            self.nl                     = 100*df["N"][index]+df["L"][index]
            self.twoj                   = df["2J+1"][index]-1
            self.configuration          = df["Configuration"][index]
            file.write("{0:6d}\t{1:6d}\t{2:6d}\t{3:.8e}\t{4:6d}\t{5:6d}\t{6:6d}\t{7:s}\n".format(self.num_electrons, self.level_index, self.level_index_of_ionized, self.level_energy, self.parity, self.nl, self.twoj, self.configuration))


class TransitionData:
    def __init__(self):
        self.upper_level_index              = -1
        self.upper_level_statistical_weight = 0
        self.lower_level_index              = -1
        self.lower_level_statistical_weight = 0
        self.transition_energy              = 0.0
        self.oscillator_strength            = 0.0
        self.radiative_decay_rate           = 0.0

    def output(self, data, file):
        df = read_csv(data, sep="\t")
        for index in range(len(df.index)):
            self.upper_level_index              = df["Initial Level"][index]-1
            self.upper_level_statistical_weight = 0
            self.lower_level_index              = df["Final Level"][index]-1
            self.lower_level_statistical_weight = 0
            self.transition_energy              = 12398/df["Wavelength"][index]
            self.oscillator_strength            = df["Oscillator Strength"][index]
            self.radiative_decay_rate           = df["Einstein A Coefficient"][index]
            file.write("{0:6d}\t{1:6d}\t{2:6d}\t{3:6d}\t{4:12.6e}\t{5:12.6e}\t{6:12.6e}\n".format(self.upper_level_index, self.upper_level_statistical_weight, self.lower_level_index, self.lower_level_statistical_weight, self.transition_energy, self.oscillator_strength, self.radiative_decay_rate))


class AutoionizationData:
    def __init__(self):
        self.bound_level_index   = -1
        self.bound_level_twoj    = 0
        self.ionized_level_index = -1
        self.ionized_level_twoj  = 0
        self.transition_energy   = 0.0
        self.autoionization_rate = 0.0

    def output(self, data, file):
        df = read_csv(data, sep="\t")
        for index in range(len(df.index)):
            self.bound_level_index   = df["Initial Level"][index]
            self.bound_level_twoj    = df["2J+1"][index]-1
            self.ionized_level_index = df["Final Level"][index]
            self.ionized_level_twoj  = df["2J+1"][index]-1
            self.transition_energy   = df["Energy"][index]
            self.autoionization_rate = df["Rate"][index]
            file.write("{0:6d}\t{1:6d}\t{2:6d}\t{3:6d}\t{4:10.4e}\t{5:10.4e}\n".format(self.bound_level_index, self.bound_level_twoj, self.ionized_level_index, self.ionized_level_twoj, self.transition_energy, self.autoionization_rate))
    

class PhotoionizationData:
    def __init__(self):
        self.bound_level_index    = -1
        self.bound_level_twoj     = 0
        self.ionized_level_index  = -1
        self.ionized_level_twoj   = 0
        self.l                    = 0
        self.ionization_potential = 0.0
        self.sigma0               = 0.0
        self.gamma                = 0.0
        self.tau                  = 0.0
        self.cs_data              = []
        self.fit_status           = 0
        self.fit_chisq            = 0.0
        self.fit_ndf              = 0
    
    def output(self):
        print("{0:6d}\t{1:6d}\t{2:6d}\t{3:6d}\t{4:6d}\t{5:.6e}\t{6:.6e}\t{7:.6e}\t{8:.6e}".format(self.bound_level_index, self.bound_level_twoj, self.ionized_level_index, self.ionized_level_twoj, self.l, self.ionization_potential, self.sigma0, self.gamma, self.tau))


class RadiativeRecombinationData:
    def __init__(self):
        self.num_electrons              = 0
        self.lower_level_index          = -1
        self.upper_level_index          = -1
        self.transition_quantum_numbers = 0
        self.transition_energy          = 0.0
        self.probability                = 0.0
    
    def output(self, data, file):
        df = read_csv(data, sep="\t")
        for index in range(len(df.index)):
            self.num_electrons          = 0
            self.lower_level_index      = df["Final"]
        print("{0:6d}\t{1:6d}\t{2:6d}\t{3:6d}\t{4:.6e}\t{5:.6e}".format(self.num_electrons, self.lower_level_index, self.upper_level_index, self.transition_quantum_numbers, self.transition_energy, self.probability))


if __name__=="__main__":
    Atom = ["Si"]
    Ion  = ["Si01", "Si02", "Si03", "Si04", "Si05", "Si06", "Si07", "Si08", "Si09", "Si10", "Si11", "Si12", "Si13", "Si14"]

    for atom in Atom:
        os.chdir(atom)
        for ion in Ion:
            with open(ion+".en", mode="w") as file:
                Level = LevelInformation()
                Level.output("/Users/tanimoto/github/atomicdatabase/database/"+ion+"_Level.tsv", file)
            with open(ion+".tr", mode="w") as file:
                Transition = TransitionData()
                Transition.output("/Users/tanimoto/github/atomicdatabase/database/"+ion+"_Transition.tsv", file)
            with open(ion+".ai", mode="w") as file:
                Autoionization = AutoionizationData()
                Autoionization.output("/Users/tanimoto/github/atomicdatabase/database/"+ion+"_Autoionization.tsv", file)
        os.chdir("../")