import pfac.atom
import pfac.fac
import subprocess


if __name__=="__main__":
    for i in range(26,27):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
        directory     = "../database01/{0:s}/".format(atomic_symbol)
        subprocess.call("mkdir {0:s}".format(directory),shell=True)
        pfac.atom.atomic_data(nele=[14], asym=atomic_symbol, dir=directory)