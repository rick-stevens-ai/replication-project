#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2/10/23 3:39 PM

@author: alejandrobertolet
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, gamma

import matplotlib
matplotlib.use("Qt5Agg")
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['font.size'] = 14

class MicrodosimetricGammaModel:
    def __init__(self, pars=None):
        self._BDD = None
        self._BDD_pars = None
        self._BDI = None
        self._BDI_pars = None
        self._SBD = None
        self._SBD_pars = None
        self._SBI = None
        self._SBI_pars = None
        self._N_sites = None
        self._N_sites_pars = None
        self._N_sites_with_DSB = None
        self._N_sites_with_DSB_pars = None
        self._gamma_par1 = None
        self._gamma_par1_pars = None
        self._gamma_par2 = None
        self._gamma_par2_pars = None
        self.SetFunctionsAndParameters(pars)

    def getBD(self, yF):
        return self.getBDD(yF) + self.getBDI(yF)

    def getSB(self, yF):
        return self.getSBD(yF) + self.getSBI(yF)

    def getBDD(self, yF):
        return self._BDD(yF, *self._BDD_pars)

    def getBDI(self, yF):
        return self._BDI(yF, *self._BDI_pars)

    def getSBD(self, yF):
        return self._SBD(yF, *self._SBD_pars)

    def getSBI(self, yF):
        return self._SBI(yF, *self._SBI_pars)

    def getN_sites(self, yF):
        return self._N_sites(yF, *self._N_sites_pars)

    def getN_sites_with_DSB(self, yF):
        return self._N_sites_with_DSB(yF, *self._N_sites_with_DSB_pars)

    def getGamma_par1(self, yF):
        return self._gamma_par1(yF, *self._gamma_par1_pars)

    def getGamma_par2(self, yF):
        return self._gamma_par2(yF, *self._gamma_par2_pars)

    def getComplexityDistribution(self, yF):
        complexities = np.arange(2, 16)
        return self.gamma_func(complexities, self.getGamma_par1(yF), self.getGamma_par2(yF))

    def SetFunctionsAndParameters(self, pars=None):
        if pars is None:
            self._BDD = self.linear_func
            self._BDD_pars = np.array([1.1438926873102784])
            self._BDI = self.exp_func
            self._BDI_pars = np.array([835.0598386496638, 0.004708596548947047])
            self._SBD = self.linear_func
            self._SBD_pars = np.array([0.9578480335391005])
            self._SBI = self.exp_func
            self._SBI_pars = np.array([150.79186867033644, 0.008818172389461304])
            self._N_sites = self.linear_plus_exp_func
            self._N_sites_pars = np.array([-2.8802301446631557, 1760.3998493763145, 0.005129474298616052])
            self._N_sites_with_DSB = self.linquad_func
            self._N_sites_with_DSB_pars = np.array([0.12961848390465075, 0.0009656759528770472])
            self._gamma_par1 = self.quadratic_func
            self._gamma_par1_pars = np.array([8.413492407157908e-05, 0.007306747718838028, 1.403544707074441])
            self._gamma_par2 = self.quadratic_func
            self._gamma_par2_pars = np.array([-6.623202846258205e-05, 0.0014812837684336443, 1.4943128627102855])
        else:
            if 'BDD' in pars:
                self._BDD = pars['BDD'][0]
                self._BDD_pars = pars['BDD'][1]
            if 'BDI' in pars:
                self._BDI = pars['BDI'][0]
                self._BDI_pars = pars['BDI'][1]
            if 'SBD' in pars:
                self._SBD = pars['SBD'][0]
                self._SBD_pars = pars['SBD'][1]
            if 'SBI' in pars:
                self._SBI = pars['SBI'][0]
                self._SBI_pars = pars['SBI'][1]
            if 'N_sites' in pars:
                self._N_sites = pars['N_sites'][0]
                self._N_sites_pars = pars['N_sites'][1]
            if 'N_sites_with_DSB' in pars:
                self._N_sites_with_DSB = pars['N_sites_with_DSB'][0]
                self._N_sites_with_DSB_pars = pars['N_sites_with_DSB'][1]
            if 'gamma_par1' in pars:
                self._gamma_par1 = pars['gamma_par1'][0]
                self._gamma_par1_pars = pars['gamma_par1'][1]
            if 'gamma_par2' in pars:
                self._gamma_par2 = pars['gamma_par2'][0]
                self._gamma_par2_pars = pars['gamma_par2'][1]


    @staticmethod
    def linear_func(x, a):
        return a * x

    @staticmethod
    def exp_func(x, a, b):
        return a * (1 - np.exp(-b * x))

    @staticmethod
    def linear_plus_exp_func(x, a, c, d):
        return a * x + c * (1 - np.exp(-d * x))

    @staticmethod
    def quadratic_func(x, a, b, c):
        return a * np.array(x) ** 2 + b * np.array(x) + c

    @staticmethod
    def linquad_func(x, a, b):
        return a * x + b * x ** 2

    @staticmethod
    def survival_func(x, alpha, beta):
        return np.exp(-alpha * x - beta * x ** 2)

    @staticmethod
    def poisson_func(x, a):
        return poisson.pmf(x, a)

    @staticmethod
    def gamma_func(x, a, b):
        rv = gamma(a, b)
        return rv.pdf(x)

    @staticmethod
    def sigmoid_func(x, b, c):
        return 1 / (1 + np.exp(-b * (x - c)))

    @staticmethod
    def get_rsquared(y_pred, y_mean, y):
        SS_res = np.sum((y - y_pred) ** 2)
        SS_tot = np.sum((y - y_mean) ** 2)
        return 1 - (SS_res / SS_tot)

    def fit_compound_poisson(data):
        lambda_poisson = poisson.fit(np.round(data))[0]
        lambda_compound = np.mean(data)
        return lambda_poisson, lambda_compound


