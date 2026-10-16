# atomic_data.py, spectrum.py, generate_database.py で共通に使う設定
import numpy

ATOMIC_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# 元素ごとの最大電子数 (データベースには電子数 1 から最大電子数までのイオンを含める)
# MONACO の maxElectronsForIonized はこの値以下にすること
MAX_ELECTRON_NUMBERS = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:7, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, 20:20, 21:21, 22:22, 23:23, 24:24, 25:25, 26:26, 27:27, 28:28, 29:29, 30:30}

# 温度・密度グリッド (spectrum.py, generate_database.py, line_probability.py で共有)
# ファイルは tNN / dNN のインデックスで対応づけるため、ここ以外で定義しない
TEMPERATURES = numpy.logspace(-1, 4, 51) # eV (0.1 eV - 10 keV, 0.1 dex 刻み)
DENSITIES    = numpy.logspace(0, 12, 13)   # cm^-3 (1 - 1e12, 1 dex 刻み。占有数・衝突励起の冷却は密度に依存する)

# 衝突励起の輝線 (_lnce) に書き出す遷移エネルギーの下限 [eV] (.ln と同じ。冷却率 .cool には全遷移を使う)
LINE_ENERGY_MIN = 1.0e+02

# ground_photoionization.py (基底準位の光電離断面積 .pi だけを全イオンについて作る) の対象元素。
# 出力は共有データベース /Users/tanimoto/software/database/atomic_data/<元素>/<元素><電子数>.pi (電子数 ≤ 10 の既存ファイルと同じ場所)
GROUND_PI_ELEMENTS = list(range(1, 31))
