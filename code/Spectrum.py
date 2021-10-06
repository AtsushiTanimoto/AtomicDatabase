import numpy
import pfac.fac
import pfac.spm
import subprocess


if __name__=="__main__":
    for i in range(26,27):
        for j in range(1,2):
            atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
            input_dir     = "../database01/{0:s}/".format(atomic_symbol)
            output_dir    = "../database01/{0:s}/{0:s}{1:02d}_spec/".format(atomic_symbol, j)
            temperatures  = numpy.logspace( 0, 3, 31)
            densities     = numpy.logspace( 0, 0,  1)
            populations   = 31*[(1+i)*[1.0/(1+i)]]
            subprocess.call("rm -r {0:s}".format(output_dir), shell=True)
            subprocess.call("mkdir {0:s}".format(output_dir), shell=True)
                
            if   i==8  and j==2:
                temperatures[0]  = temperatures[1]
                temperatures[30] = temperatures[29]
            elif i==13 and j==2:
                temperatures[4]  = temperatures[3]
            elif i==16 and j==2:
                temperatures[6]  = temperatures[7]
            elif i==18 and j==2:
                temperatures[7]  = temperatures[6]
            elif i==20 and j==2:
                temperatures[7]  = temperatures[6]
                temperatures[8]  = temperatures[9]
            elif i==21 and j==2:
                temperatures[8]  = temperatures[7]
            elif i==23 and j==2:
                temperatures[9]  = temperatures[8]
            elif i==26 and j==2:
                temperatures[10] = temperatures[9]
            elif i==26 and j==3:
                temperatures[10] = temperatures[9]
            elif i==29 and j==2:
                temperatures[11] = temperatures[10]
                
            pfac.spm.spectrum(neles=[j], temp=temperatures, den=densities, population=populations, pref=atomic_symbol, dir0=input_dir, dir1=output_dir, nion=2, ai=0, ce=1, ci=1, rr=1, rrc=1)