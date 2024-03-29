# Atomic Libraries
import AutoionizationData
import LevelData
import LineProbability
import PhotoexcitationData
import PhotoionizationData
import PopulationData
import RadiativeDecayData
import RadiativeRecombinationData
import RecombinationRate
import TemperatureDensityGrid

# Python Libraries
import logging
import numpy
import pfac.fac
import subprocess


if __name__=="__main__":
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger  = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    for i in range(26, 27):
        subprocess.call("rm -r ../database02/{0:s}".format(pfac.fac.ATOMICSYMBOL[i]), shell=True)
        subprocess.call("mkdir ../database02/{0:s}".format(pfac.fac.ATOMICSYMBOL[i]), shell=True)
            
        for j in range(1, min(11, i)):
            densities     = numpy.logspace(0, 0,  1)
            temperatures  = numpy.logspace(0, 4, 41)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_ln" .format(pfac.fac.ATOMICSYMBOL[i],j), shell=True)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_pop".format(pfac.fac.ATOMICSYMBOL[i],j), shell=True)

            logger.info("{0:s}{1:02d} PopulationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Population = PopulationData.PopulationData()
            Population.write(i,j,temperatures,densities)
            
            logger.info("{0:s}{1:02d} PhotoexcitationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Photoexcitation = PhotoexcitationData.PhotoexcitationData()
            Photoexcitation.write(i,j,temperatures,densities)
            
            logger.info("{0:s}{1:02d} RecombinationRate...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Recombination = RecombinationRate.RecombinationRate()
            Recombination.write(i,j,temperatures)

            logger.info("{0:s}{1:02d} AutoionizationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Autoionization = AutoionizationData.AutoionizationData()
            Autoionization.write(i,j)

            logger.info("{0:s}{1:02d} LevelData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Level = LevelData.LevelData()
            Level.write(i,j)

            logger.info("{0:s}{1:02d} LineProbability...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Line = LineProbability.LineProbability()
            Line.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} PhotoionizationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Photoionization = PhotoionizationData.PhotoionizationData()
            Photoionization.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} RadiativeDecayData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Radiativedecay = RadiativeDecayData.RadiativeDecayData()
            Radiativedecay.write(i,j)

            logger.info("{0:s}{1:02d} RadiativeRecombinationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Radiativerecombination = RadiativeRecombinationData.RadiativeRecombinationData()
            Radiativerecombination.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} TemperatureDensityGrid...".format(pfac.fac.ATOMICSYMBOL[i],j))
            Grid = TemperatureDensityGrid.TemperatureDensityGrid()
            Grid.write(i,j,temperatures,densities)