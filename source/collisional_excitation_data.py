import os

import numpy
import pfac.fac

import config


EV = 1.602176634e-12   # erg


class CollisionalExcitationData:
    """
    collisional_spectrum() (ce=1 だけの衝突輻射モデル、_specce) から
      .cool: 温度・密度グリッドごとの衝突励起の冷却率 Λ/(n_e n_ion) [erg cm^3 s^-1]
             (全放射遷移と 2 光子崩壊の Σ_u pop_u Σ_l A_ul (E_u - E_l) / n_e。占有率はイオン内で Σ = 1)
             列: 温度番号, kT [eV], 密度番号, n_e [cm^-3], Λ/(n_e n_ion)
      _lnce/<元素><電子数>_tXXdYYi2.ln: 衝突励起の輝線 (遷移エネルギー ≥ config.LINE_ENERGY_MIN)。
             列は .ln と同じ (電子数, 下準位, 上準位, 遷移の種別 (0), エネルギー [eV]) で、最後の列は
             イオン 1 個・電子密度あたりの光子放射率 pop_u A_ul / n_e [cm^3 s^-1] (.ln の「再結合 1 回あたり」とは規格化が違う)
    を作る。準位番号は FAC のもの (.en と同じ)。
    """
    def _level_energies(self, atomic_number, electron_number):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        energies = {}
        with open(f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.en") as f:
            for line in f:
                data = line.split()
                if len(data) >= 6:
                    try:
                        energies[int(data[0])] = float(data[2])
                    except ValueError:
                        pass
        return energies

    def generate(self, atomic_number, electron_number, temperature_index, density_index, energies):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        prefix = (f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_specce/"
                  f"{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d{density_index:d}i2.d")
        n_e = config.DENSITIES[density_index]
        population = {}
        with open(prefix + "0") as f:
            for line in f:
                data = line.split()
                if int(data[0]) == electron_number:
                    population[int(data[1])] = float(data[8])
        lines = []
        cooling = 0.0
        for dump_type in (1, 2):
            if not os.path.exists(prefix + str(dump_type)):
                continue
            with open(prefix + str(dump_type)) as f:
                for line in f:
                    data = line.split()
                    if int(data[0]) != electron_number:
                        continue
                    upper, lower, rate = int(data[1]), int(data[2]), float(data[3])
                    pop = population.get(upper, 0.0)
                    if pop <= 0.0 or rate <= 0.0 or upper not in energies or lower not in energies:
                        continue
                    delta_E = energies[upper] - energies[lower]
                    if delta_E <= 0.0:
                        continue
                    emission = pop * rate / n_e            # 光子放射率 [cm^3 s^-1] (イオン 1 個・n_e あたり)
                    cooling += emission * delta_E * EV
                    if delta_E >= config.LINE_ENERGY_MIN and dump_type == 1:
                        lines.append((lower, upper, delta_E, emission))
        lines.sort(key=lambda x: x[2])
        return cooling, lines

    def write(self, atomic_number, electron_number, temperatures, densities):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        energies = self._level_energies(atomic_number, electron_number)
        prefix = f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}"
        with open(prefix + ".cool", mode="w") as fcool:
            for i in range(len(temperatures)):
                for j in range(len(densities)):
                    cooling, lines = self.generate(atomic_number, electron_number, i, j, energies)
                    fcool.write(f" {i:02d}     {temperatures[i]:11.5e}   {j:02d}     {densities[j]:11.5e}     {cooling:11.5e}\n")
                    with open(f"{prefix}_lnce/{atomic_symbol:s}{electron_number:02d}_t{i:02d}d{j:02d}i2.ln", mode="w") as fln:
                        for lower, upper, delta_E, emission in lines:
                            fln.write(f"{electron_number:2d}  {lower:6d}  {upper:6d}    {0:4d}       {delta_E:12.6e}     {emission:10.4e}\n")
