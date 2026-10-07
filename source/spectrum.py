import subprocess

import numpy
import pfac.crm
import pfac.fac
import pfac.spm

import config


def line_emissivity(atomic_number, electron_number, densities, temperatures):
    atomic_symbol  = pfac.fac.ATOMICSYMBOL[atomic_number]
    minimum_energy = 0.000e+00 # eV
    maximum_energy = 1.000e+04 # eV
    threshold      = 0.000e+00
    transitions    = [1, 2, 3, 4, 5, 6, 7, 201, 202, 301, 302, 303, 401, 402, 403, 404, 501, 502, 503, 504, 505, 601, 602, 603, 604, 605, 606, 701, 702, 703, 704, 705, 706, 707]
    input_dir      = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec"
    output_dir     = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_line"
    subprocess.run(f"rm -r {output_dir:s}", shell=True)
    subprocess.run(f"mkdir {output_dir:s}", shell=True)

    for k in range(len(temperatures)):
        for l in range(len(densities)):
            for transition in transitions:
                input_filename  = input_dir  + f"/{atomic_symbol:s}{electron_number:02d}b_t{k:02d}d{l:d}i2.sp"
                output_filename = output_dir + f"/{atomic_symbol:s}{electron_number:02d}a_t{k:02d}d{l:02d}i02.ln"
                pfac.crm.SelectLines(input_filename, output_filename, electron_number, transition, minimum_energy, maximum_energy, threshold)


def spectrum(atomic_number, electron_number, densities, temperatures):
    atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
    input_dir     = f"../database01/{atomic_symbol:s}/"
    output_dir    = f"../database01/{atomic_symbol:s}/{atomic_symbol:s}{electron_number:02d}_spec/"
    populations   = len(temperatures)*[(1+atomic_number)*[1.0/(1+atomic_number)]]
    ai            = 1 if electron_number>1 else 0 # H 様イオンには自動電離準位がない
    subprocess.run(f"rm -r {output_dir:s}", shell=True)
    subprocess.run(f"mkdir {output_dir:s}", shell=True)
    pfac.spm.spectrum(neles=[electron_number], temp=temperatures, den=densities, population=populations, pref=atomic_symbol, dir0=input_dir, dir1=output_dir, nion=2, ai=ai, ce=0, ci=0, rr=1, rrc=1)


if __name__=="__main__":
    density_array       = 1.000e-10*numpy.logspace(0, 0,  1)
    temperature_array   = 1.000e+00*numpy.logspace(0, 4, 41)

    for i in config.ATOMIC_NUMBERS:
        for j in range(1, 1+i):
            spectrum(i, j, density_array, temperature_array)
            line_emissivity(i, j, density_array, temperature_array)