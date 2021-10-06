import numpy
import pfac.crm
import pfac.fac
import subprocess


if __name__=="__main__":
    for i in range(26,27):
        for j in range(1,11):
            minimum_energy = 0.0e+00 # eV
            maximum_energy = 1.0e+04 # eV
            threshold      = 0.0e+00
            temperatures  = numpy.logspace( 0, 3, 31)
            densities     = numpy.logspace( 0, 0,  1)
            transitions    = [1, 2, 3, 4, 5, 6, 7, 201, 202, 301, 302, 303, 401, 402, 403, 404, 501, 502, 503, 504, 505, 601, 602, 603, 604, 605, 606, 701, 702, 703, 704, 705, 706, 707]
            input_dir      = "../database01/{0:s}/{0:s}{1:02d}_spec".format(pfac.fac.ATOMICSYMBOL[i], j)
            output_dir     = "../database01/{0:s}/{0:s}{1:02d}_line".format(pfac.fac.ATOMICSYMBOL[i], j)
            subprocess.call("rm -r {0:s}".format(output_dir), shell=True)
            subprocess.call("mkdir {0:s}".format(output_dir), shell=True)

            for k in range(len(temperatures)):
                for l in range(len(densities)):
                    for transition in transitions:
                        input_filename  = input_dir  + "/{0:s}{1:02d}b_t{2:02d}d{3:02d}i02.sp".format(pfac.fac.ATOMICSYMBOL[i], j, k, l)
                        output_filename = output_dir + "/{0:s}{1:02d}a_t{2:02d}d{3:02d}i02.ln".format(pfac.fac.ATOMICSYMBOL[i], j, k, l)
                        pfac.crm.SelectLines(input_filename, output_filename, j, transition, minimum_energy, maximum_energy, threshold)                