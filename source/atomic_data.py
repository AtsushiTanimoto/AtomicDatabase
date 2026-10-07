import os
import shutil

import pfac.atom
import pfac.fac

import config


if __name__=="__main__":
    for i in config.ATOMIC_NUMBERS:
        atomic_symbol           = pfac.fac.ATOMICSYMBOL[i]
        electron_number_array   = range(1, 1+i)
        output_dir              = f"../database01/{atomic_symbol:s}/"
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)
        pfac.atom.atomic_data(nele=electron_number_array, asym=atomic_symbol, dir=output_dir)
