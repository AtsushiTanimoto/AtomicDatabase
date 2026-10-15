"""
基底準位の光電離断面積 (.pi) だけを、config.GROUND_PI_ELEMENTS の全元素・全イオン (電子数 1〜Z) について作る。
光電離平衡コード (~/github/photoionized_equilibrium) が共有データベース (電子数 ≤ 10) にないイオンに使う。

  python3 ground_photoionization.py [--elements Mg,Si,S] [--min-electrons 11] [--max-electrons 30] [--include-neutral]

- 中性原子 (電子数 = Z) は既定では飛ばす。FAC の単配置計算は中性原子の閾値付近で精度が悪く (Mg I で Verner の 1/100)、
  光電離平衡コードは中性原子に EPICS2025 の表を使うため。--include-neutral で含める。

- FAC は既定では基底配置の候補と、そこから電子を 1 個抜いた配置だけで構造と RR を計算する (run_fac_ground。1 イオン数秒〜数分)。
  --full なら pfac.atom.atomic_data を RR だけ (no_ce, no_ci, no_ai, no_tr) で走らせる (全励起配置を含み、電子数 14 以上では時間単位)。
  生データは ../database01/<元素>/ に置く (atomic_data.py の全過程の出力と同じ場所・同じファイル名)
  (<元素><電子数>a.rr が既にあれば FAC は走らせない)。
- .rr の基底準位 (束縛準位 0) のチャネルを σ(E) = Σ0 (E/I)^Γ exp(-E/τ) でフィット (対数線形最小二乗。τ < 0 なら Γ = -3 に固定)
  して共有データベース /Users/tanimoto/software/database/atomic_data/<元素>/<元素><電子数>.pi に同じ形式で書く (既にあれば飛ばす)。
- 1 イオンごとに所要時間をログに出す。電子数の多いイオン (特に Fe 以降の中性付近) は FAC に長時間かかるので、
  --min-electrons / --max-electrons と --elements で必要な範囲から順に回す。
"""
import argparse
import os
import time

import numpy
import pfac.atom
import pfac.fac

import config


DATABASE01 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database01")
DATABASE   = "/Users/tanimoto/software/database/atomic_data"   # 共有データベース (MONACO と同じ)。既存の電子数 ≤ 10 の .pi と並べて置く


def read_ground_level_channels(rr_path):
    """.rr から基底準位 (束縛準位 0) のチャネルを読む。戻り値: [(見出し列, E [eV], σ [cm²]), ...]"""
    channels = []
    header, energies, cross_sections = None, [], []

    def flush():
        if header is not None and header[0] == 0 and len(energies) > 1:
            channels.append((header, numpy.array(energies[1:]), numpy.array(cross_sections[1:])))   # 1 点目はパラメータ行

    with open(rr_path) as f:
        for line in f:
            columns = line.split()
            if len(columns) == 6:
                try:
                    candidate = [int(columns[0]), int(columns[1]), int(columns[2]), int(columns[3]), float(columns[4]), int(columns[5])]
                except ValueError:
                    continue
                flush()
                header = candidate
                energies, cross_sections = [], []
            elif len(columns) == 4 and header is not None:
                try:
                    energies.append(float(columns[0]) + header[4])
                    cross_sections.append(1.0e-20 * float(columns[2]))
                except ValueError:
                    pass
    flush()
    return channels


def fit_channel(I, E, sigma):
    """σ(E) = Σ0 (E/I)^Γ exp(−E/τ) のフィット (対数を取って線形最小二乗)。戻り値 (Σ0, Γ, τ) か None"""
    positive = sigma > 0.0
    if numpy.count_nonzero(positive) < 3:
        return None
    E, sigma = E[positive], sigma[positive]
    A = numpy.column_stack([numpy.ones_like(E), numpy.log(E / I), -E])
    c = numpy.linalg.lstsq(A, numpy.log(sigma), rcond=None)[0]
    s0, gamma, inverse_tau = numpy.exp(c[0]), c[1], c[2]
    if inverse_tau <= 0.0:
        A = numpy.column_stack([numpy.ones_like(E), -E])
        c = numpy.linalg.lstsq(A, numpy.log(sigma) + 3.0 * numpy.log(E / I), rcond=None)[0]
        s0, gamma, inverse_tau = numpy.exp(c[0]), -3.0, max(c[1], 1.0e-6)
    return float(s0), float(gamma), float(1.0 / inverse_tau)


