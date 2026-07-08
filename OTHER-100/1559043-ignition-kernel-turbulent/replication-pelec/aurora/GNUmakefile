# AMReX
DIM = 3
COMP = gnu
PRECISION = DOUBLE

PROFILE = FALSE
TINY_PROFILE = TRUE

USE_MPI = TRUE
USE_OMP = FALSE
USE_CUDA = FALSE
USE_HIP = FALSE
USE_SYCL = TRUE

DEBUG = FALSE

# PeleC / Pele
PELE_CVODE_FORCE_YCORDER = TRUE
PELE_USE_MAGMA = FALSE
PELE_COMPILE_AJACOBIAN = TRUE
Eos_Model := Fuego
Transport_Model := Simple
Chemistry_Model := drm19

Bpack := ./Make.package
Blocs := .
PELE_HOME := ../../..
include $(PELE_HOME)/Exec/Make.PeleC
