# AMReX
DIM = 3
COMP = gnu
PRECISION = DOUBLE

# Profiling
PROFILE = FALSE
TINY_PROFILE = TRUE

# Performance
USE_MPI = TRUE
USE_OMP = FALSE
USE_CUDA = TRUE
USE_HIP = FALSE
USE_SYCL = FALSE
CUDA_ARCH = 80

# Debugging
DEBUG = FALSE

# PeleC
PELE_CVODE_FORCE_YCORDER = TRUE
PELE_USE_MAGMA = FALSE
PELE_COMPILE_AJACOBIAN = TRUE
Eos_Model := Fuego
Transport_Model := Simple
Chemistry_Model := drm19

# GNU Make
Bpack := ./Make.package
Blocs := .
PELE_HOME := ../../..
include $(PELE_HOME)/Exec/Make.PeleC
