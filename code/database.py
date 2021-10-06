import AutoionizationData
import LevelData
import LineEmissivity
import logging
import numpy
import pfac.fac
import PopulationData
import RecombinationRate
import subprocess
import TransitionData


if __name__=="__main__":
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger  = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


    for i in range(26,27):
        for j in range(1,i):
            densities     = numpy.logspace(0,0, 1)
            temperatures  = numpy.logspace(0,3,31)
            subprocess.call("mkdir ../database02/{0:s}"                  .format(pfac.fac.ATOMICSYMBOL[i]  ),shell=True)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_line".format(pfac.fac.ATOMICSYMBOL[i],j),shell=True)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_pop" .format(pfac.fac.ATOMICSYMBOL[i],j),shell=True)
            
            logger.info("{0:s}{1:02d} AutoionizationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Autoionization = AutoionizationData.AutoionizationData()
            Autoionization.write(i,j)

            logger.info("{0:s}{1:02d} LevelData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Level = LevelData.LevelData()
            Level.write(i,j)

            logger.info("{0:s}{1:02d} TransitionData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Transition = TransitionData.TransitionData()
            Transition.write(i,j)

            logger.info("{0:s}{1:02d} RecombinationRate...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Recombination = RecombinationRate.RecombinationRate()
            Recombination.write(i,j,temperatures)

            logger.info("{0:s}{1:02d} LineEmissivity...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Line = LineEmissivity.LineEmissivity()
            Line.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} PopulationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Population = PopulationData.PopulationData()
            Population.write(i,j,temperatures,densities)