#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2/10/23 4:14 PM

@author: alejandrobertolet
"""
from src import mgm

yF = 4.0 # microdosimetric quantity for a given beam in kev/um

# DNA damage for a monoenergetic beam
model = mgm.MicrodosimetricGammaModel()
base_damage = model.getBD(yF)
strand_breaks = model.getSB(yF)
direct_base_damage = model.getBDD(yF)
indirect_base_damage = model.getBDI(yF)
direct_strand_breaks = model.getSBD(yF)
indirect_strand_breaks = model.getSBI(yF)
num_sites = model.getN_sites(yF)
num_sites_with_DSB = model.getN_sites_with_DSB(yF)
complexity_distribution = model.getComplexityDistribution(yF)