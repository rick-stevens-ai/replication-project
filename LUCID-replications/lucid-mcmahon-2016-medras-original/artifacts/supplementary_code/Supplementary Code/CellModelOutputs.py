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

import CellDNAModel as DNAModel
import DNAModelFit
import SurvivalFit
import SurvivalModel

##############
# Prepare curve values for figures in paper
##############

# Merge a set of long and short lists into single dataset for printing
def mergeLists(listOfLists):
	maxLength = max([len(l) for l in listOfLists])
	finalSet = []
	for l in listOfLists:
		l=l+[['']*len(l[0])]*(maxLength-len(l))
		if finalSet == []:
			finalSet = l
		else:
			finalSet=[f+p for f,p in zip(finalSet,l)]
	return finalSet

# Prepare mismatch data
def misrepairPrep(popt):
	# Build model curve
	doses = [0.001]+[d*0.8 for d in xrange(1,101)]
	modelNormal = DNAModelFit.modelDNARepair([[d,3.05,46,24,0,0,0,4,-1] for d in doses],*popt)
	outModel = [[d,m] for d,m in zip(doses,modelNormal)]

	mergedList = mergeLists([outModel])

	header = "Dose\tNormal misrepair\n"

	with open('Model Data - Misrepaired Breaks.tsv','w') as f:
		f.write(header)
		for row in mergedList:
			f.write("\t".join(map(str,row)))
			f.write("\n")

# Prepare aberration data
def aberrationPrep(popt):
	# Build model curve
	doses = [0.001]+[d*0.1 for d in xrange(1,101)]
	modelNormal = DNAModelFit.modelDNARepair([[d,3.05,46,-1,0,0,0,1,-1] for d in doses],*popt)
	outModel = [[d,m] for d,m in zip(doses,modelNormal)]

	modelDefective = DNAModelFit.modelDNARepair([[d,3.05,46,-1,1,0,0,1,-1] for d in doses],*popt)
	outDef = [[d,m] for d,m in zip(doses,modelDefective)]

	modelHamster = DNAModelFit.modelDNARepair([[d,2.433,21,-1,0,0,0,1,-1] for d in doses],*popt)
	outHam = [[d,m] for d,m in zip(doses,modelHamster)]


	mergedList = mergeLists([outModel]+[outDef]+[outHam])

	header = "Dose\tNormal aberration\tDose\tMMEJ aberration\tDose\tHamster cell aberrations\t"
	header=header+"\n"

	with open('Model Data - Aberration Yield.tsv','w') as f:
		f.write(header)
		for row in mergedList:
			f.write("\t".join(map(str,row)))
			f.write("\n")

# Prepare mutation data
def mutationPrep(popt):
	# Build model curve
	doses = [0.001]+[d*0.1 for d in xrange(1,101)]
	modelNormal = DNAModelFit.modelDNARepair([[d,3.05,46,-1,0,0,33523/1E6,0,-1] for d in doses],*popt)
	outModel = [[d,m] for d,m in zip(doses,modelNormal)]

	modelHamster = DNAModelFit.modelDNARepair([[d,2.7,22,-1,0,0,33523/1E6,0,-1] for d in doses],*popt)
	outHum = [[d,m] for d,m in zip(doses,modelHamster)]

	pmod = list(popt)
	pmod[3]=0
	modelPointless = DNAModelFit.modelDNARepair([[d,2.7,22,-1,0,0,33523/1E6,0,-1] for d in doses],*pmod)
	outPointless = [[d,m] for d,m in zip(doses,modelPointless)]

	mergedList = mergeLists([outModel]+[outHum]+[outPointless])

	header = "Dose\tNormal mutation\tDose\tHamster misrepair\tDose\tHamster without point mutation\t"
	header=header+"\n"

	with open('Model Data - Mutation Yield.tsv','w') as f:
		f.write(header)
		for row in mergedList:
			f.write("\t".join(map(str,row)))
			f.write("\n")

# Prepare foci data
def fociPrep(popt):
	times = [0.1*t for t in xrange(240)]+[1*t for t in xrange(25,350)]

	modelLists = []
	for phase in [0,2]:
		modelNormal = DNAModelFit.modelDNARepair([[2,3.05,46,t,0,phase,0,2,-1] for t in times],*popt)
		outNormal = [[d,m] for d,m in zip(times,modelNormal)]

		modelNHEJ = DNAModelFit.modelDNARepair([[2,3.05,46,t,1,phase,0,2,-1] for t in times],*popt)
		outNHEJ = [[d,m] for d,m in zip(times,modelNHEJ)]

		modelHR = DNAModelFit.modelDNARepair([[2,3.05,46,t,2,phase,0,2,-1] for t in times],*popt)
		outHR = [[d,m] for d,m in zip(times,modelHR)]

		modelLists = modelLists+[outNormal]+[outNHEJ]+[outHR]

	mergedList = mergeLists(modelLists)

	header = "Time\tNormal G1\tTime\tNHEJ Defective G1\tTime\tHR Defective G1\tTime\tNormal G2\tTime\tNHEJ Defective G2\tTime\tHR Defective G2\t"
	header=header+"\n"

	with open('Model Data - Foci Yields.tsv','w') as f:
		f.write(header)
		for row in mergedList:
			f.write("\t".join(map(str,row)))
			f.write("\n")