def write_pi(symbol, number_of_electrons):
    rr_path = os.path.join(DATABASE01, symbol, f"{symbol}{number_of_electrons:02d}a.rr")
    channels = read_ground_level_channels(rr_path)
    if not channels:
        raise ValueError(f"{rr_path} に基底準位のチャネルがない")
    os.makedirs(os.path.join(DATABASE, symbol), exist_ok=True)
    output = os.path.join(DATABASE, symbol, f"{symbol}{number_of_electrons:02d}.pi")
    with open(output, "w") as f:
        for header, E, sigma in channels:
            fit = fit_channel(header[4], E, sigma)
            if fit is None:
                continue
            s0, gamma, tau = fit
            f.write(f"{header[0]:6d} {header[1]:3d}   {header[2]:6d} {header[3]:3d}  {header[5]:6d}      {header[4]:11.5e}   {s0:10.4e}  {gamma:10.4e}   {tau:10.4e}\n")
    return output


SUBSHELL_ORDER = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p"]   # Madelung 則の順
SUBSHELL_CAPACITY = {"s": 2, "p": 6, "d": 10, "f": 14}


def _fill(order, N):
    occupation = []
    for subshell in order:
        if N <= 0:
            break
        q = min(N, SUBSHELL_CAPACITY[subshell[-1]])
        occupation.append((subshell, q))
        N -= q
    return occupation


def ground_configurations(Z, N):
    """
    基底配置の候補 (FAC の配置文字列のリスト)。中性原子向けの Madelung 則の詰め方と、イオン向けに 3d を 4s より先に
    詰める詰め方の両方を入れ、FAC の Structure で低い方を基底準位にする (遷移金属イオンでは 3d^n が基底)。
    """
    candidates = [_fill(SUBSHELL_ORDER, N)]
    order_3d_first = ["1s", "2s", "2p", "3s", "3p", "3d", "4s", "4p", "5s", "4d", "5p"]
    candidates.append(_fill(order_3d_first, N))
    # 4s と 3d が両方部分的に詰まる場合はその中間 (4s1 3d^(k+1)) も加える
    base = dict(candidates[0])
    if "4s" in base and base["4s"] == 2 and "3d" in base and base["3d"] < 10:
        mixed = dict(base); mixed["4s"] = 1; mixed["3d"] += 1
        candidates.append([(k, mixed[k]) for k in SUBSHELL_ORDER if k in mixed])
    strings = []
    for occupation in candidates:
        text = " ".join(f"{subshell}{q}" for subshell, q in occupation)
        if text not in strings:
            strings.append(text)
    return strings


def ionized_configurations(configurations):
    """各基底配置の候補から電子を 1 個抜いた配置すべて (重複なし)。基底準位からの一電子光電離の終状態"""
    strings = []
    for text in configurations:
        occupation = [(item[:2], int(item[2:])) for item in text.split()]
        for i, (subshell, q) in enumerate(occupation):
            reduced = occupation[:i] + ([(subshell, q - 1)] if q > 1 else []) + occupation[i + 1:]
            ionized = " ".join(f"{s}{n}" for s, n in reduced)
            if ionized and ionized not in strings:
                strings.append(ionized)
    return strings


