import subprocess

import pfac.crm
import pfac.fac
import pfac.spm

import config


def line_emissivity(atomic_number, electron_number, densities, temperatures):
    atomic_symbol  = pfac.fac.ATOMICSYMBOL[atomic_number]
    minimum_energy = 0.000e+00 # eV
    maximum_energy = 1.000e+04 # eV
    threshold      = 0.000e+00
    transition     = 0 # 0: 全ての輝線と RRC (DR サテライト線など傍観電子のある遷移も含む)
    input_dir      = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec"
    output_dir     = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_line"
    subprocess.run(f"rm -r {output_dir:s}", shell=True)
    subprocess.run(f"mkdir {output_dir:s}", shell=True)

    for k in range(len(temperatures)):
        for l in range(len(densities)):
            input_filename  = input_dir  + f"/{atomic_symbol:s}{electron_number:02d}b_t{k:02d}d{l:d}i2.sp"
            output_filename = output_dir + f"/{atomic_symbol:s}{electron_number:02d}a_t{k:02d}d{l:02d}i02.ln"
            pfac.crm.SelectLines(input_filename, output_filename, electron_number, transition, minimum_energy, maximum_energy, threshold)


def spectrum(atomic_number, electron_number, densities, temperatures):
    """
    再結合 (RR, DR) だけの衝突輻射モデル (nion=2: 対象イオンと 1 階上のイオン)。
    再結合カスケードの輝線 (_line → .ln) と再結合率 (.rates) の元になる。
    イオンの存在比は全段階一様に与えるが、.ln と .rates は上のイオンの占有率で規格化するので結果はこの仮定に依存しない。
    """
    atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
    input_dir     = f"../database01/{atomic_symbol:s}/"
    output_dir    = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec/"
    populations   = len(temperatures)*[(1+atomic_number)*[1.0/(1+atomic_number)]]
    ai            = 1 if electron_number>1 else 0 # H 様イオンには自動電離準位がない
    subprocess.run(f"rm -r {output_dir:s}", shell=True)
    subprocess.run(f"mkdir {output_dir:s}", shell=True)
    pfac.spm.spectrum(neles=[electron_number], temp=temperatures, den=densities, population=populations, pref=atomic_symbol, dir0=input_dir, dir1=output_dir, nion=2, ai=ai, ce=0, ci=0, rr=1, rrc=1)


def collisional_spectrum(atomic_number, electron_number, densities, temperatures):
    """
    衝突励起だけの衝突輻射モデル (pfac.spm.spectrum と同じ手順を crm で直接組む。nion=2、ce=1, ci=1, rr=0, ai=0、
    1 階上のイオンの存在比 0、対象イオンの存在比 1)。出力は _specce/<元素><電子数>a_t<温度>d<密度>i2.d<型>:
      .d0 準位 (列 8 が占有率), .d1 放射遷移, .d2 2 光子崩壊, .d3 衝突励起率 (順・逆), .d6 衝突電離率 (順・逆)
    率の単位は 1e-10 cm^3 s^-1 (放射遷移は s^-1)。
    衝突励起の冷却率 (.cool)・輝線 (_lnce) と衝突電離係数 (.rates) の元になる。
    CI 率は 1 階上のイオンのデータ (SetBlocks) がないと計算されないので nion=2 の形にする。
    """
    atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
    input_dir     = f"../database01/{atomic_symbol:s}/"
    output_dir    = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_specce/"
    subprocess.run(f"rm -r {output_dir:s}", shell=True)
    subprocess.run(f"mkdir {output_dir:s}", shell=True)
    k = electron_number
    pfac.crm.AddIon(k, 0.0, input_dir + f"{atomic_symbol:s}{k:02d}b")
    if k > 1:
        pfac.crm.SetBlocks(0.0, input_dir + f"{atomic_symbol:s}{k-1:02d}b")
    else:
        pfac.crm.SetBlocks(0.0)
    pfac.crm.SetTRRates(0)
    for i in range(len(temperatures)):
        pfac.crm.SetEleDist(0, temperatures[i], -1, -1)
        pfac.crm.SetCERates(1)
        pfac.crm.SetCIRates(1)
        pfac.crm.SetAbund(k-1, 0.0)
        pfac.crm.SetAbund(k, 1.0)
        for j in range(len(densities)):
            pfac.crm.SetEleDensity(densities[j])
            pfac.crm.SetIteration(1e-4)
            pfac.crm.SetCascade(0, 1e-4)
            pfac.crm.InitBlocks()
            pfac.crm.LevelPopulation()
            pfac.crm.Cascade()
            prefix = output_dir + f"{atomic_symbol:s}{k:02d}a_t{i:02d}d{j:d}i2.d"
            for dump_type in (0, 1, 2, 3, 6):
                pfac.crm.DumpRates(prefix + str(dump_type), -1, dump_type, -1, 1)
            pfac.crm.ReinitCRM(3)
        pfac.crm.ReinitCRM(2)
    pfac.crm.ReinitCRM(0)


if __name__=="__main__":
    density_array       = 1.000e-10*config.DENSITIES # FAC の密度の単位は 1e10 cm^-3
    temperature_array   = config.TEMPERATURES

    for i in config.ATOMIC_NUMBERS:
        for j in range(1, 1+config.MAX_ELECTRON_NUMBERS[i]):
            spectrum(i, j, density_array, temperature_array)
            line_emissivity(i, j, density_array, temperature_array)
            collisional_spectrum(i, j, density_array, temperature_array)