# Prepare aberration data by time
def aberrationTimePrep(popt):
	# Build model curve
	times = [t*0.01 for t in range(240)]

	model1Gy = DNAModelFit.modelDNARepair([[1,3.05,46,t,0,2,0,1,-1] for t in times],*popt)
	out1Gy = [[d,m] for d,m in zip(times,model1Gy)]

	model2_5Gy = DNAModelFit.modelDNARepair([[2.5,3.05,46,t,0,2,0,1,-1] for t in times],*popt)
	out2_5Gy = [[d,m] for d,m in zip(times,model2_5Gy)]

	model4Gy = DNAModelFit.modelDNARepair([[4,3.05,46,t,0,2,0,1,-1] for t in times],*popt)
	out4Gy = [[d,m] for d,m in zip(times,model4Gy)]

	mergedList = mergeLists([out1Gy]+[out2_5Gy]+[out4Gy])

	header = "Dose\tAberrations 1 Gy\tDose\tAberrations 2.5 Gy\tDose\tAberrations 4 Gy\t"
	header=header+"\n"

	with open('Model Data - Aberration Kinetics.tsv','w') as f:
		f.write(header)
		for row in mergedList:
			f.write("\t".join(map(str,row)))
			f.write("\n")

# Plot response curves for systems of interest
def plotSurvivalCurves(DNAParams,poptSurv):
	DNAParams = DNAModel.parseParameters(*poptDNA)
	# Plot G1 survival for CHO cells
	doses=[d*0.1 for d in range(0,101)]
	cond=[[d,2.7,22,-1,0,0,0,6,-1] for d in doses]
	G1CHO = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)
	cond=[[d,2.7,22,-1,1,0,0,6,-1] for d in doses]
	G1CHONHEJDefect = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)

	# Same for G2
	cond=[[d,2.7,22,-1,0,2,0,6,-1] for d in doses]
	G2CHO = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)
	cond=[[d,2.7,22,-1,1,2,0,6,-1] for d in doses]
	G2CHONHEJDefect = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)

	# Human line, G1 delayed plating
	cond=[[d,3.05,46,-1,0,0,0,6,-1] for d in doses]
	G1HumDelayed = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)
	cond=[[d,3.05,46,-1,1,0,0,6,-1] for d in doses]
	G1HumDelayedNHEJ = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)

	# Human line, immediate plating
	cond=[[d,3.05,46,0,0,0,0,6,-1] for d in doses]
	G1HumImmed = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)
	cond=[[d,3.05,46,0,1,0,0,6,-1] for d in doses]
	G1HumImmedNHEJ = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)

	# Mitosis
	mitodoses = [d*0.02 for d in range(0,101)]
	cond = [[d,3.05,46,-1,0,3,0,6,-1] for d in mitodoses]
	mitoSurv = SurvivalFit.survivalWrapper(cond,DNAParams,*poptSurv)

	header = "Dose\tG1CHO\tG1CHONHEJDefect\tG2GHO\tG2CHONHEJDefect\tG1HumanDelayed\tG1HumanNHEJDelayed\tG1HumanImmediate\tG1HumanNHEJImmediate\tMitoDose\tMitoticCells\n"
	with open('Model Data - Survival.tsv','w') as f:
		f.write(header)
		for row in zip(doses,G1CHO,G1CHONHEJDefect,G2CHO,G2CHONHEJDefect,G1HumDelayed,G1HumDelayedNHEJ,G1HumImmed,G1HumImmedNHEJ,mitodoses,mitoSurv):
			f.write("\t".join(map(str,row)))
			f.write("\n")

#Prepare data for all figures
def figureCurvePrep(poptDNA,poptSurv):
	fociPrep(poptDNA)
	misrepairPrep(poptDNA)
	aberrationPrep(poptDNA)
	mutationPrep(poptDNA)
	aberrationTimePrep(poptDNA)
	plotSurvivalCurves(poptDNA,poptSurv)


if __name__ == "__main__":
	poptDNA   = DNAModelFit.doFit()
	DNAParams = DNAModel.parseParameters(*poptDNA)
	poptSurv  = SurvivalFit.doFit(DNAParams)

	figureCurvePrep(poptDNA,poptSurv)
