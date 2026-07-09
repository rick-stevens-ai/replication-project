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

# Model mitosis
def modelMitosis(cond,dnaParams,survParams):
	mitoticRate,apoptoticRate = survParams
	tempCond = list(cond)
	tempCond[3]=0
	initialStatus = DNAModel.modelCellDNA(tempCond,dnaParams)
	initialBreaks = initialStatus[0]
	surv = np.exp(-initialBreaks*mitoticRate)
	tempCond = list(cond)
	tempCond[5] = 0
	G1Surv = modelNonprolif(tempCond,dnaParams,survParams)
	return surv*G1Surv

# Model survival of non-proliferating cells - purely aberration driven
def modelNonprolif(cond,dnaParams,survParams):
	tempCond = list(cond)
	finalStatus = DNAModel.modelCellDNA(tempCond,dnaParams)
	lethalAberrations = finalStatus[2]
	surv= np.exp(-lethalAberrations)
	return surv

# Model survival of proliferating cells. Driven by aberration and G1 arrest. 
def modelG1Prolif(cond,dnaParams,survParams):
	mitoticRate,apoptoticRate = survParams	
	tempCond = list(cond)

	initialBreaks = DNAModel.modelCellDNA(tempCond,dnaParams)
	initialBreaks = initialBreaks[0]

	tempCond[3]=-1
	lethalAberrations = DNAModel.modelCellDNA(tempCond,dnaParams)
	lethalAberrations = lethalAberrations[2]

	apoptoticSurvival = np.exp(-initialBreaks*apoptoticRate)
	surv = np.exp(-lethalAberrations)*apoptoticSurvival
	return surv

# Model survival in G2, allowing for mitotic catastrophe
def modelG2Survival(cond,dnaParams,survParams):
	mitoticRate,apoptoticRate = survParams	
	tempCond = list(cond)
	lethalAberrations = DNAModel.modelCellDNA(tempCond,dnaParams)
	lethalAberrations = lethalAberrations[2]

	tempCond[3]=8
	baseBreaks = DNAModel.modelCellDNA(tempCond,dnaParams)
	baseBreaks = baseBreaks[0]
	MBreaks = min(baseBreaks,20)
	mitoticSurvival = np.exp(-MBreaks*mitoticRate)
	surv= np.exp(-lethalAberrations)*mitoticSurvival
	return surv

# Calculate survival for a single condition
# Logic tree to decide what to treat cells as	
def calculateSurvival(cond,dnaParams,survParams):
	# Mitotic cells
	if cond[5]==3:
		return modelMitosis(cond,dnaParams,survParams)
	# G0 non-proliferating
	if cond[5]==0 and cond[3]<0:
		return modelNonprolif(cond,dnaParams,survParams)
	# G1 proliferating
	if cond[5]==0:
		return modelG1Prolif(cond,dnaParams,survParams)
	# G2 delayed plating
	if cond[5]==2 and cond[3]<0:
		return modelG2Survival(cond,dnaParams,survParams)
	print 'Could not identify cell phase!'
	return -1
