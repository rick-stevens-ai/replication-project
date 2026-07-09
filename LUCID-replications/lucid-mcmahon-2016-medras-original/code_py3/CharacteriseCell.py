# ############################################################################
# 
# This software is made freely available in accordance with the simplifed BSD
# license:
# 
# Copyright (c) <2016>, <Stephen McMahon>
# All rights reserved
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND 
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Contacts: Stephen McMahon,	stephen.mcmahon@qub.ac.uk
# 
# ############################################################################

import numpy as np
import math
import scipy

# Theta is the integral of recombination probability for a single random DSB, either over a whole cell (2*Radius) or some sub-volume of radius r. 
def theta(sigma,Radius,r=float('nan')):
	# If r is not given, do full cell. 
	if(math.isnan(r)):
		r=2*Radius

	termOne   = 8*np.sqrt(math.pi*2)*pow(Radius,3)*sigma*scipy.special.erf(r/(np.sqrt(2)*sigma))
	termTwo   = -np.exp(-r*r/(2*sigma*sigma))*(pow(r,4)+4*pow(r,2)*(sigma*sigma-3*Radius*Radius)+16*r*pow(Radius,3)+8*sigma*sigma*(sigma*sigma-3*pow(Radius,2)))
	termThree = (8*pow(sigma,4)-24*Radius*Radius*sigma*sigma)
	scaling   = math.pi*(sigma*sigma)/(4*pow(Radius,3))
	thetaVal = (termOne+termTwo+termThree)*scaling
	return thetaVal

# Calculate 'eta' value, characterising probability of misrepair
def calcMisrepairCoefficient(sigma,Radius):
	# Terms obtained from skew correction analysis
	base = 0.7567
	rate = 5.3924

	thetaVal       = 2*theta(sigma,Radius)/(4.0/3.0*math.pi*pow(Radius,3))
	skewCorrection = base+(1-base)*(1-np.exp(-rate*sigma/Radius))
	return thetaVal/skewCorrection

# Calculate inter-chromosome rate
def calcInterChrom(sigma,Radius,chromosomes):
	return 1-theta(sigma,Radius*pow(chromosomes,-1.0/3.0))/theta(sigma,Radius)

# Calculate rate of deletions larger than delSize in MBP
def calcLargeDel(sigma,Radius,chromosomes,genomeSize,delSize):
	largeDelRadius = pow(delSize/(2.0*genomeSize*1000.0),0.333333)
	intraChromRate = theta(sigma,Radius*pow(chromosomes,-1.0/3.0)) / theta(sigma,Radius)
	delFraction    = (1-theta(sigma,pow(chromosomes,-1.0/3.0),largeDelRadius) / theta(sigma,pow(chromosomes,-1.0/3.0)))
	largeDelRate   = intraChromRate*delFraction
	return largeDelRate

# Calculate probability of inter-arm event in same chromosome
def calcInterArm(sigma,Radius,genomeSize,chromosomes,phase):
	# Calculate length of average chromosome based on genome
	# Need additional scaling of 0.5 if we're in G2, due to 2x DNA
	chromosomeLengthMBP = 2000.0*genomeSize/(chromosomes)
	if phase==2:
		chromosomeLengthMBP = chromosomeLengthMBP/2.0
	chromosomeRadius = Radius*pow(chromosomes,-1.0/3.0)
	maxSeparation    = pow((chromosomeLengthMBP/2.0)/(2000.0*genomeSize),1.0/3.0)

	lastBP = 0
	totalProb = 0

	# Iterate over sub-divided chromosome
	for n in range(1,101):
		currRadius = maxSeparation*(n/100.0)
		basePairs  = 2*pow(currRadius,3)*(2000.0*genomeSize)
		chromosomeFrac = (basePairs-lastBP)/chromosomeLengthMBP
		rejoinAtLeastRadius = (1-theta(sigma,chromosomeRadius,currRadius)/theta(sigma,chromosomeRadius))
		totalProb = totalProb+rejoinAtLeastRadius*chromosomeFrac

		# Drop out once probability gets small enough
		if rejoinAtLeastRadius < 0.0001:
			break
		lastBP = basePairs

	return totalProb

