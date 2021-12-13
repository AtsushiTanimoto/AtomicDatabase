import pfac.atom
import pfac.fac
import subprocess


if __name__=="__main__":
    for i in range(17,31):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
        directory     = "../database01/{0:s}/".format(atomic_symbol)
        subprocess.run("rm -r {0:s}".format(directory), shell=True)
        subprocess.run("mkdir {0:s}".format(directory), shell=True)
        pfac.atom.atomic_data(nele=range(1,min(11,i)), asym=atomic_symbol, dir=directory)
