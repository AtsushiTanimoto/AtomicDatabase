import os
import shutil

import pfac.atom
import pfac.fac

import argparse

import config


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--elements", default=None, help="元素記号をカンマ区切り (既定: config.ATOMIC_NUMBERS)")
    args = parser.parse_args()
    atomic_numbers = [pfac.fac.ATOMICSYMBOL.index(e.strip().capitalize()) for e in args.elements.split(",")] if args.elements else config.ATOMIC_NUMBERS
    for i in atomic_numbers:
        atomic_symbol           = pfac.fac.ATOMICSYMBOL[i]
        electron_number_array   = range(1, 1+config.MAX_ELECTRON_NUMBERS[i])
        output_dir              = f"../database01/{atomic_symbol:s}/"
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)
        pfac.atom.atomic_data(nele=electron_number_array, asym=atomic_symbol, dir=output_dir)