# Calculate mutation probability for a misrepair event in a given gene
# Also buffer values, as calculation is time-consuming in full fit.
def calculateMutationProbability(sigma,Radius,genomeSize, chromosomes, geneSize, calculatedProbabilities= []):
	# If size is <=0, no mutation calculation
	if geneSize<=0:
		return 0

	# Try and find precalculated value in buffered list
	parameters = [sigma,Radius,genomeSize,chromosomes,geneSize]
	try:
		probability = (next(x[1] for x in calculatedProbabilities if x[0]==parameters))
		return probability
	except StopIteration:
	# If not found, calculate new value.
		chromosomeRadius = Radius*pow(chromosomes,-1.0/3.0)
		largeDelSize     = 3.0

		interChromRate = calcInterChrom(sigma,Radius,chromosomes)
		largeDelRate   = calcLargeDel(sigma,Radius,chromosomes,genomeSize,largeDelSize)

		# For in gene rate, exclude lethal events - Asymmetric inter-chromosome and large deletions
		partialDelRate = geneSize*(1-0.5*(interChromRate+largeDelRate))

		# Limit deletion count to those which are non-lethal
		maxBreak = max(largeDelSize-geneSize,0)
		steps    = 50
		stepPoints = [x*maxBreak/(1.0*steps) for x in range(steps)]
		inChromRate = theta(sigma,pow(chromosomes,-1.0/3.0))
		fullDelRate = 0

		# Integrate over breaks of each size
		for breakRange in stepPoints:
			minDeletion     = breakRange+geneSize
			minRadius       = pow(minDeletion/(2.0*genomeSize*1000.0),1/3.0)
			atLeastGeneRate = (1-interChromRate)*(1-theta(sigma,pow(chromosomes,-1.0/3.0),minRadius)/inChromRate)
			nonLethalRate   = atLeastGeneRate - largeDelRate # Exclude lethally large deletions
			fullDelRate     = fullDelRate + 0.5*nonLethalRate*maxBreak/steps # Only include asymmetric events, as symmetric preserve gene

		fullDelRate = fullDelRate*0.5/maxBreak # Correct for direction to centromere and normalise to breaks per 1 MBP

		# Log results so we don't have to recalculate this scenario
		calculatedProbabilities.append([parameters,fullDelRate+partialDelRate])

		return fullDelRate + partialDelRate

# Characterise different misrejoining rates for a given cell type
# Cell radius is equal to 1 and sigma is normalised.
def calculateMisrepParameters(sigma,genomeSize,chromosomes,phase,geneSize):
	# Calculate misrepair coefficient
	misRepCoefficient = calcMisrepairCoefficient(sigma,1)

	# Calculate inter-chromosome rate
	interChromRate = calcInterChrom(sigma,1,chromosomes)

	# Calculate rate for large deletions - 3 MBP
	largeDelSize = 3.0
	largeDelRate = calcLargeDel(sigma,1,chromosomes,genomeSize,largeDelSize)

	# Calulate probability for inter-arm rejoining
	interArmRate = calcInterArm(sigma,1,genomeSize,chromosomes,phase)

	# Calculate rate for a given mutation size
	mutationRate = calculateMutationProbability(sigma,1,genomeSize, chromosomes, geneSize)

	misrepairParams = [misRepCoefficient,interChromRate,largeDelRate,interArmRate, mutationRate]

	return misrepairParams

