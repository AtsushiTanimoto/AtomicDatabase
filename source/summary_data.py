import collections

import pfac.fac


class SummaryData:
    def __init__(self):
        # MONACO の setTwoPhotonDecay() が TransitionDataSet を参照する上位準位 (H 様 2s, He 様 2 1S0)
        self.two_photon_levels = {1:2, 2:5}


    def generate(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        prefix        = f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}"

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
                with open(prefix + f"_ln/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.ln", mode="r") as fin:
                    recombinations[(i, j)] = len(fin.readlines())

        return {"num_levels":num_levels, "num_temperatures":len(temperatures), "num_densities":len(densities), "num_photoexcitations":num_photoexcitations, "num_photoionizations":num_photoionizations, "radiative_decays":radiative_decays, "autoionizations":autoionizations, "recombinations":recombinations}


    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        summary_data  = self.generate(atomic_number, electron_number, temperatures, densities)

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.sum", mode="w") as fout:
            fout.write(f"L {summary_data['num_levels']:8d}\n")
            fout.write(f"G {summary_data['num_temperatures']:3d} {summary_data['num_densities']:3d}\n")
            fout.write(f"X {summary_data['num_photoexcitations']:8d}\n")
            fout.write(f"I {summary_data['num_photoionizations']:8d}\n")

            for level in sorted(summary_data["radiative_decays"]):
                fout.write(f"D {level:8d} {summary_data['radiative_decays'][level]:8d}\n")

            for level in sorted(summary_data["autoionizations"]):
                fout.write(f"A {level:8d} {summary_data['autoionizations'][level]:8d}\n")

            for (i, j) in sorted(summary_data["recombinations"]):
                fout.write(f"R {i:2d} {j:2d} {summary_data['recombinations'][(i, j)]:8d}\n")
