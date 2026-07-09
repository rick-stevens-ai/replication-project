# MGM
Microdosimetric Gamma Model to calculate DNA damage

## Introduction
MGM is a microdosimetric gamma model to calculate DNA damage depending on the values of microdosimetric quantities for a given beam.

## Installation
### Requirements
* Python 3
* Python packages: numpy, scipy

## Usage
### Library
The library can be used to calculate the DNA damage provided yF for a monoenergetic beam:
```
import mgm
yF = 4.0 # microdosimetric quantity for a given beam in kev/um

# DNA damage for a monoenergetic beam
MGM = mgm.MicrodosimetricGammaModel()
base_damage = MGM.getBD(yF)
strand_breaks = MGM.getSB(yF)
direct_base_damage = MGM.getBDD(yF)
indirect_base_damage = MGM.getBDI(yF)
direct_strand_breaks = MGM.getSBD(yF)
indirect_strand_breaks = MGM.getSBI(yF)
num_sites = MGM.getN_sites(yF)
num_sites_with_DSB = MGM.getN_sites_with_DSB(yF)
complexity_distribution = MGM.getComplexityDistribution(yF)
```

Another example is provided in the scripts folder to read a microdosimetric distribution,
calculate the resulting DNA damage and plot the results.
```
import mgm

# Data file, format is 'microdose' (3 columns with energy, specific energy and lineal energy)
data_file = 'xray_microdosimetry_1um.phsp'

# Other supported formats are:
# - A list of lineal energy values; each value in a new row
# - A list of bins with number of counts in each bin; each bin in a new row, separated by a space

# Initialize calculator.

calc = mgm.MicrodosimetryGammaCalculator(data_file, format='microdose', subsample=1000)
calc.CalculateDamage()
calc.PlotComplexityDistribution(density=True)

# Gets the number of sites with DSBs
print(calc.getNumberOfSitesWithDSB(perTrack=True))

# Distribute damages over a nucleus with radius 3.5 um. Dose scales the number of damage sites.
# This returns a list of damage sites with position (x, y, z), and complexity
dose = 2 #Gy
damages = calc.DistributeDamageOverNucleus(dose=dose, radius=3.5, inTracks=True)
print('Number of sites for ', dose, ' Gy: ', len(damages))
calc.PlotDistributedDamageOverNucleus()
```