def run_fac_ground(symbol, Z, number_of_electrons, fac_dir):
    """
    基底準位の光電離に必要な分だけの FAC 計算: 対象イオンは基底配置の候補、電離後のイオンはそこから電子を 1 個抜いた配置。
    pfac.atom.atomic_data (全励起配置を含む) より桁違いに速い。出力は <元素><電子数>{a,b}.{en,rr} (形式は同じ)。
    準位番号は Structure を対象イオン → 電離後のイオンの順に呼ぶので、基底準位が 0 になる。
    """
    import pfac.fac
    prefix = os.path.join(fac_dir, f"{symbol}{number_of_electrons:02d}")
    bound = ground_configurations(Z, number_of_electrons)
    ionized = ionized_configurations(bound)
    pfac.fac.Reinit(0)
    pfac.fac.SetAtom(symbol)
    pfac.fac.Config("g", *bound)
    pfac.fac.Config("i", *ionized)
    if number_of_electrons > 1:
        pfac.fac.ConfigEnergy(0)
    pfac.fac.OptimizeRadial(["g"])
    if number_of_electrons > 1:
        pfac.fac.ConfigEnergy(1)
    pfac.fac.Structure(prefix + "b.en", ["g"])
    pfac.fac.Structure(prefix + "b.en", ["i"])
    pfac.fac.MemENTable(prefix + "b.en")
    pfac.fac.PrintTable(prefix + "b.en", prefix + "a.en", 1)
    pfac.fac.RRTable(prefix + "b.rr", ["g"], ["i"])
    pfac.fac.PrintTable(prefix + "b.rr", prefix + "a.rr", 1)
    pfac.fac.Reinit(0)


def generate(atomic_number, number_of_electrons, full=False):
    symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
    output = os.path.join(DATABASE, symbol, f"{symbol}{number_of_electrons:02d}.pi")
    if os.path.exists(output):
        return "exists"
    fac_dir = os.path.join(DATABASE01, symbol)
    os.makedirs(fac_dir, exist_ok=True)
    if not os.path.exists(os.path.join(fac_dir, f"{symbol}{number_of_electrons:02d}a.rr")):
        if full:
            pfac.atom.atomic_data(nele=[number_of_electrons], asym=symbol, dir=fac_dir + "/",
                                  no_ce=True, no_ci=True, no_ai=True, no_tr=True)
        else:
            run_fac_ground(symbol, atomic_number, number_of_electrons, fac_dir)
    write_pi(symbol, number_of_electrons)
    return "done"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--elements", default=None, help="元素記号をカンマ区切り (既定: config.GROUND_PI_ELEMENTS)")
    parser.add_argument("--min-electrons", type=int, default=1)
    parser.add_argument("--max-electrons", type=int, default=30)
    parser.add_argument("--include-neutral", action="store_true", help="中性原子 (電子数 = Z) も作る")
    parser.add_argument("--full", action="store_true", help="pfac.atom.atomic_data (全励起配置) で計算する (遅い。既定は基底配置と一電子電離の配置だけ)")
    parser.add_argument("--fac-dir", default=None, help="FAC の出力先 (既定: ../database01)。検証用")
    parser.add_argument("--pi-dir", default=None, help=".pi の出力先 (既定: 共有データベース ATOMIC_DATA_DIR)。検証用")
    args = parser.parse_args()
    if args.elements:
        atomic_numbers = [pfac.fac.ATOMICSYMBOL.index(e.strip().capitalize()) for e in args.elements.split(",")]
    else:
        atomic_numbers = config.GROUND_PI_ELEMENTS
    if args.fac_dir:
        DATABASE01 = args.fac_dir
    if args.pi_dir:
        DATABASE = args.pi_dir
    for Z in atomic_numbers:
        symbol = pfac.fac.ATOMICSYMBOL[Z]
        for n in range(max(1, args.min_electrons), min(Z, args.max_electrons) + 1):
            if n == Z and not args.include_neutral:
                continue
            t = time.time()
            try:
                status = generate(Z, n, full=args.full)
            except Exception as error:
                print(f"{symbol}{n:02d}: FAILED ({error})", flush=True)
                continue
            print(f"{symbol}{n:02d}: {status} ({(time.time() - t) / 60.0:.1f} min)", flush=True)
