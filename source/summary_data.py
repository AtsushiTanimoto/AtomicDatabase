import collections

import pfac.fac


class SummaryData:
    def __init__(self):
        # MONACO の setTwoPhotonDecay() が TransitionDataSet を参照する上位準位 (H 様 2s, He 様 2 1S0)
        self.two_photon_levels = {1:2, 2:5}


    def generate(self, atomic_number, electron_number, temperatures, densities):
        prefix = "../database02/{0:s}/{0:s}{1:02d}".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number)

        with open(prefix + ".en", mode="r") as fin:
            num_levels = len(fin.readlines())

        with open(prefix + ".px.tr", mode="r") as fin:
            num_photoexcitations = len(fin.readlines())

        with open(prefix + ".pi", mode="r") as fin:
            num_photoionizations = len(fin.readlines())

        radiative_decays = collections.Counter()
        with open(prefix + ".rd.tr", mode="r") as fin:
            for line in fin.readlines():
                radiative_decays[int(line.split()[0])] += 1

        if electron_number in self.two_photon_levels:
            radiative_decays[self.two_photon_levels[electron_number]] += 0

        autoionizations = collections.Counter()
        with open(prefix + ".ai", mode="r") as fin:
            for line in fin.readlines():
                autoionizations[int(line.split()[0])] += 1

        recombinations = {}
        for i in range(len(temperatures)):
            for j in range(len(densities)):
                with open(prefix + "_ln/{0:s}{1:02d}_t{2:02d}d{3:02d}i2.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j), mode="r") as fin:
                    recombinations[(i, j)] = len(fin.readlines())

        return {"num_levels":num_levels, "num_temperatures":len(temperatures), "num_densities":len(densities), "num_photoexcitations":num_photoexcitations, "num_photoionizations":num_photoionizations, "radiative_decays":radiative_decays, "autoionizations":autoionizations, "recombinations":recombinations}


    def write(self, atomic_number, electron_number, temperatures, densities):
        summary_data = self.generate(atomic_number, electron_number, temperatures, densities)

        with open("../database02/{0:s}/{0:s}{1:02d}.sum".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number), mode="w") as fout:
            fout.write("L {0:8d}\n".format(summary_data["num_levels"]))
            fout.write("G {0:3d} {1:3d}\n".format(summary_data["num_temperatures"], summary_data["num_densities"]))
            fout.write("X {0:8d}\n".format(summary_data["num_photoexcitations"]))
            fout.write("I {0:8d}\n".format(summary_data["num_photoionizations"]))

            for level in sorted(summary_data["radiative_decays"]):
                fout.write("D {0:8d} {1:8d}\n".format(level, summary_data["radiative_decays"][level]))

            for level in sorted(summary_data["autoionizations"]):
                fout.write("A {0:8d} {1:8d}\n".format(level, summary_data["autoionizations"][level]))

            for (i, j) in sorted(summary_data["recombinations"]):
                fout.write("R {0:2d} {1:2d} {2:8d}\n".format(i, j, summary_data["recombinations"][(i, j)]))
