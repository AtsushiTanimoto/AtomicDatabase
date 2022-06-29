from mpi4py import MPI
import pfac.atom
import pfac.fac
import subprocess


if __name__=="__main__":
    comm          = MPI.COMM_WORLD
    rank          = comm.Get_rank()
    size          = comm.Get_size()
    atomic_symbol = pfac.fac.ATOMICSYMBOL[1+rank]
    directory     = "/Users/tanimoto/github/AtomicDatabase/database01/{0:s}/".format(atomic_symbol)
    subprocess.run("rm -r {0:s}".format(directory), shell=True)
    subprocess.run("mkdir {0:s}".format(directory), shell=True)
    pfac.atom.atomic_data(nele=range(1,min(11,1+rank)), asym=atomic_symbol, dir=directory)