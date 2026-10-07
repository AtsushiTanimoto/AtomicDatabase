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
        atomic_symbol = pfac.fac.ATOMICSYMBOL[i]

        subprocess.call(f"rm -r ../database02/{atomic_symbol:s}", shell=True)
        subprocess.call(f"mkdir ../database02/{atomic_symbol:s}", shell=True)
            
        for j in range(1, min(11, i)):
            densities     = numpy.logspace(0, 0,  1)
            temperatures  = numpy.logspace(0, 4, 41)
            subprocess.call(f"mkdir ../database02/{atomic_symbol:s}/{atomic_symbol:s}{j:02d}_ln", shell=True)
            subprocess.call(f"mkdir ../database02/{atomic_symbol:s}/{atomic_symbol:s}{j:02d}_pop", shell=True)

            logger.info(f"{atomic_symbol:s}{j:02d} PopulationData...")
            population = population_data.PopulationData()
            population.write(i,j,temperatures,densities)
            
            logger.info(f"{atomic_symbol:s}{j:02d} PhotoexcitationData...")
            photoexcitation = photoexcitation_data.PhotoexcitationData()
            photoexcitation.write(i,j,temperatures,densities)
            
            logger.info(f"{atomic_symbol:s}{j:02d} RecombinationRate...")
            recombination = recombination_rate.RecombinationRate()
            recombination.write(i,j,temperatures)

            logger.info(f"{atomic_symbol:s}{j:02d} AutoionizationData...")
            autoionization = autoionization_data.AutoionizationData()
            autoionization.write(i,j)

            logger.info(f"{atomic_symbol:s}{j:02d} LevelData...")
            level = level_data.LevelData()
            level.write(i,j)

            logger.info(f"{atomic_symbol:s}{j:02d} LineProbability...")
            line = line_probability.LineProbability()
            line.write(i,j,temperatures,densities)

            logger.info(f"{atomic_symbol:s}{j:02d} PhotoionizationData...")
            photoionization = photoionization_data.PhotoionizationData()
            photoionization.write(i,j,temperatures,densities)

            logger.info(f"{atomic_symbol:s}{j:02d} RadiativeDecayData...")
            radiative_decay = radiative_decay_data.RadiativeDecayData()
            radiative_decay.write(i,j)

            logger.info(f"{atomic_symbol:s}{j:02d} RadiativeRecombinationData...")
            radiative_recombination = radiative_recombination_data.RadiativeRecombinationData()
            radiative_recombination.write(i,j,temperatures,densities)

            logger.info(f"{atomic_symbol:s}{j:02d} TemperatureDensityGrid...")
            grid = temperature_density_grid.TemperatureDensityGrid()
            grid.write(i,j,temperatures,densities)

            logger.info(f"{atomic_symbol:s}{j:02d} SummaryData...")
            summary = summary_data.SummaryData()
            summary.write(i,j,temperatures,densities)
