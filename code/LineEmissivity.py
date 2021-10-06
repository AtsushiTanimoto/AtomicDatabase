import pfac.crm
import pfac.fac
import subprocess


class LineEmissivity:
    def __init__(self):
        pass


    def write(self, atomic_number, electron_number, temperatures, densities):
        minimum_energy = 0.0e+00 # eV
        maximum_energy = 1.0e+04 # eV
        threshold      = 0.0e+00
        transitions    = [1, 2, 3, 4, 5, 6, 7, 201, 202, 301, 302, 303, 401, 402, 403, 404, 501, 502, 503, 504, 505, 601, 602, 603, 604, 605, 606, 701, 702, 703, 704, 705, 706, 707]
        input_dir      = "../database01/{0:s}/{0:s}{1:02d}_spec".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number)
        output_dir     = "../database02/{0:s}/{0:s}{1:02d}_ln"  .format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number)
        subprocess.call("rm -r {0:s}".format(output_dir), shell=True)
        subprocess.call("mkdir {0:s}".format(output_dir), shell=True)

        for i in range(len(temperatures)):
            for j in range(len(densities)):
                for transition in transitions:
                    input_filename  = input_dir  + "/{0:s}{1:02d}b_t{2:02d}d{3:02d}i02.sp".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j)
                    output_filename = output_dir + "/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[atomic_number], electron_number, i, j)
                    pfac.crm.SelectLines(input_filename, output_filename, electron_number, transition, minimum_energy, maximum_energy, threshold)                