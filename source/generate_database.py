import logging
import subprocess

import numpy
import pfac.fac

import autoionization_data
import config
import level_data
import line_probability
import photoexcitation_data
import photoionization_data
import population_data
import radiative_decay_data
import radiative_recombination_data
import recombination_rate
import summary_data
import temperature_density_grid


if __name__=="__main__":
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger  = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    for i in config.ATOMIC_NUMBERS:
        subprocess.call("rm -r ../database02/{0:s}".format(pfac.fac.ATOMICSYMBOL[i]), shell=True)
        subprocess.call("mkdir ../database02/{0:s}".format(pfac.fac.ATOMICSYMBOL[i]), shell=True)
            
        for j in range(1, min(11, i)):
            densities     = numpy.logspace(0, 0,  1)
            temperatures  = numpy.logspace(0, 4, 41)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_ln" .format(pfac.fac.ATOMICSYMBOL[i],j), shell=True)
            subprocess.call("mkdir ../database02/{0:s}/{0:s}{1:02d}_pop".format(pfac.fac.ATOMICSYMBOL[i],j), shell=True)

            logger.info("{0:s}{1:02d} PopulationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            population = population_data.PopulationData()
            population.write(i,j,temperatures,densities)
            
            logger.info("{0:s}{1:02d} PhotoexcitationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            photoexcitation = photoexcitation_data.PhotoexcitationData()
            photoexcitation.write(i,j,temperatures,densities)
            
            logger.info("{0:s}{1:02d} RecombinationRate...".format(pfac.fac.ATOMICSYMBOL[i],j))
            recombination = recombination_rate.RecombinationRate()
            recombination.write(i,j,temperatures)

            logger.info("{0:s}{1:02d} AutoionizationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            autoionization = autoionization_data.AutoionizationData()
            autoionization.write(i,j)

            logger.info("{0:s}{1:02d} LevelData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            level = level_data.LevelData()
            level.write(i,j)

            logger.info("{0:s}{1:02d} LineProbability...".format(pfac.fac.ATOMICSYMBOL[i],j))
            line = line_probability.LineProbability()
            line.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} PhotoionizationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            photoionization = photoionization_data.PhotoionizationData()
            photoionization.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} RadiativeDecayData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            radiative_decay = radiative_decay_data.RadiativeDecayData()
            radiative_decay.write(i,j)

            logger.info("{0:s}{1:02d} RadiativeRecombinationData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            radiative_recombination = radiative_recombination_data.RadiativeRecombinationData()
            radiative_recombination.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} TemperatureDensityGrid...".format(pfac.fac.ATOMICSYMBOL[i],j))
            grid = temperature_density_grid.TemperatureDensityGrid()
            grid.write(i,j,temperatures,densities)

            logger.info("{0:s}{1:02d} SummaryData...".format(pfac.fac.ATOMICSYMBOL[i],j))
            summary = summary_data.SummaryData()
            summary.write(i,j,temperatures,densities)
