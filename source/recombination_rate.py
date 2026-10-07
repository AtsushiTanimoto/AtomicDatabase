import collections

import pfac.fac


class RecombinationRate:
    def __init__(self):
        pass


    def generate(self, atomic_number, electron_number, temperature_index):
        # spectrum.py の pfac.spm.spectrum が DumpRates で書き出した、衝突輻射モデル自身の率から再結合率を求める
        # .d0: 準位 (占有率), .d1: 放射遷移, .d2: 2 光子崩壊, .d4: 放射再結合, .d5: 自動電離 (dir) と二電子捕獲 (inv)
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        prefix        = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec/{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d0i2.d"
        population    = {}

        with open(prefix + "0", mode="r") as fin:
            for line in fin.readlines():
                data                      = line.split()
                population[int(data[1])] = float(data[8])

        def rates(dump_type):
            with open(prefix + str(dump_type), mode="r") as fin:
                for line in fin.readlines():
                    data = line.split()
                    yield int(data[1]), int(data[2]), float(data[3]), float(data[4])

        radiative_rate      = collections.Counter()
        autoionization_rate = collections.Counter()
        capture_rate        = collections.Counter()

        for dump_type in (1, 2):
            for upper, lower, rate, _ in rates(dump_type):
                radiative_rate[upper] += rate

        for bound, ionized, rate, inverse_rate in rates(5):
            autoionization_rate[bound] += rate
            capture_rate[bound]        += population[ionized]*inverse_rate

        # RR: 再結合する側の準位の占有率 × 率, DR: 二電子捕獲率 × 放射安定化の分岐比
        radiative_recombination_rate    = sum(population[ionized]*rate for ionized, bound, rate, _ in rates(4))
        dielectronic_recombination_rate = sum(capture_rate[level]*radiative_rate[level]/(radiative_rate[level]+autoionization_rate[level]) for level in capture_rate if radiative_rate[level]>0)

        # FAC の単位 (1e-10 cm^3 s^-1) から cm^3 s^-1 に変換
        return 1e-10*radiative_recombination_rate, 1e-10*dielectronic_recombination_rate


    def write(self, atomic_number, electron_number, temperatures):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]

        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.rates", mode="w") as fout:
            for i in range(len(temperatures)):
                radiative_recombination_rate, dielectronic_recombination_rate = self.generate(atomic_number, electron_number, i)
                fout.write(f" {i:02d}     {temperatures[i]:11.5e}     {radiative_recombination_rate:11.5e}   {dielectronic_recombination_rate:11.5e}\n")
