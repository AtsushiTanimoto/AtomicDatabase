import collections
import os

import numpy
import pfac.fac

import config


EV = 1.602176634e-12   # erg


class RecombinationRate:
    """
    .rates: 温度グリッドごとに 1 行
      列: 温度番号, kT [eV], α_RR [cm^3 s^-1], α_DR [cm^3 s^-1], q_CI [cm^3 s^-1] (基底準位からの衝突電離),
          Λ_RR/(n_e n_ion+1) [erg cm^3 s^-1] (放射再結合で電子が失う運動エネルギー),
          Λ_DR/(n_e n_ion+1) [erg cm^3 s^-1] (二電子捕獲で電子が失う運動エネルギー = 共鳴エネルギー)
    再結合は spectrum.py の spectrum() (ce=0) の率ダンプ (_spec)、衝突電離は collisional_spectrum() の率ダンプ (_specce) から。
    """
    def __init__(self):
        self._rr_channels = None

    # ---- 放射再結合の平均運動エネルギー --------------------------------------------------
    def _load_rr_channels(self, atomic_number, electron_number):
        """
        FAC の .rr (database01/<元素><電子数>a.rr) から光電離断面積のチャネル (電離後の準位 i → 束縛準位 b) を読み、
        σ(E) = Σ0 (E/I)^Γ exp(-E/τ) でフィットする (対数線形最小二乗。τ < 0 なら Γ = -3 に固定)。
        戻り値: {(i, b): (I [eV], Γ, τ [eV])}
        """
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        path = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.rr"
        channels = {}
        header, energies, cross_sections = None, [], []

        def flush():
            if header is None or len(energies) < 4:
                return
            E = numpy.array(energies[1:]); sigma = numpy.array(cross_sections[1:])   # 1 点目はパラメータ行
            positive = sigma > 0.0
            if numpy.count_nonzero(positive) < 3:
                return
            E, sigma, I = E[positive], sigma[positive], header[4]
            A = numpy.column_stack([numpy.ones_like(E), numpy.log(E / I), -E])
            c = numpy.linalg.lstsq(A, numpy.log(sigma), rcond=None)[0]
            gamma, inverse_tau = c[1], c[2]
            if inverse_tau <= 0.0:
                A = numpy.column_stack([numpy.ones_like(E), -E])
                c = numpy.linalg.lstsq(A, numpy.log(sigma) + 3.0 * numpy.log(E / I), rcond=None)[0]
                gamma, inverse_tau = -3.0, max(c[1], 1.0e-6)
            channels[(header[2], header[0])] = (I, gamma, 1.0 / inverse_tau)

        with open(path) as f:
            for line in f:
                columns = line.split()
                if len(columns) == 6:
                    try:
                        candidate = [int(columns[0]), int(columns[1]), int(columns[2]), int(columns[3]), float(columns[4]), int(columns[5])]
                    except ValueError:
                        continue
                    flush()
                    header, energies, cross_sections = candidate, [], []
                elif len(columns) == 4 and header is not None:
                    try:
                        energies.append(float(columns[0]) + header[4])
                        cross_sections.append(1.0e-20 * float(columns[2]))
                    except ValueError:
                        pass
        flush()
        return channels

    @staticmethod
    def _mean_kinetic_energy(I, gamma, tau, kT):
        """
        Milne の関係 σ_RR(ε) ∝ (ε+I)^2 σ_PI(ε+I)/ε と Maxwell 分布から、再結合する電子の平均運動エネルギー ⟨ε⟩ [eV]。
        重み w(ε) = (ε+I)^(2+Γ) exp(-(ε+I)/τ) exp(-ε/kT) (定数は比で消える)。
        """
        epsilon = numpy.geomspace(1.0e-4 * kT, 80.0 * kT, 400)
        log_w = (2.0 + gamma) * numpy.log(epsilon + I) - (epsilon + I) / tau - epsilon / kT
        w = numpy.exp(log_w - numpy.max(log_w))
        return numpy.trapezoid(epsilon * w, epsilon) / numpy.trapezoid(w, epsilon)

    # ---- 率ダンプ -----------------------------------------------------------------------
    @staticmethod
    def _read_rates(path):
        with open(path) as f:
            for line in f:
                data = line.split()
                yield int(data[1]), int(data[2]), float(data[3]), float(data[4])

    @staticmethod
    def _read_populations(path):
        population = {}
        with open(path) as f:
            for line in f:
                data = line.split()
                population[int(data[1])] = float(data[8])
        return population

    def _resonance_energies(self, atomic_number, electron_number):
        """.ai (database01/<元素><電子数>a.ai) から自動電離準位 a と電離後の準位 i の組の共鳴エネルギー [eV]"""
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        path = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}a.ai"
        energies = {}
        if not os.path.exists(path):
            return energies
        with open(path) as f:
            for line in f:
                data = line.split()
                if len(data) == 7:
                    try:
                        energies[(int(data[0]), int(data[2]))] = float(data[4])
                    except ValueError:
                        pass
        return energies

    # ---- 1 温度分 --------------------------------------------------------------------------
    def generate(self, atomic_number, electron_number, temperature_index):
        # spectrum.py の pfac.spm.spectrum が DumpRates で書き出した、衝突輻射モデル自身の率から再結合率を求める
        # .d0: 準位 (占有率), .d1: 放射遷移, .d2: 2 光子崩壊, .d4: 放射再結合, .d5: 自動電離 (dir) と二電子捕獲 (inv)
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        prefix = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec/{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d0i2.d"
        kT = config.TEMPERATURES[temperature_index]
        population = self._read_populations(prefix + "0")
        radiative_rate = collections.Counter()
        for dump_type in (1, 2):
            for upper, lower, rate, _ in self._read_rates(prefix + str(dump_type)):
                radiative_rate[upper] += rate
        if self._rr_channels is None:
            self._rr_channels = self._load_rr_channels(atomic_number, electron_number)
            self._resonance = self._resonance_energies(atomic_number, electron_number)

        # RR: 再結合する側の準位の占有率 × 率。冷却は各チャネルの平均運動エネルギーで重み付け
        radiative_recombination_rate = 0.0
        radiative_recombination_cooling = 0.0
        for ionized, bound, rate, _ in self._read_rates(prefix + "4"):
            contribution = population.get(ionized, 0.0) * rate
            radiative_recombination_rate += contribution
            channel = self._rr_channels.get((ionized, bound))
            if channel is not None and contribution > 0.0:
                radiative_recombination_cooling += contribution * self._mean_kinetic_energy(*channel, kT)

        # DR: 二電子捕獲率 × 放射安定化の分岐比。冷却は捕獲された電子の運動エネルギー (共鳴エネルギー) で重み付け
        autoionization_rate = collections.Counter()
        capture_rate = collections.Counter()
        capture_energy = collections.Counter()
        if os.path.exists(prefix + "5"):
            for bound, ionized, rate, inverse_rate in self._read_rates(prefix + "5"):
                autoionization_rate[bound] += rate
                capture = population.get(ionized, 0.0) * inverse_rate
                capture_rate[bound] += capture
                capture_energy[bound] += capture * self._resonance.get((bound, ionized), 0.0)
        dielectronic_recombination_rate = 0.0
        dielectronic_recombination_cooling = 0.0
        for level in capture_rate:
            if radiative_rate[level] > 0.0:
                branching = radiative_rate[level] / (radiative_rate[level] + autoionization_rate[level])
                dielectronic_recombination_rate += capture_rate[level] * branching
                dielectronic_recombination_cooling += capture_energy[level] * branching

        # 衝突電離 (基底準位から全準位へ): collisional_spectrum() の率ダンプ .d6 (密度に依存しないので密度番号 0)
        prefix_ce = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_specce/{atomic_symbol:s}{electron_number:02d}a_t{temperature_index:02d}d0i2.d"
        collisional_ionization_rate = 0.0
        if os.path.exists(prefix_ce + "6"):
            for bound, ionized, rate, _ in self._read_rates(prefix_ce + "6"):
                if bound == 0:
                    collisional_ionization_rate += rate

        # FAC の単位 (1e-10 cm^3 s^-1) から cm^3 s^-1 に、エネルギーは eV から erg に変換
        return (1e-10 * radiative_recombination_rate, 1e-10 * dielectronic_recombination_rate, 1e-10 * collisional_ionization_rate,
                1e-10 * radiative_recombination_cooling * EV, 1e-10 * dielectronic_recombination_cooling * EV)

    def write(self, atomic_number, electron_number, temperatures):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
        self._rr_channels = None
        with open(f"../database02/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}.rates", mode="w") as fout:
            for i in range(len(temperatures)):
                rr, dr, ci, rr_cooling, dr_cooling = self.generate(atomic_number, electron_number, i)
                fout.write(f" {i:02d}     {temperatures[i]:11.5e}     {rr:11.5e}   {dr:11.5e}   {ci:11.5e}   {rr_cooling:11.5e}   {dr_cooling:11.5e}\n")
