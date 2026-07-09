Mechanistic Modelling of DNA Repair and Cellular Survival Following Radiation-Induced DNA Damage
Stephen J McMahon1,2, Jan Schuemann1, Harald Paganetti1, Kevin M Prise2

1 Department of Radiation Oncology, Massachusetts General Hospital, 30 Fruit St, Boston, MA 02114, USA
2 Centre for Cancer Research and Cell Biology, Queen’s University Belfast, Belfast, BT9 7AE, N. Ireland
-------------------------------------------------------------------------------------------------------

Supplementary Code Notes
-------------------------

This Python code implements the DNA repair and survival models described in the above paper, together 
with helper functions which perform the fitting and plotting associated with the results presented in 
the main text. 

This code was developed using Python 2.7.10, and requires the numpy and Scipy packages. 

To generate the output presented in the paper, the following command can be used:


	python CellModelOutputs.py

This function will a) fit both the DNA repair and Cell Survival models based on the data set used as 
input to the paper; and b) generate output files containing response curves for each of the figures 
presented in the main text. 



The functions contained in each of the python files are also briefly summarised below.


CharacteriseCell.py
-------------------

This is the lowest level of the DNA repair model, and calculates basic rates of misrepair and aberration
formation for a particular cell type. Functions calculate the overlap integral, Theta, and the individual 
rates for different types of aberration and mutation as required for other functions.

CellDNAModel.py
-------------------

This file implements the calculation of biological endpoints for a specified experimental condition, 
which includes both the type of cell, the dose to which it is exposed and the time at which the endpoint
is measured. The main user function in this module is the "modelCellDNA(cond,params)" function, which 
returns a full set of endpoint values for a given condition 'cond' based on a set of fitting parameters 
'params' as defined below. 

SurvivalModel.py
-------------------

This file implements the calculation of survival, based on the DNA repair and cell survival models. The
main user function is "calculateSurvival(cond,dnaParams,survParams)", which returns the predicted 
survival level for a given condition, based on DNA model and survival model params (dnaParams,survParams,
respectively). 


DNAModelFit.py
-------------------

This file implements the fitting of the DNA repair model to the full data set used in this work (included 
as 'Full DNA Data Sets.csv'). If run directly, it will call the core fitting routine, calculate the 
optimum fit, and print the fit statistics and final best-fit parameter set. It is also included as a 
module in higher-level functions, below.

SurvivalFit.py
-------------------

As above, this file implements the fitting of the survival model to the survival data sets (included as 
'Full Survival Data Sets.csv'). If run directly, it will first calculate the optimum DNA repair fitting
parameters through DNAModelFit, and then use these together with the survival model to optimise the 
survival fitting parameters. Once again, fit statistics and best-fit parameter set will be output.


CellModelOutputs.py
-------------------

If called directly, this file uses the above code to calculate the best-fit to each of the data sets for 
both survival and DNA repair, and then calculates the response functions for each of the endpoints 
considered in this work, and plots a series of tsv files with the model curves used in the Figures 
presented in the above paper. 



Condition and Parameter Specification
-------------------

For the purposes of this model, ‘conditions’ define the cell type and experimental conditions leading to
a particular results, and are defined as a list as follows:

[Dose (Gy), Cell Genome size (Gbp), Chromosomes per cell, Time of measurement following irradiation (h), 
Cell Repair Defect (0=Normal, 1=NHEJ Defect, 2=HR Defect), cell phase at irradiation (0=G1, 2=G2, 3=M),
Gene size for mutation rate (Mbp)]

Parameter sets are similarly initially defined as a list, and converted to a dictionary for ease of use.
Parameter arguments are assumed to be in the following order, for DNA repair model:

[sigma, mu_NHEJ, mu_MMEJ, nu, p_c, p_f, lambda_f, lambda_s, lambda_m]

And the survival model:

[Psi, Phi]
