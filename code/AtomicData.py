import pfac.atom
import pfac.fac
import subprocess


if __name__=="__main__":
    for i in range(3,11):
        for j in range(1,i):
            atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
            directory     = "../database01/{0:s}/".format(atomic_symbol)
            subprocess.call("rm -r {0:s}".format(directory), shell=True)
            subprocess.call("mkdir {0:s}".format(directory), shell=True)
            pfac.atom.atomic_data(nele=[j], asym=atomic_symbol, dir=directory)