class MicrodosimetryGammaCalculator:
    def __init__(self, spectrum_filename, format='list', subsample=None):
        self.mgm = MicrodosimetricGammaModel()
        self.reader = MicrodosimetryReader(spectrum_filename, format, subsample)

    def CalculateDamage(self):
        # Calculate the total number of sites
        self.nsites = np.sum(self.mgm.getN_sites_with_DSB(self.reader.lineal_energy))

        # Calculate the complexity distribution
        self.complexities = np.arange(2, 16)
        self.complexitydist = np.sum(
            [self.mgm.getComplexityDistribution(yvalue) for yvalue in self.reader.lineal_energy], axis=0)

    def getComplexityDistribution(self):
        return self.complexities, self.complexitydist

    def getNumberOfSitesWithDSB(self, perTrack=True):
        if perTrack:
            return self.nsites / len(self.reader.lineal_energy)
        return self.nsites

    def PlotComplexityDistribution(self, density=False):
        if density:
            complexitydist = self.complexitydist / np.sum(self.complexitydist)
        else:
            complexitydist = self.complexitydist
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.bar(self.complexities, complexitydist, width=0.5, color='blue', edgecolor='black', alpha=0.5)
        ax.set_xlabel('Complexity')
        ax.set_ylabel('Probability density')
        possible_values = np.array([i for i in np.arange(2, 16, 1)])
        ax.set_xticks(possible_values)
        ax.set_xlim(1.5, 16.5)
        ax.grid(linestyle='--', linewidth=0.5, alpha=0.7)
        plt.draw()
        plt.show()
        return fig, ax

    def DistributeDamageOverNucleus(self, dose, radius, inTracks=True, allParallel=False):
        '''Distribute damage over the nucleus.
        Returns a list of damage sites, containing position and complexity.
        If the parameter inTracks is true, then the damage is distributed in straight lines (as
        many as original tracks we have)'''
        self.radius = radius
        dosepertrack = np.mean(self._getZ(self.reader.lineal_energy, radius))
        totalsites = self.getNumberOfSitesWithDSB(perTrack=True) * dose / dosepertrack
        self.damages = []
        if inTracks:
            nTracks = int(np.round(dose/dosepertrack))
            # Sample straight lines crossing the nucleus and get length for each one of them in the nucleus
            lengths = np.zeros(nTracks)
            trackinitialpoints = np.zeros((nTracks, 3))
            trackdirections = np.zeros((nTracks, 3))
            for i in range(nTracks):
                # Randomly choose a position within the nucleus
                r = np.random.uniform(0, radius)
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                x = r * np.sin(phi) * np.cos(theta)
                y = r * np.sin(phi) * np.sin(theta)
                z = r * np.cos(phi)
                # Randomly choose a direction. If all parallel is True, all tracks will be parallel
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                if allParallel:
                    phi = 0
                dx = np.sin(phi) * np.cos(theta)
                dy = np.sin(phi) * np.sin(theta)
                dz = np.cos(phi)
                # Calculate the length of the track in the nucleus
                lengths[i], distancetoinitialpoint = self._getTrackLength(x, y, z, dx, dy, dz, radius)
                trackinitialpoints[i, :] = np.array([x, y, z]) + distancetoinitialpoint * np.array([dx, dy, dz])
                trackdirections[i, :] = np.array([dx, dy, dz])
            # Assign the number of damages depending on each track length
            shareofdamagepertrack = totalsites * lengths / np.sum(lengths)
            ndamagesPerTrack = np.zeros(nTracks)
            remainingsites = totalsites
            for itrack in range(nTracks):
                while remainingsites > 0 and shareofdamagepertrack[itrack] > 0:
                    ndamagesPerTrack[itrack] += 1
                    shareofdamagepertrack[itrack] -= 1
                    remainingsites -= 1

            # Fill track by track according to the number of damages per track
            for j in range(nTracks):
                while ndamagesPerTrack[j] > 0:
                    # Randomly choose a position within the track
                    r = np.random.uniform(0, lengths[j])
                    x = trackinitialpoints[j, 0] + r * trackdirections[j, 0]
                    y = trackinitialpoints[j, 1] + r * trackdirections[j, 1]
                    z = trackinitialpoints[j, 2] + r * trackdirections[j, 2]
                    # Randomly choose a complexity
                    complexity = np.random.choice(self.complexities, p=self.complexitydist / np.sum(self.complexitydist))
                    self.damages.append([(x, y, z), complexity])
                    ndamagesPerTrack[j] -= 1
        else:
            for i in range(int(totalsites)):
                # Randomly choose a position within the nucleus
                r = np.random.uniform(0, radius)
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                x = r * np.sin(phi) * np.cos(theta)
                y = r * np.sin(phi) * np.sin(theta)
                z = r * np.cos(phi)
                # Randomly choose a complexity
                complexity = np.random.choice(self.complexities, p=self.complexitydist / np.sum(self.complexitydist))
                self.damages.append([(x, y, z), complexity])
        return self.damages

    def PlotDistributedDamageOverNucleus(self, title=None):
        positions = np.array([d[0] for d in self.damages])
        complexities = np.array([d[1] for d in self.damages])

        # Set up a colormap and normalize the complexities to [0, 1] range
        cmap = 'plasma'
        colormap = plt.get_cmap(cmap)
        norm = plt.Normalize(complexities.min(), complexities.max())

        # Plot 3D the positions in a sphere
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        for position, complexity in zip(positions, complexities):
            ax.scatter(position[0], position[1], position[2], s=10 * complexity, c='blue',
                       alpha=0.6)

        # Show a sphere with the radius of the nucleus
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = self.radius * np.cos(u) * np.sin(v)
        y = self.radius * np.sin(u) * np.sin(v)
        z = self.radius * np.cos(v)
        ax.plot_wireframe(x, y, z, color="k", alpha=0.25)

        # Create a legend to show complexities as point sizes
        comps = np.unique(complexities)
        legend_handles = [plt.scatter([], [], s=10 * c, c='blue', alpha=0.7, label=str(c)) for c in comps]
        ax.legend(handles=legend_handles, title='Complexity', loc='upper right')

        # Set axis labels and formatting
        ax.tick_params(axis='both', which='major', labelsize=12, pad=8)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        # Add a title
        if title is None:
            plt.title('Distribution of Damage over Nucleus', fontsize=18, pad=20)
        else:
            plt.title(title, fontsize=14)

        plt.show()

    def _getZ(self, y, radius):
        e = 1.602176634e-19
        yKeVum = y * e * 1e9
        rho = 997  # kg/m^3
        radiusM = radius * 1e-6
        return yKeVum / (rho * np.pi * radiusM**2)

    def _getTrackLength(self, x, y, z, dx, dy, dz, radius):
        # Calculate the intersection of the track with the sphere
        a = dx**2 + dy**2 + dz**2
        b = 2 * (x * dx + y * dy + z * dz)
        c = x**2 + y**2 + z**2 - radius**2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return 0
        else:
            t1 = (-b + np.sqrt(discriminant)) / (2 * a)
            t2 = (-b - np.sqrt(discriminant)) / (2 * a)
            return np.abs(t1 - t2), t2


