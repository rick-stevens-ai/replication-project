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

import DNAModelFit
import CellDNAModel as DNAModel
import SurvivalModel

# Wrapper to calculate survivals for fit
def survivalWrapper(conditions,DNAParams,*survParams):
	retList = []
	for cond in conditions:
		retList.append(SurvivalModel.calculateSurvival(cond[:-2],DNAParams,survParams))
	return np.array(retList)

# Do survival fit - optionally log transformed
def doFit(DNAParams):
	print '\nSurvival Fit'
	logTransform = True

	# Read in survival data, assume all points are correctly marked as survival
	conditions,survival,uncertainty = DNAModelFit.readDataFile('Full Survival Data Sets.csv')
	uncertainty = DNAModelFit.addBaseError(survival,uncertainty,0.05)

	# Initial guesses for mitotic and apoptic death rates
	mitoticParam = [0.1]
	apopParam = [0.01]
	pStart = mitoticParam+apopParam

	# Log transform for fit if desired
	if logTransform:
		uncertainty = [x/y for x,y in zip(uncertainty,survival)]
		survival    = [np.log(x) for x in survival]
		popt,pcov= scipy.optimize.curve_fit(lambda x,*params :np.log(survivalWrapper(x,DNAParams,*params)),conditions,survival,p0=pStart,sigma=uncertainty)
	else:
		popt,pcov= scipy.optimize.curve_fit(lambda x,*params :survivalWrapper(x,DNAParams,*params),conditions,survival,p0=pStart,sigma=uncertainty)

	bestModel=(survivalWrapper(np.array(conditions),DNAParams,*popt))
	if logTransform:
		bestModel = np.log(bestModel)
	chiSq=[]
	for cond,surv,mod,sig in zip(conditions,survival,bestModel,uncertainty):
		chiSq.append((surv-mod)*(surv-mod)/(sig*sig))

	print 'Chisq: ',sum(chiSq), '\tMean Chisq: ',sum(chiSq)/len(chiSq),'\tN:',len(chiSq), "\n"
	print "Mitotic Rate\tApoptotic Rate"
	print "\t".join(map(str,popt)), "\n","\t".join(map(str,np.sqrt(pcov.diagonal())))

	return popt

if __name__ == "__main__":
	poptDNA   = DNAModelFit.doFit()
	DNAParams = DNAModel.parseParameters(*poptDNA)
	poptSurv  = doFit(DNAParams)
