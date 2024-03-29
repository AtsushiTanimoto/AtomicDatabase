import pfac.atom
import pfac.fac
import subprocess


if __name__=="__main__":
    for i in range(26, 27):
        atomic_symbol = pfac.fac.ATOMICSYMBOL[i]
        directory     = "/Users/tanimoto/github/AtomicDatabase/database01/{0:s}/".format(atomic_symbol)
        subprocess.run("rm -r {0:s}".format(directory), shell=True)
        subprocess.run("mkdir {0:s}".format(directory), shell=True)
        pfac.atom.atomic_data(nele=range(1, 1+i), asym=atomic_symbol, dir=directory)