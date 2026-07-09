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

import CharacteriseCell

#DNA Damage rate, common parameter
DSBPerGBPPerGy = 35/3.05

# Parse flat list of parameters into a dictionary for simplicity
def parseParameters(*parameters):
	params=9
	recombRange,NHEJFidelity,MMEJFidelity,pointMutations,complexFrac,failFrac,fastRepair,slowRepair,verySlowRepair = parameters[0:params]
	paperScales = parameters[params:]
	params = {}
	params['recombRange']=recombRange;    	params['NHEJFidelity']=NHEJFidelity; params['MMEJFidelity']=MMEJFidelity
	params['pointMutations']=pointMutations; 
	params['complexFrac']=complexFrac;		
	params['fastRepair']=fastRepair;	params['slowRepair']=slowRepair;	params['verySlowRepair']=verySlowRepair
	params['failFrac']=failFrac;			

	params['PaperScalings']=list(paperScales)

	return params

# Model probabilities of different events for a single DSB repaired by a single processes
def singleProcessModel(frac,repairRate,time,misrepairParams):
	correctRepairRate,visibleAberrationRate,lethalAberrationRate = misrepairParams
	# Time<0 assume full repair
	if time<0:
		remainingBreaks = 0
	else:
		remainingBreaks  = frac*np.exp(-repairRate*time)
	misrepairedBreaks= (frac-remainingBreaks)*(1-correctRepairRate)
	# NB: Scaling of 0.5 on aberrations, as each 'full' aberration involves 2 misrepaired DSBs
	lethalAberr      = 0.5*misrepairedBreaks*lethalAberrationRate
	visibleAberr     = 0.5*misrepairedBreaks*visibleAberrationRate

	return [remainingBreaks,misrepairedBreaks,lethalAberr,visibleAberr]

# Calculate mutation rate for a specific gene
def calcMutationRate(geneSize,deletionRate,pointMutationRate,initialDSBs,misrepairedDSB,genomeSize):
	# Rate of partial and total deletions. Scaled by 0.5 as each deletion involves 2 misrepaired DSBs
	deletions = 0.5*misrepairedDSB/(genomeSize*2000)*deletionRate

	# Rate of point mutations
	pointMutations = pointMutationRate*(initialDSBs-misrepairedDSB)*geneSize/(genomeSize*2000.0)

	return deletions+pointMutations

# Generate misrepair and aberration rates for a particular process
def calcProcessMisrepair(initialDSBs,fidelity,misrepairParams):
	# If fideliety is exactly 1, assume perfect repair by HR, no aberrations
	if fidelity == 1:
		return [1,0,0]

	# Get per-break misrepair rate and calculate total correct fraction
	eta_misrepair = misrepairParams[0]
	rejoinFidelity = (1-np.exp(-initialDSBs*eta_misrepair))/(initialDSBs*eta_misrepair)
	totalCorrectFrac = rejoinFidelity*fidelity

	# Get aberration rates
	lethalAberrationRate = misrepairParams[5][0][2]
	visibleAberrationRate = misrepairParams[5][1][2]

	# Return repair fidelity and aberration rates
	return [totalCorrectFrac,visibleAberrationRate,lethalAberrationRate]

# Model genetic damage in cell at a given time and dose combination
# Return: Unrepaired DSBs, misrepaired DSBs, visible aberratons, lethal aberrations, mutation rate
def modelCellDNA(cond,params):
	dose,genomeSize,chromosomes,time,repairDefect,phase,geneSize=cond

	# If dose is zero, no damage of any kind.
	if dose==0:
		return [0,0,0,0,0]

	sigma 			= params['recombRange']
	complexFrac 	= params['complexFrac']
	failFrac 		= params['failFrac']
	fastRepair		= params['fastRepair']
	slowRepair 		= params['slowRepair']
	verySlowRepair	= params['verySlowRepair']	
	NHEJFidelity 	= params['NHEJFidelity']
	MMEJFidelity 	= params['MMEJFidelity']
	pointMutationRate = params['pointMutations']

	repairParams,misrepairParams = CharacteriseCell.getCellCharacteristics(sigma,complexFrac,failFrac,genomeSize,chromosomes,repairDefect,phase,geneSize)

	# Calculate total number of DSBs
	initialDSBs = DSBPerGBPPerGy*dose*genomeSize
	# If in G2, double initial DSB count
	if phase>=2:
		initialDSBs=initialDSBs*2

	# Calculate repair parameters for NHEJ, HR, and MMEJ
	# Returns correct rate, visible aberration rate, lethal aberration rate
	NHEJRepairFidelity = calcProcessMisrepair(initialDSBs,NHEJFidelity,misrepairParams)
	HRRepairFidelity   = calcProcessMisrepair(initialDSBs,1,misrepairParams)
	MMEJRepairFideliety= calcProcessMisrepair(initialDSBs,MMEJFidelity,misrepairParams)

	# Assign MMEJ rates to NHEJ or HR as appropriate, if defects are present
	if repairDefect % 2 ==1:
		NHEJRepairFidelity = MMEJRepairFideliety
	if (repairDefect /2 ) % 2 ==1:
		HRRepairFidelity   = MMEJRepairFideliety

	# Sum up events from DSBs repaired by each process for an 'average' DSB
	# Fast repair - NHEJ
	fastBreaks = singleProcessModel(repairParams[0],fastRepair,time,NHEJRepairFidelity)

	# Slow repair - HR if in phase 2, NHEJ otherwise
	if phase==2:
		slowBreaks = singleProcessModel(repairParams[1],slowRepair,time,HRRepairFidelity)
	else:
		slowBreaks = singleProcessModel(repairParams[1],slowRepair,time,NHEJRepairFidelity)

	# Very slow repair - always by MMEJ
	verySlowBreaks = singleProcessModel(repairParams[2],verySlowRepair,time,MMEJRepairFideliety)

	# Sum over all repair processes and scale for full DSB count
	finalCellStatus = [initialDSBs*sum(x) for x in zip(fastBreaks,slowBreaks,verySlowBreaks)]

	# Calculate a mutation rate, if gene size is specified
	if geneSize>0:
		# Get rate for deletions resulting from aberration misrepair
		deletionRate = misrepairParams[4]
		finalCellStatus.append(calcMutationRate(geneSize,deletionRate,pointMutationRate,initialDSBs,finalCellStatus[1],genomeSize))
	else:
		finalCellStatus.append(0)

	# Final return: Unrepaied DSBs, misrepaired DSBs, lethal aberrations, visible aberrations, mutation rate
	return finalCellStatus

# Get foci count, corrected for differences in paper scaling and initial foci delay
def getFociCount(condition,params):
	paperScales = params['PaperScalings']

	newCondition = list(condition)

	newCondition[3]=max(0,newCondition[3]-0.125)
	
	noBreaks = modelCellDNA(newCondition,params)[0]

	return noBreaks