# Calculate visible and lethal aberration rates per misrepaired break
def calculateAberrationRates(phase,interChromRate,largeDelRate,interArmRate):
	# Split by phase, due to differences in visibility and deletion
	if phase == 0:
		# Only asymmetric interchromosome events (dicentrics) are visible, also lethal
		aberrationRateDic = interChromRate*0.5
		visibleDic        = aberrationRateDic

		# Only large asymmetric intrachromosome events (deletions) are visible & lethal
		aberrationRateDel = largeDelRate*0.5
		visibileDel       = aberrationRateDel
	if phase == 2:
		# In G2, all inter-chrom events are visible. Only asymmetric are lethal.
		aberrationRateDic = interChromRate*0.5
		visibleDic        = interChromRate

		# Inter-arm are always visible, and inter-chrom/inter arm are lethal. 
		# Intra-arm are visible if large, but non-lethal
		aberrationRateDel = interArmRate
		visibileDel       = interArmRate  + largeDelRate*(1-interArmRate/(1-interChromRate))
	if phase==3:
		# In mitosis, no repair until we pull through to G1. So treat as G1. 
		# Only asymmetric interchromosome events (dicentrics) are visible, also lethal
		aberrationRateDic = interChromRate*0.5
		visibleDic        = aberrationRateDic

		# Only large asymmetric intrachromosome events (deletions) are visible & lethal
		aberrationRateDel = largeDelRate*0.5
		visibileDel       = aberrationRateDel

	# Sum rates and return
	totalLethal = aberrationRateDic + aberrationRateDel
	aberrRates  = [[aberrationRateDic,aberrationRateDel,totalLethal]]

	totalVisible = visibleDic + visibileDel
	aberrRates.append([visibleDic,visibileDel, totalVisible])

	return aberrRates

# Build a set of cell-line specific misrepair parameters
def characteriseMisrepair(sigma, genomeSize,chromosomes,phase,geneSize):
	# Scale genome size to phase
	if phase==2:
		genomeSize = genomeSize*2

	# Calculate misrepair probabilities, and resulting aberration rates
	misRepCoefficient,interChromRate,largeDelRate,interArmRate, mutationRate = calculateMisrepParameters(sigma,genomeSize,chromosomes,phase,geneSize)
	aberrationRates = calculateAberrationRates(phase,interChromRate,largeDelRate,interArmRate)

	misrepairParams = [misRepCoefficient,interChromRate,largeDelRate,interArmRate,mutationRate,aberrationRates]
	return misrepairParams

# Calculate fraction of repair by each process
def characteriseRepair(complexFrac, failureRate, repairDefect, phase):
	# Basic behaviour for normal cell
	fastRepair     = (1-complexFrac)
	slowRepair     = complexFrac
	verySlowRepair = 0

	# NHEJ defective - fast component fails
	if repairDefect % 2 == 1:
		verySlowRepair = verySlowRepair+ fastRepair*failureRate
		fastRepair     = fastRepair*(1-failureRate)

	# HR defective - if we're in G2, slow component fails. Otherwise no effect
	if (repairDefect / 2) % 2 == 1 and phase== 2:
		verySlowRepair = verySlowRepair + slowRepair*failureRate
		slowRepair     = slowRepair * (1-failureRate)

	return [fastRepair,slowRepair,verySlowRepair]

# Characterise behaviour for a given cell and phase
def characteriseFullCell(sigma,complexFrac,failureRate,genomeSize,chromosomes,repairDefect,phase,geneSize):
	repairParams = characteriseRepair(complexFrac,failureRate,repairDefect,phase)
	misrepairParams = characteriseMisrepair(sigma,genomeSize,chromosomes,phase,geneSize)
	return [repairParams,misrepairParams]

# Get cell parameters. Cache results of calculations so we don't repeat them unnecessarily
def getCellCharacteristics(sigma,complexFrac,failureRate,genomeSize,chromosomes,repairDefect,phase=0,geneSize=0,storedCellParameters=[]):
	parameters = [sigma,complexFrac,failureRate,genomeSize,chromosomes,repairDefect,phase,geneSize]
	try:
		cellParams = (next(x[1] for x in storedCellParameters if x[0]==[parameters]))
		return cellParams
	except StopIteration:
		cellParams = characteriseFullCell(sigma,complexFrac,failureRate,genomeSize,chromosomes,repairDefect,phase,geneSize)
		storedCellParameters.append([[parameters],cellParams])
		return cellParams
