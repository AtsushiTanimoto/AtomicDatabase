import numpy
import pfac.fac
import pfac.spm
import subprocess


def LineEmissivity(atomic_number, electron_number, densities, temperatures):
    minimum_energy = 0.0e+00 # eV
    maximum_energy = 1.0e+04 # eV
    threshold      = 0.0e+00
    transitions    = [1, 2, 3, 4, 5, 6, 7, 201, 202, 301, 302, 303, 401, 402, 403, 404, 501, 502, 503, 504, 505, 601, 602, 603, 604, 605, 606, 701, 702, 703, 704, 705, 706, 707]
    input_dir      = "../database01/{0:s}/{0:s}{1:02d}_spec".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number)
    output_dir     = "../database01/{0:s}/{0:s}{1:02d}_line".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number)
    subprocess.call("rm -r {0:s}".format(output_dir), shell=True)
    subprocess.call("mkdir {0:s}".format(output_dir), shell=True)

    for k in range(len(temperatures)):
        for l in range(len(densities)):
            for transition in transitions:
                input_filename  = input_dir  + "/{0:s}{1:02d}b_t{2:02d}d{3:02d}i02.sp".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, k, l)
                output_filename = output_dir + "/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, k, l)
                pfac.crm.SelectLines(input_filename, output_filename, electron_number, transition, minimum_energy, maximum_energy, threshold)


def Spectrum(atomic_number, electron_number, densities, temperatures):
    atomic_symbol = pfac.fac.ATOMICSYMBOL[atomic_number]
    input_dir     = "../database01/{0:s}/".format(atomic_symbol)
    output_dir    = "../database01/{0:s}/{0:s}{1:02d}_spec/".format(atomic_symbol, electron_number)
    populations   = 31*[(1+atomic_number)*[1.0/(1+atomic_number)]]
    subprocess.call("rm -r {0:s}".format(output_dir), shell=True)
    subprocess.call("mkdir {0:s}".format(output_dir), shell=True)        
    pfac.spm.spectrum(neles=[electron_number], temp=temperatures, den=densities, population=populations, pref=atomic_symbol, dir0=input_dir, dir1=output_dir, nion=2, ai=0, ce=0, ci=0, rr=1, rrc=1)


def main():
    densities      = 1e-10*numpy.logspace(0, 0, 1)
    temperatures   = 1e+00*numpy.logspace(0, 3, 31)

    for i in range(26,27):
        for j in range(1,3):
            Spectrum(i, j, densities, temperatures)
            LineEmissivity(i, j, densities, temperatures)


if __name__=="__main__":
    main()