class MicrodosimetryReader:
    def __init__(self, spectrum_filename, format='list', subsample=None):
        if format == 'microdose':
            self._read_microdose_spectrum(spectrum_filename, subsample)
        elif format == 'list':
            self._read_list_spectrum(spectrum_filename, subsample)
        elif format == 'bins':
            self._read_bins_spectrum(spectrum_filename, subsample)
        self.lineal_energy = np.array(self.lineal_energy)

    def _read_microdose_spectrum(self, spectrum_filename, subsample):
        # Read in the data from the ASCII file
        data = np.loadtxt(spectrum_filename)
        # Separate the columns into arrays
        self.energy_deposits = np.array(data[:, 0])
        self.specific_energy = np.array(data[:, 1])
        self.lineal_energy = data[:, 2]
        if subsample is not None and subsample > 0:
            # Generate a random subsample of the data
            selectedIndexes = np.random.choice(len(self.lineal_energy), subsample, replace=False)
            self.lineal_energy = self.lineal_energy[selectedIndexes]
            self.energy_deposits = self.energy_deposits[selectedIndexes]
            self.specific_energy = self.specific_energy[selectedIndexes]

    def _read_list_spectrum(self, spectrum_filename, subsample):
        # Read in the data from the ASCII file
        self.lineal_energy = np.loadtxt(spectrum_filename)
        if subsample is not None and subsample > 0:
            # Generate a random subsample of the data
            selectedIndexes = np.random.choice(len(self.lineal_energy), subsample, replace=False)
            self.lineal_energy = self.lineal_energy[selectedIndexes]

    def _read_bins_spectrum(self, spectrum_filename, subsample):
        data = np.loadtxt(spectrum_filename)
        self.bins = data[:, 0]
        self.values = data[:, 1]
        self.lineal_energy = []
        for i in range(1, len(self.bins)):
            for j in range(int(self.values[i])):
                # Appends a value with a random number between the bin edges
                self.lineal_energy.append(np.random.uniform(self.bins[i-1], self.bins[i]))
        if subsample is not None and subsample > 0:
            # Generate a random subsample of the data
            selectedIndexes = np.random.choice(len(self.lineal_energy), subsample, replace=False)
            self.lineal_energy = self.lineal_energy[selectedIndexes]

