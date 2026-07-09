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
import scipy

import CellDNAModel as DNAModel 

# Read file with mutation, aberration and misrepair data
def readDataFile(filename):
	fileData = open(filename,'r')
	# Condition is dose, genome size, chromsome count, time of measurement, 
	# repair defect, cell cycle phase and size of gene for mutation analysis,
	# and paper ID for foci count scaling if needed
	condition=[]
	values=[]
	uncertainty =[]

	for row in fileData:
		if len(row)>0 and row[0][0]!='#':
			#Trim out trailing characters
			while len(row)>0 and (row[-1]=="," or row[-1]=="\n"):
				row=row[:-1]
			if len(row)==0:
				continue
			row = row.split(',')
			row = row[0:11]
			if row[0]=='':
				continue
			row=list(map(float,row))
			cond=row[0:-2]

			if cond[-2]<7:
				condition.append(cond)
				values.append(row[-2])
				uncertainty.append(max(row[-1],0.001*row[-2]+1E-12))

	return (condition,values,uncertainty)

# Add base error to imported data
def addBaseError(values,uncertainty,baseErr):
	newUnc=[]
	for val,unc in zip(values,uncertainty):
		baseVal = val*baseErr
		extraUnc = np.sqrt(unc*unc+baseVal*baseVal)
		newUnc.append(extraUnc)
	return newUnc

# Helper function, to prepare data for fit
def modelDNARepair(conditions,*parameters):
	# Parse parameters into dictionary, for ease of handling
	params = DNAModel.parseParameters(*parameters)
	paperScales = params['PaperScalings']
	retValues = []
	for baseCond in conditions:
		PID = baseCond[-1]
		endPoint = baseCond[-2]
		cond = baseCond[:-2]
		# Mutation rate
		if endPoint==0:
			retValues.append(DNAModel.modelCellDNA(cond,params)[4])
			continue
		# Visible aberration rate
		if endPoint==1:
			retValues.append(DNAModel.modelCellDNA(cond,params)[3])
			continue
		# Remaining DSB foci, scaled by paper scaling if relevant.
		if endPoint==2:
			noBreaks = DNAModel.getFociCount(cond,params)
			noFoci = noBreaks*paperScales[int(PID)-1] if PID>0 else noBreaks
			retValues.append(noFoci)
			continue
		# Old misrepair data. May need little extra calculation or method
		if endPoint==3:
			retValues.append(DNAModel.modelCellDNA(cond,params)[0])
			continue
		# Misrepaired DSBs
		if endPoint==4:
			cellState = DNAModel.modelCellDNA(cond,params)
			incorrectFraction = (cellState[0]+cellState[1])/(cond[0]*cond[1]*DNAModel.DSBPerGBPPerGy)
			retValues.append(incorrectFraction)
			continue
		# Lethal chromosome aberrations. 
		if endPoint==5:
			retValues.append(DNAModel.modelCellDNA(cond,params)[2])
			continue
		print('Error: shouldn\'t be here! ',cond,endPoint,PID)

	return np.array(retValues)

# Execute DNA Model fit
def misrepairFit(conditions,misRep, weights):
	# Get number of papers with foci counts to scale
	paperCount = int(max([cond[-1] for cond in conditions]))

	misRepParams = [0.045,0.99,0.5]
	pointMutations = [0.01]
	complexFraction = [0.4]
	failFrac    = [0.6]
	repairRates = [3.7,0.15,0.008]
	fociCountTweaks = [0.5]*paperCount

	pStart = misRepParams+pointMutations+complexFraction+failFrac+repairRates+fociCountTweaks

	popt,pcov = scipy.optimize.curve_fit(modelDNARepair,conditions,misRep,p0=pStart,sigma=weights)

	return popt, pcov

# Carry out DNA model fit, and return optimum parameter set
def doFit():
	print('DNA Repair Fit')
	conditions,measurements,uncertainty = readDataFile("./Full DNA Data Sets.csv")
	uncertainty=addBaseError(measurements,uncertainty,0.05)	

	fitList = []
	popt, pcov=misrepairFit(conditions,measurements,uncertainty)

	bestModel= modelDNARepair(np.array(conditions),*popt)
	chiSq=[]
	for cond,mut,mod,sig in zip(conditions,measurements,bestModel,uncertainty):
		chiSq.append((mut-mod)*(mut-mod)/(sig*sig))
	print('Chisq: ',sum(chiSq), '\tMean Chisq: ',sum(chiSq)/len(chiSq),'\tN:',len(chiSq), "\n")

	print(DNAModel.parseParameters(*popt))
	return popt

if __name__ == "__main__":
	doFit()
