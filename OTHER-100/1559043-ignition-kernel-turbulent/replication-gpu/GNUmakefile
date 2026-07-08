# AMReX
DIM = 3
COMP = gnu
PRECISION = DOUBLE
USE_EB = FALSE
USE_HYPRE = FALSE

# Performance
USE_MPI = TRUE
USE_OMP = FALSE
USE_CUDA = TRUE
USE_HIP = FALSE
USE_SYCL = FALSE
CUDA_ARCH = 80

# Profiling
PROFILE = FALSE
TINY_PROFILE = TRUE

# Debugging
DEBUG = FALSE

# PeleLMeX
USE_PLASMA = FALSE

# PelePhysics - DRM19 methane mechanism (21 species, 84 reactions)
Chemistry_Model = drm19
Eos_Model = Fuego
Transport_Model = Simple

PELE_HOME ?= ../../..
include $(PELE_HOME)/Exec/Make.PeleLMeX
