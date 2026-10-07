import os
import shutil

import pfac.atom
import pfac.fac

import config


if __name__=="__main__":
    for i in config.ATOMIC_NUMBERS:
        atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
        output_dir    = "../database01/{0:s}/".format(atomic_symbol)
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)
        pfac.atom.atomic_data(nele=range(1, 1+i), asym=atomic_symbol, dir=output_dir)
