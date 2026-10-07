# atomic_data.py, spectrum.py, generate_database.py で共通に使う設定
import numpy

ATOMIC_NUMBERS = [8]

# 温度・密度グリッド (spectrum.py, generate_database.py, line_probability.py で共有)
# ファイルは tNN / dNN のインデックスで対応づけるため、ここ以外で定義しない
TEMPERATURES = numpy.logspace(-1, 4, 51) # eV (0.316 eV - 10 keV, 0.1 dex 刻み)
DENSITIES    = numpy.logspace(0, 0, 1)     # cm^-3
