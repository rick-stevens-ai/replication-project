1
2
3
4
5
6
7
8
*
Correspondence: aosipov@fmbcfmba.ru; Tel.: +7-915-437-3245

## Abstract
Understanding the relative contributions of different repair pathways to radiation-induced DNA damage responses remains a challenging issue in terms of studying the radiation injury endpoints. The comparative manifestation of homologous recombination (HR) after irradiation with different doses greatly determines the overall effectiveness of recovery in a dividing cell after irradiation, since HR is an error-free mechanism intended to perform the repair of DNA double-strand breaks (DSB) during S/G2 phases of the cell cycle. In this article, we present experimentally observed evidence of dose-dependent shifts in the relative contributions of HR in human fibroblasts after X-ray exposure at doses in the range 20–1000 mGy, which is also supported by quantitative modeling of DNA DSB repair. Our findings indicate that the increase in the radiation dose leads to a dose-dependent decrease in the relative contribution of HR in the entire repair process.

## Keywords: DNA double-strand breaks, ionizing radiation, DNA repair pathways, homologous recombination, mathematical modeling
Keywords: DNA double-strand breaks, ionizing radiation, DNA repair pathways, homologous recombination, mathematical modeling

## Received 2023 Jul 28; Revised 2023 Sep 6; Accepted 2023 Sep 7; Collection date 2023 Sep.
Received 2023 Jul 28; Revised 2023 Sep 6; Accepted 2023 Sep 7; Collection date 2023 Sep.

## 1. IntroductionIonizing radiation (IR) affects the DNA structure by inducing various types of damage, of which DNA double-strand breaks (DSB) are considered to be the most deleterious examples [1,2]. 

## 1. Introduction
Ionizing radiation (IR) affects the DNA structure by inducing various types of damage, of which DNA double-strand breaks (DSB) are considered to be the most deleterious examples [1,2]. DSBs are considered to be critical DNA lesions because their misrepair can lead to severe mutations, oncogenesis, cell death or senescence [3]. In this regard, the selection of an optimal repair pathway is crucial to the cell in terms of achieving a final outcome [4]. Non-homologous end joining (NHEJ) and homologous recombination (HR) are two major DSB repair pathways present in mammalian and human cells. NHEJ fuses the two broken ends with little regard for homology, leading to deletions and other rearrangements [5]. In contrast, HR typically copies the missing information from the sister chromatid into the break site, resulting in the exact reconstitution of the original sequence. In the last few decades, at least three alternative pathways of DSB repair were suggested to be operational following the ionizing radiation exposure. These distinct pathways, namely single-strand annealing (SSA), microhomology-mediated end-joining (MMEJ) and alternative end-joining (Alt-EJ), are distinguished based on the amount of DNA sequence complementarity used to align DNA ends [6].
Revealing the mechanistic nature of DSB repair pathways and evaluating their manifestation in response to different radiation doses aims to improve our understanding of the deleterious effects of ionizing radiation and our ability to predict them [7,8]. The development of our predictive capabilities impacts the accuracy of radiotherapy and radiation-induced cancer risk estimations, as well as being relevant to health issues in people living in areas with high background radiation and future manned space exploration, as astronauts can be exposed to complex radiation fields.
One of the initial events involved in the complex process of DNA repair from DSBs is the phosphorylation of the core histone H2AX by kinases of the PIKK families (phosphatidylinositol 3 kinase-related kinases) ATM, ATR and DNA-PKcs in the flanking regions of DSBs of chromatin [9]. Dynamic microstructures containing thousands of copies of the phosphorylated histone H2AX (γ-H2AX), which are called “foci” in the literature, are easily visualized using immunocytochemical staining [10,11,12]. The analysis of γH2AX foci provides information regarding the number of DNA repair sites derived from DSBs, their distribution over the nuclear volume, and their impact on the kinetics of repair. However, it is equally important to evaluate not only changes in the total number of DSBs, but also the proportion of DSBs repaired via the HR error-free pathway. For this purpose, the analysis of the foci associated with the key HR protein Rad51 is most often used [13].
Computational and mathematical modeling associated with cancer radiotherapy and radiation risk assessments have been undertaken for decades, and they proceed along with the new biophysics phenomena that have been identified [14,15,16,17,18]. Along with the modeling of radiation risk itself, there are a series of models designed to understand the kinetics of radiation-induced DNA damage repair and associated secondary cancer risk. Combining the numerical simulation with experimental methods allows us to identify new mechanistic properties involved in the DNA repair process, which are hardly accessible to experimental studies, but could be important in terms of providing a detailed understanding of the variety of outcomes induced by ionizing radiation.
One of the intriguing tasks potentially being solved by combining the experimental measurements with simulation techniques is the activation of specific DSB pathways following low-dose radiation exposure. Currently, there are many works devoted to changes in the number of DNA damage foci present in mammalian cells irradiated at low doses [19,20,21,22]. However, the issue of DSB repair efficiency after low-dose radiation exposure remains one of the controversial topics of present-day radiation biology.
The current study aims to perform the experimental probing of the relative contribution of the HR pathway to DSB repair, which is induced via X-ray exposure in the dose range from 20 to 1000 mGy, with the subsequent numerical evaluation of γ-H2AX foci considered to be the main DSB repair marker.

## 2. Materials and Methods2.1. Experimental Study2.1.1. Cell CultureThe studies were performed using a human skin fibroblast culture (Cell Applications, San Diego, CA, USA, Cat.no. 106K-05a). Cells were

## 2. Materials and Methods

## 2.1. Experimental Study2.1.1. Cell CultureThe studies were performed using a human skin fibroblast culture (Cell Applications, San Diego, CA, USA, Cat.no. 106K-05a). Cells were cultured at 37 °C and 5

## 2.1. Experimental Study

## 2.1.1. Cell CultureThe studies were performed using a human skin fibroblast culture (Cell Applications, San Diego, CA, USA, Cat.no. 106K-05a). Cells were cultured at 37 °C and 5% CO2 in a standard DME

## 2.1.1. Cell Culture
The studies were performed using a human skin fibroblast culture (Cell Applications, San Diego, CA, USA, Cat.no. 106K-05a). Cells were cultured at 37 °C and 5% CO2 in a standard DMEM culture medium with a high glucose content (4.5 g/L) (Thermo Fisher Scientific, Waltham, MA, USA) supplemented with 2 mmol/L of L-glutamine (Thermo Fisher Scientific, Waltham, MA, USA), 100 U/mL of penicillin, 100 μg/mL of streptomycin (Thermo Fisher Scientific, Waltham, MA, USA) and 10% fetal bovine serum (Thermo Fisher Scientific, Waltham, MA, USA). Fibroblasts were then plated on 4-centimeter-squared coverslips in 35-millimeter Petri dishes (SPL Lifesciences, Pocheon-City, Gyeonggi-Do, Republic of Korea) with a density of 104 cells/cm2. Next, 3–5 passages of cells in the phase of exponential growth (cell population density ~60–70%) were used to perform the experiments.

## 2.1.2. IrradiationThe cells were irradiated using the RUB RUST-M1 X-irradiator (Diagnostika-M LLC, Moscow, Russia), which was equipped with two X-ray emitters, at a dose rate of 40 mGy/min and voltage

## 2.1.2. Irradiation
The cells were irradiated using the RUB RUST-M1 X-irradiator (Diagnostika-M LLC, Moscow, Russia), which was equipped with two X-ray emitters, at a dose rate of 40 mGy/min and voltage of 100 kV, current of 0.8 mA, using a 1.5-millimeter Al filter and at a temperature of 4 °C (LAB ARMOR BEADS thermal granules were used for cooling). The error in the exposure dose was estimated to be within 15%. After irradiation, cells were incubated under the standard conditions of a CO2 incubator (37 °C, 5% CO2) for 0.25–24 h.

## 2.1.3. ImmunocytochemistryCells were fixed on coverslips in 4% paraformaldehyde in PBS (pH 7.4) for 15 min at room temperature, followed by two PBS rinses (pH 7.4) and permeabilization in 0.3% Triton-

## 2.1.3. Immunocytochemistry
Cells were fixed on coverslips in 4% paraformaldehyde in PBS (pH 7.4) for 15 min at room temperature, followed by two PBS rinses (pH 7.4) and permeabilization in 0.3% Triton-X100 (in PBS, pH 7.4) supplemented with 2% bovine serum albumin (BSA) to block non-specific antibody binding. To perform immunocytochemical staining, the slides were incubated for 1 h at room temperature with a primary mouse monoclonal antibody against γH2AX (dilution 1: 200, 05-636-I clone JBW301, Merck-Millipore, Burlington, VT, USA) and rabbit polyclonal antibody against Rad51 (dilution 1:200, ABE257, Merck-Millipore, Burlington, VT, USA) or CENPF (dilution dilution 1:200, ab5, Abcam, Waltham, MA, USA) in PBS (pH 7.4) containing 1% BSA. After rinses with PBS, cells were incubated for 1 h at room temperature with the goat anti-mouse Alexa Fluor 488 conjugated secondary antibodies IgG (H + L) (Life Technologies, Carlsbad, SA, USA), with a dilution of 1: 600 and goat anti-rabbit rhodamine conjugated antibodies (Merck-Millipore, Burlington, VT, USA), with a dilution of 1:400 in PBS (pH 7.4) with 1% BSA. ProLong Gold medium (Life Technologies, Carlsbad, SA, USA) was used with DAPI to perform DNA counter-staining and for the prevention of photo fading. Cells were viewed and imaged using a Nikon Eclipse Ni-U microscope (Nikon, Tokyo, Japan) equipped with a high definition ProgRes MFcool camera (Jenoptik AG, Jena, Germany). The filter sets UV-2E/C (340–380-nanometer excitation and 435–485-nanometer emission), B-2E/C (465–495-nanometer excitation and 515–555-nanometer emission) and Y-2E/C (540–580-nanometer excitation and 600–660-nanometer emission) were used. At least 200 cells were analyzed to determine each data point. γ-H2AX and Rad51 foci were counted through manual scoring and using DARFI software (https://github.com/varnivey/darfi; accessed on 19 September 2016).

## 2.1.4. Statistical AnalysisStatistical analysis of the data was conducted using the Statistica 8.0 software (StatSoft, Tulsa, OK, USA). The results were presented as the means of three independent exp

## 2.1.4. Statistical Analysis
Statistical analysis of the data was conducted using the Statistica 8.0 software (StatSoft, Tulsa, OK, USA). The results were presented as the means of three independent experiments ± standard error (SE).

## 2.2. Evaluating the Percentage Contribution of HR to DSB RepairIn order to evaluate the percentage contribution of HR to the repair process, the quantitative model of radiation-induced DSB repair was 

## 2.2. Evaluating the Percentage Contribution of HR to DSB Repair
In order to evaluate the percentage contribution of HR to the repair process, the quantitative model of radiation-induced DSB repair was used [23]. The model consisted of five main parts. The first part evaluated the initial yield of radiation-induced DSBs. The other parts were the quantitative models of NHEJ, HR, SSA and Alt-EJ repair pathways, as shown in Figure 1. To simulate the processing of DNA lesions by repair enzymes, the mass-action chemical kinetics approach was used.
Figure 1
Pathways for DSB repair in mammalian and human cells.
Pathways for DSB repair in mammalian and human cells.
The kinetics of DSB induction and repair were simulated as follows:
(1)
where N0 = NncDSB + NcDSB; VNHEJ, VHR, VSSA, Vmicro-SSA, and VAlt-EJ are the terms characterizing the elimination of DSBs by the NHEJ, HR, SSA, micro-SSA, and Alt-EJ repair pathways, respectively. The details of these terms are given in Equation (A4) of Appendix B. In Equation (1), Nir is the fraction of irreparable DSBs, which corresponds to the level of γ-H2AX foci remaining in the cell 24 h post-irradiation. The rate of initial DSB induction was calculated as dN0/dt=α(L)dD/dt, using the same method that is used in [24,25,26]. Here, D is the dose of ionizing radiation (Gy), and α(L) is the slope coefficient of linear dose dependence, which describes the DSB induction per unit of dose (Gy−1 per cell).
Enzymatic interactions that occurred in the course of repair were simulated as follows: within the NHEJ pathway, the stage of Ku binding to a DSB was represented by the kinetic equation below
(2)
where quantities in brackets denote time-dependent intracellular concentrations of repair complexes, and K values with an appropriate subscript are used to represent the dimensional reaction rate-constants. Here, [DSB] is the number of DSBs that undergo binding by Ku, and [DSB•Ku] is the level of the resulting intermediate complex.
The stage of the recruitment of the DNA-dependent protein kinase catalytic subunit (DNA-PKcs) and Artemis to a DSB site was described as
(3)
In this kinetic equation, [DNA-PK] denotes a complex of Ku and DNA-PKcs. Art indicates that the mentioned intermediate complex is formed in the presence of Artemis.
The autophosphorylation of DNA-PKcs was represented by
(4)
where the superscript P defines the phosphorylated DNA-PK product.
The subsequent end-bridging process was described as a junction of two [DSBNHEJ•DNA-PKArtP] constructs formed at the previous repair stage.
(5)
Here, the [Bridge] intermediate complex characterizes the final product of the reaction.
The further assembly of the NHEJ repair complex promotes the recruitment of LigIV with its associated factors XRCC4 and XLF, as well as the subsequent involvement of the polynucleotide kinase phosphatase (PNKP) with a break site.
(6)
(7)
The final step of the NHEJ pathway implying the recruitment of a polymerase was denoted as follows:
(8)
In this consideration, after gap filling and ligation are finalized, it was accepted that the repair complexes dissociated, leaving the recovered double-stranded DNA (dsDNA).
The first stages of HR associated with the action of MRN, its co-factors (CtlP, ExoI, Dna2) and ATM were described in the model as follows:
(9)
(10)
(11)
where the MRN (Mre11-Rad50-Nbs1) complex interacting with other repair factors is considered to be a single complex, and superscript P defines the phosphorylated species.
The involvement of the replication protein A (RPA) in eliminating the secondary structure of DNA and protecting single-stranded regions from other enzymatic activities was denoted by
(12)
The next HR step associated with formation of Rad51 filament was described via the following kinetic equation:
(13)
where the Rad51par abbreviation denotes five biologically important Rad51 paralogs (Rad51B, Rad51C, Rad51D, XRCC2 and XRCC3), and [Rad51 filament] defines the [ssDNA•Rad51-Rad51par-BRCA2] complex.
The formation of a displacement loop (D-loop) and two methods of its subsequent resolution were represented as follows:
(14)
(15)
(16)
where [DNAinc] is the incoming DNA duplex, [Rad51 filament•DNAinc] complex is assumed to contain Rad54 protein, and dHJ is the double Holiday junction.
The SSA pathway was given as the below set of kinetics equations. The first step assuming interaction with Rad52 was denoted by
(17)
where the [ssDNA•RPA]  complex is the same as that shown in Equation (12).
The junction between Rad52 heptamer rings and each ssDNA termini that allowed the formation of a flapped structure is represented as follows:
(18)
The cutting of the flapped ends by the ERCC1-XPF endonuclease and final ligation of a damaged site with LigIII complex were simulated via
(19)
(20)
Here, Rad52 and ERCC1-XPF are assumed to dissociate from the processing site.
The simulation of the alternative end-joining pathways was based on the hypothesis suggesting two different Ku-independent repair mechanisms [27]. The first of these mechanisms was represented by MMEJ, which was sometimes considered to be an independent end-joining mechanism distinct from the other pathways. Meanwhile, experimental evidence suggested that this type of repair represented a specific subclass of the SSA pathway known as micro-SSA [28,29]. On the basis of these considerations, in our model, rejoining via MMEJ was simulated as the additional part of DSBs, which followed the SSA pathway.
To simulate the Alt-EJ pathway, an additional mechanistic explanation was proposed. According to the recent hypothesis, Alt-EJ required activity of MRX complex and possibly exhibited the same initiation steps as HR [27]. Therefore, the initial stages of Alt-EJ was described by Equations (9)–(11). After the production of ssDNA, the activity of PARP1 recruited to the DSB site was characterized by Equation (21).
(21)
The kinetics of microhomology production via polymerase activity was simulated via
(22)
(23)
In Equation (23), [MicroHomol] denotes the yield of microhomology.
The final step of Alt-EJ was believed to rely on LigI activity [27]. In the model, this stage was represented as follows:
(24)
The kinetics of the induction of γ-H2AX foci was simulated by summing up all active forms of DNA-PKcs and ATM, which were considered in the model, which was similar to the method used in [24]
(25)
where [H2AX] is the level of the histone variant H2AX and
(26)
The mechanism of γ-H2AX foci dephosphorylation was assumed to be proportional to the amount of repaired DNA, as well as its spontaneous decay with the corresponding rate constants K11 and K12.
(27)
To describe the interactions between repair enzymes and their substrates, the mass-action chemical kinetics approach was used. The details of the application of this approach to simulate the dynamic change in the intracellular concentrations of main repair complexes, as well as the model equations and their parameters, are described in Appendix A, Appendix B, Appendix C.
The evaluation of the percentage contribution of HR to DSB repair was performed via the calculated time-courses of γ-H2AX and Rad51 foci for the particular dose of X-rays. The HR contribution to PHR was evaluated as the following ratio:
(28)
where y9¯ and x14¯ are the mean numbers of Rad51 and γ-H2AX foci, respectively, counted via a 24-h simulation period.
To obtain a dependence of PHR on the X-ray dose, the ODE system was run using a sufficiently small dose step equal to 0.1 mGy within the range 0–1000 mGy. This simulation procedure yielded a curve of PHR (D) dependence that was expressed by the following formula:
(29)

## 3. Results3.1. Experimental ResultsIn Figure 2, γ-H2AX foci yields are shown, as scored at 0.25–24 h after exposure to different doses of X-rays ranging from 20 to 1000 mGy. Foci yields scored in cell

## 3. Results

## 3.1. Experimental ResultsIn Figure 2, γ-H2AX foci yields are shown, as scored at 0.25–24 h after exposure to different doses of X-rays ranging from 20 to 1000 mGy. Foci yields scored in cells exposed 

## 3.1. Experimental Results
In Figure 2, γ-H2AX foci yields are shown, as scored at 0.25–24 h after exposure to different doses of X-rays ranging from 20 to 1000 mGy. Foci yields scored in cells exposed to 500 mGy and 1000 mGy tend to peak at 0.25–1.0 h, while exposure to doses of 20–250 mGy resulted in maximum levels of foci being found at 0.25–2.0 h. At a point closer to 4 h after exposure, the signal of γ-H2AX sharply decreased with time due to the completion of the fast DSB repair being a feature of NHEJ. Then, up to 24 h after exposure, the slow DSB repair occurred, which was typically associated with complex DSBs being repaired via the HR pathway.
Figure 2
Experimentally measured time-courses of γ-H2AX foci remaining in normal human skin fibroblasts after exposure to (a) 20 mGy, 40 mGy, or 80 mGy and (b) 160 mGy, 250 mGy, 500 mGy or 1000 mGy of X-rays in comparison to background levels used as control (±SE).
Experimentally measured time-courses of γ-H2AX foci remaining in normal human skin fibroblasts after exposure to (a) 20 mGy, 40 mGy, or 80 mGy and (b) 160 mGy, 250 mGy, 500 mGy or 1000 mGy of X-rays in comparison to background levels used as control (±SE).
It is noteworthy that 24 h after exposure to 40–80 mGy, the level of γ-H2AX foci does not drop to the control values, indicating a slowdown in the DSB repair kinetics following low doses of ionizing radiation. On the other hand, 24 h after exposure to 500 mGy and 1000 mGy, the observed levels of γ-H2AX foci were slightly below those of the control values. A possible explanation is that the exposure to low and moderate doses of ionizing radiation affects cell proliferation in an opposite manner. Low doses stimulate cell proliferation, while relatively high doses lead to their reduction.
One of the sources of DNA DSBs used in the proliferation of cells is the collapse of replication forks in the S phase of the cell cycle [30]. The repair of DSBs induced in this process follows the HR pathway [30,31]. The histone H2AX in the S phase is mainly phosphorylated by the ATR kinase [32,33]. As a consequence, the percentage of cells in the S phase contributes to the average amount of γ-H2AX foci in asynchronous cell populations. This process leads to the overestimation of the γ-H2AX foci level in cells exposed to low doses and the underestimation of its presence in cells irradiated with moderate doses. The observed pattern generally meets the previous findings obtained using human fibroblasts and mesenchymal stromal cells exposed to X-rays [34,35].
To estimate the contribution of HR to the entire process of DNA DSB repair, we analyzed changes in the level of radiation-induced Rad51 foci, which are the key markers of HR (Figure 3). A statistically significant increase in the number of Rad51 foci was observed 2 h after irradiation, reaching its maximum values by 6 h. After 6 h, a decrease in the number of Rad51 foci was indicated. Finally, at 24 h after irradiation, the level of foci dropped down to the control values in cells exposed to 160–1000 mGy and remained higher than the control values in cells irradiated with doses of 40 mGy and 80 mGy.
Figure 3
Experimentally measured time-courses of Rad51 foci remaining in normal human skin fibroblasts after exposure to (a) 20 mGy, 40 mGy or 80 mGy and (b) 160 mGy, 250 mGy 500 mGy or 1000 mGy of X-rays in comparison to background levels used as control (±SE).
Experimentally measured time-courses of Rad51 foci remaining in normal human skin fibroblasts after exposure to (a) 20 mGy, 40 mGy or 80 mGy and (b) 160 mGy, 250 mGy 500 mGy or 1000 mGy of X-rays in comparison to background levels used as control (±SE).
Figure 4 illustrates RAD51 and γ-H2AX foci and the co-localization of RAD51 foci with γ-H2AX foci in normal human skin fibroblasts at 6 h (maximum values of RAD51 foci) after X-ray irradiation with doses of 80, 250, and 1000 mGy. Dose-dependent increases in the number of foci of both proteins, as well as a perfect co-localization of RAD51 foci with γ-H2AX foci, are clearly seen on the microscopic images shown in Figure 4.
Figure 4
Representative images of RAD51 and γ-H2AX foci and their co-localization at 6 h post-irradiation. Fibroblasts were irradiated, and RAD51 and γ-H2AX were immunofluorescently labeled as described in Materials and Methods section. Nuclei were counter-stained with DAPI, as shown in blue in first column of images. RAD51 and γ-H2AX foci are shown in green and red, respectively. Images in the last column were produced by merging all three channels, and they show the co-localization patterns of RAD51 and γ-H2AX.
Representative images of RAD51 and γ-H2AX foci and their co-localization at 6 h post-irradiation. Fibroblasts were irradiated, and RAD51 and γ-H2AX were immunofluorescently labeled as described in Materials and Methods section. Nuclei were counter-stained with DAPI, as shown in blue in first column of images. RAD51 and γ-H2AX foci are shown in green and red, respectively. Images in the last column were produced by merging all three channels, and they show the co-localization patterns of RAD51 and γ-H2AX.

## 3.2. Percent Contribution of HR to DSB RepairTo confirm the DSB repair model validity of radiation doses in the range of 20–1000 mGy, the calculated time-courses of γ-H2AX and Rad51 foci were compared

## 3.2. Percent Contribution of HR to DSB Repair
To confirm the DSB repair model validity of radiation doses in the range of 20–1000 mGy, the calculated time-courses of γ-H2AX and Rad51 foci were compared to the experimental data of normal human skin fibroblasts exposed to X-rays at doses of 20, 40, 80, 160, 250, 500 and 1000 mGy. The results of comparison are shown in Figure 5 and Figure 6, which depict kinetics of these foci in the range 0–24 h after irradiation.
Figure 5
Time-courses of γ-H2AX foci remaining in normal human skin fibroblasts after exposure to different doses of X-rays. The curves are the calculated results; the symbols are the experimental data (±SE). The data are normalized based on the maximum number of foci observed within the 24-h period.
Time-courses of γ-H2AX foci remaining in normal human skin fibroblasts after exposure to different doses of X-rays. The curves are the calculated results; the symbols are the experimental data (±SE). The data are normalized based on the maximum number of foci observed within the 24-h period.
Figure 6
Time-courses of Rad-51 foci remaining in normal human skin fibroblasts after exposure to different doses of X-rays. The curves are the calculated results; the symbols are the experimental data (±SE). The data are normalized based on maximum number of foci observed within the 24-h period.
Time-courses of Rad-51 foci remaining in normal human skin fibroblasts after exposure to different doses of X-rays. The curves are the calculated results; the symbols are the experimental data (±SE). The data are normalized based on maximum number of foci observed within the 24-h period.
Although the exposure to doses of 20–250 mGy results in relatively low absolute levels of γ-H2AX, the entire repair process does not seem to occur faster than in the case of higher considered doses. The proportion of γ-H2AX foci observed after exposure to 20–250 mGy remains elevated for a period similarly long to that following the exposure to the doses of 500–1000 mGy. We hypothesize that the observed pattern of DSB repair occurs due to the preferential activation of HR pathway, which takes longer to eliminate the damage.
Interestingly, following the exposure to doses of 160 mGy and above, the levels of γ-H2AX foci remaining 24 h after irradiation were lower than the background value. This finding suggests that DSBs normally induced as a consequence of non-radiation factors can undergo a more effective elimination if cells enter the process of radiation-induced DSB repair. It could also be expected that in cells that have successfully completed the repair of a certain portion of radiation-induced DSBs, the background levels of γ-H2AX foci can be suppressed compared to non-irradiated cells for at least a residual period after exposure.
Overall, the juxtaposition of the simulated and experimentally measured data affirms the validity of the suggested DSB repair model used for relatively low radiation doses, enabling the calculation of time-courses of γ-H2AX and Rad51 foci within the full dose range of interest (0–1000 mGy) to obtain a continuous dependence of PHR on D.
The results yielding the percentage contribution of HR to DSB repair are shown in Figure 7. The general pattern of HR involvement in the DSB repair is characterized by a near-exponentially decreasing function, which is supposed to depend on the cell line, type of ionizing radiation and other factors. The dependence of HR on different factors requires more detailed examination.
Figure 7
Dependence of the percentage contribution of HR to DSB repair on the radiation dose (PHR(D)). The curve line is fitted; the symbols are the experimental data.
Dependence of the percentage contribution of HR to DSB repair on the radiation dose (PHR(D)). The curve line is fitted; the symbols are the experimental data.

## 3.3. Dose-Dependent Changes in the S/G2-Phase Cell FractionsDNA repair via HR predominantly occurs in the S/G2 phases of the cell cycle. Therefore, to ensure the correct interpretation of the obtained

## 3.3. Dose-Dependent Changes in the S/G2-Phase Cell Fractions
DNA repair via HR predominantly occurs in the S/G2 phases of the cell cycle. Therefore, to ensure the correct interpretation of the obtained results, it was important to estimate the changes in the proportion of cells in the S/G2 phases in the irradiated cell populations. For this purpose, we used immunohistochemical analysis of a protein marker of cells in S/G2 phases—Centromere protein F (CENPF). This protein, being a component of the nuclear matrix during G2 phase, has been used as a marker of S/G2 cells [36,37]. Its synthesis commences in the early S phase and ceases in the M phase, with a peak at the G2 phase [37].
The results presented in Figure 8 show that exposure to low doses (20–80 mGy) of X-rays leads to a slight increase in the proportion of CENPF-positive cells. However, these changes are not statistically significant (p > 0.05). In contrast, irradiation at doses of 250, 500 and 1000 mGy leads to significant 2.15 (p = 0.004), 3.69 (p = 0.0003) and 6.93 (p = 0.0002) fold decreases in the proportion of CENPF positive cells, respectively. In general, after irradiation at doses of 160–1000 mGy, the pattern of change in the proportions of S/G2-phase fibroblasts is characterized by a near-exponentially decreasing function. The obtained results are in good agreement with dose-dependent changes in the relative contribution of HR in irradiated cells.
Figure 8
Dose-dependent changes in the S/G2-phase cell fractions (CENPF positive cells) 24 h after the irradiation of fibroblasts. Data are means ± SE of the three independent experiments.
Dose-dependent changes in the S/G2-phase cell fractions (CENPF positive cells) 24 h after the irradiation of fibroblasts. Data are means ± SE of the three independent experiments.

## 4. DiscussionOur study reveals distinct patterns of γ-H2AX and Rad51 foci dynamics following the application of low and moderate doses of X-rays. We identified several parameters of the foci dynamics,

## 4. Discussion
Our study reveals distinct patterns of γ-H2AX and Rad51 foci dynamics following the application of low and moderate doses of X-rays. We identified several parameters of the foci dynamics, which demonstrate different regularities in response to low and moderate doses, including periods of reaching peak levels of γ-H2AX foci, numbers of γ-H2AX and Rad51 foci remaining 24 h post-irradiation compared to control levels. All of these characteristics of DNA DSB repair demonstrate a pronounced dose-dependent shift. Within the dose steps selected for use in the analysis, the dose-dependent shift associated with reaching peak levels of γ-H2AX foci is observed between 250 and 500 mGy. The doses triggering the levels of remaining γ-H2AX and Rad51 foci appeared to be within the ranges of 80—500 mGy and of 80—160 mGy, respectively.
The juxtaposition of our results with other findings [38] suggests another confirmation of a dose-dependent shift in the activity of DNA repair systems, at least with regard to the repair of radiation-induced DSBs. On one hand, the number of DSBs increases linearly with the radiation dose, and the entire cell response depends on the correctness of DNA repair. Our results show that relatively low doses of low-LET ionizing radiation lead to a higher contribution of the error-free repair via the HR pathway. Since HR takes longer than NHEJ, low-dose-mediated activation of DNA repair mechanisms may not only protect DNA from the immediate damage, but also result in prolonged adaptive responses, protecting the cell from future oxidative insults (such as high-dose radiation), as is confirmed in [38,39,40,41,42,43,44]. The observed shift to error-free HR allows the restoration of the genome with maximum fidelity.
The mechanistic nature of the relative contribution of HR at low doses remains under debate. Nevertheless, our results support one of the possible scenarios of engagement of this repair pathway in the response to low doses of low-LET ionizing radiation [45]. According to these findings, error-prone pathways, including NHEJ, Alt-EJ and SSA, are partly or completely suppressed and likely only operate when HR fails to process the damage. An increase in the dose of low-LET radiation leads to the suppression of HR via mechanisms that remain to be identified, while the contribution of NHEJ increases and becomes the first choice. The decrease in the fraction of cells in the S/G2 phases after irradiation at doses of 250–1000 mGy, as shown in our work, suggests that the simplest mechanism used to reduce the contribution of HR with increasing radiation dose is the cell cycle arrest in G1/S phase. It is believed that HR is primarily active in the S/G2 phase of the cell cycle, as HR requires a sister chromatid to perform template-based repair [46,47,48]. Thus, a simple mechanistic decrease in the portion of S/G2 cells should also lead to a decrease in the relative HR contribution to DNA DSB repair. However, to prove this assumption, additional research is needed to address the role played by HR proteins in cell cycle regulation, including the analysis of this regulation in low-dose radiation-exposed cells. To determine if the HR contribution in DNA DSB repair is directly affected by radiation doses, the analysis should be restricted to S/G2 cells. The overall strategy for the future research in this direction should elucidate whether the proportion of the cells with the cell cycle arrest is really comparable to the proportion of cells in which the direct effect of radiation on the HR-capacity is seen. Our study was limited to a radiation dose of 1 Gy, while the model in [45] postulates that DNA end resection remains active, showing signs of suppression only above 20 Gy. Therefore, the increased engagement of error-prone Alt-EJ and SSA under conditions of persisting resection and partially suppressed HR can only be identified through the simulation approach.
Considering that there are plenty of well-established findings regarding the strong compensatory power of the DBS repair in eukaryotes, it is incorrect to assume that the radiation effects associated with the DSB removal follow linear dose dependence. Even the mechanistic nature of the assembly of DSB repair super-complexes in response to the appearance of radiation-induced lesions reflects the non-linear kinetics of this process, which may blur the resulting outcome within a certain dose range. It may also suggest that genotoxicity and late risks associated with the quality of DSB repair after exposure to low-LET radiation can cross some radiation dose threshold.

## AcknowledgmentsThe authors would like to thank Daria Molodtsova for her help with preparing and editing the manuscript.

## Acknowledgments
The authors would like to thank Daria Molodtsova for her help with preparing and editing the manuscript.

## Appendix A. Details the DSB Repair ModelThe initial yield of DSBs, denoted as (N0), was calculated as
(A1)dN0dt=α(L)dDdt,
where D is the radiation dose (Gy), and α(L)=aexp(−bL) is the slope coefficien

## Appendix A. Details the DSB Repair Model
The initial yield of DSBs, denoted as (N0), was calculated as
(A1)
where D is the radiation dose (Gy), and α(L)=aexp(−bL) is the slope coefficient of linear dose dependence, which describes DSB induction per unit of dose (Gy−1 per cell). Parameters a and b used in this equation are presented in Appendix C. The particular details of parameter evaluation, as well as the simulation of each repair pathway, can be found in [23].
The dynamic change in the intracellular concentrations of the main repair complexes is expressed via the following differential equation:
(A2)
where Xi (i=1,…,n) is the intracellular level of the i-th repair complex, t is time, and the functions V+ and V− are the complex accumulation and degradation, respectively. The dimensionless form of the system of ordinary differential equations (ODE) referred to the simulation of NHEJ, HR, SSA and two alternative repair pathways, as well as its parameters and initial conditions, which are presented in Appendix B, Appendix C. In the present study, the ODE system was solved using the fourth-order Runge–Kutta method. The integration time-step is denoted as 10−10 s in order to satisfy the fastest reactions being simulated in the model.
In order to simulate DSB rejoining in the asynchronous cell culture, we set a model cell cycle distribution similar to the distribution of HF19 cells observed in [49], where 40% of cells were in G0/G1, <10% were in S phase and 50% were in G2/M. Assuming that S-phase cells include two equal sub-fractions of early S and late S cells, the final distribution was set as follows: 45% of cells are in the G0/G1 and early S phases, and 55% of cells are in the late S and G2/M phases. Based on the data discussed in [26,28,50,51], the model provides the following pathways for the repair of non-clustered and clustered DSBs: In G0/G1 and early S phases, non-clustered DSBs are likely to follow rejoining via NHEJ, while the limited number of complex DSBs may undergo PARP1-dependent Alt-EJ. The other pathways are assumed to be unavailable or masked by NHEJ in these phases. In the late S and G2/M phases, non-clustered DSBs may follow NHEJ and be a substrate for SSA and micro-SSA pathways. The clustered DSBs are suggested to proceed through HR, SSA and Alt-EJ. Finally, in our calculations, the models of corresponding repair mechanisms are processed based on the following scheme:
(A3)
where 0.45 and 0.55 represent the fractions of cells in the G0/G1 and early S, as well as in the late S and G2/M, phases, respectively; NncDSB and NcDSB represent amounts of non-clustered and clustered DSBs; and T represents the total size of the exponentially growing cell culture set to be 105 cells, as mentioned in [49]. The model accounts for the cell cycle dependence of the repair pathways by initiating the computation procedure with the levels of NncDSB and NcDSB parameters based on the cell cycle distribution of the cell culture used in the experiment.

## Appendix B. Equations of the ModelThe dynamic change in the levels of NHEJ repair complexes and γ-H2AX foci is described by the following system of ordinary differential equations:(A4)dn0dτ=α(L)dDdtNi

## Appendix B. Equations of the Model
The dynamic change in the levels of NHEJ repair complexes and γ-H2AX foci is described by the following system of ordinary differential equations:
(A4)
The initial conditions of this system of wild-type cells are as follows: n0(0) = α(L)D, x2(0) = x4(0) = x5(0) = x6(0) = x8(0) = x10(0) = x12(0) = x13(0) = x14(0) = 0. The values of variables x1, x3, x7, x9, x11 and x15 are set to be constant and equal to x1.
In Equation (A4), n0 is the scaled number of radiation-induced DBSs; Nir is the non-dimensional fraction of irreparable DSBs; x1, x3, x7, x9 and x11 are scaled intracellular concentrations of the Ku, DNA-PKcs, LigIV-XRCC4-XLF, PNK and Pol enzymes, respectively; x2, x4, x5, x6, x8, x10, x12 and x13, are normalized intracellular concentrations of intermediate complexes represented by [DSB•Ku], [DSB•DNA-PKArt], [DSB•DNA-PKArtP], [Bridge], [Bridge•LigIV-XRCC4-XLF], [Bridge•LigIV-XRCC4-XLF•PNKP], [Bridge•LigIV-XRCC4-XLF•PNKP•Pol] and [dsDNA]; x14, x15 and y5 are the scaled levels of the γ-H2AX foci, histone variant H2AX and [DSB•MRN-CtIP-ExoI-Dna2•ATMP] complex that contribute to the fluorescent signal upon the measurement of γ-H2AX foci induction; y15, z8 and w5 are the concentrations of the [dHJ], [dsDNAnicks•LigIII] and [MicroHomol•LigI], respectively; and ki is the scaled rate constants. The variables of the model are normalized based on Ku total cellular level: n0=N0/X1, xi=Xi/X1, yi=Yi/X1, zi=Zi/X1 and wi=Wi/X1. In terms of molar concentration, this level was estimated as X1=N/(NAVnucl)=9.19×10−7M, where N = 400 000 is the number of Ku molecules per cell [52], NA is the Avogadro constant and Vnucl=7.23×10−13 L is an average volume of the cell nucleus in human fibroblasts [53]. In this consideration, x1 = 1.
The kinetics of the HR repair complexes is described by the following system of ordinary differential equations:
(A5)
The initial conditions of this system for wild-type cells are as follows: y2(0) = y4(0) = y5(0) = y6(0) = y8(0) = y10(0) = y11(0) = y13(0) = y14(0) = y15(0) = 0. The values of y1, y3, y7, y9 and y12 variables are set to be constant and equal to x1.
In Equation (A5), y1, y3, y4, y7 and y9 are scaled intracellular concentrations of the MRN, ATM, ATMP, RPA and Rad51-Rad51par-BRCA2 complexes, respectively; y12 is the normalized level of incoming homologous sequence designated as [DNAinc]; y2, y5, y6, y8, y10, y11, y13, y14 and y15 are the normalized intracellular concentrations of the [DSB•MRN-CtIP-ExoI-Dna2], [DSB•MRN-CtIP-ExoI-Dna2•ATMP], [ssDNA], [ssDNA•RPA], [ssDNA•RPA•Rad51-Rad51par-BRCA2], [Rad51 filament], [Rad51 filament•DNAinc], [D-loop] and [dHJ] intermediate complexes, respectively; and pi are scaled rate constants. The variables are also normalized based on the Ku total cellular level as yi=Yi/X1.
The dimensionless forms of the equations used in the SSA model are represented as follows:
(A6)
The initial conditions of this system for wild-type cells are as follows: z2(0) = z3(0) = z5(0) = z6(0) = z8(0) = 0. The values of variables z1, z4 and z7 are set to be constant and equal to x1.
In Equation (A6), z1, z4 and z7 are scaled cellular levels of Rad52, ERCC1-XPF and LigIII enzymes, respectively; z2, z3, z5, z6 and z8 are scaled intracellular concentrations of the [ssDNA•RPA•Rad52], [Flap], [Flap•ERCC1-XPF], [dsDNAnicks] and [dsDNAnicks• LigIII]  intermediate complexes, respectively; and qi is the scaled rate constants. The variables are also normalized based on Ku total cellular level as zi=Zi/X1.
The kinetics of the Alt-EJ intermediate complexes is described by the following system of ordinary differential equations:
(A7)
The initial conditions of this system for wild-type cells are as follows: w2(0) = w4(0) = w5(0) = w7(0) = 0. The values of w1, w3 and w6 variables are set to be constant and equal to x1.
In Equation (A4), w1, w3 and w6 are scaled cellular levels of PARP1, Pol and LigI, respectively; w2, w4, w5 and w7 are scaled intracellular concentrations of the [ssDNA•PARP1] , [ssDNA•Pol] , [MicroHomol] and [MicroHomol•LigI] intermediate complexes, respectively; and ri is the scaled rate constants. The variables are also normalized based on Ku total cellular level as wi=Wi/X1.

## Appendix C. Parameters of the ModelThe dimensionless parameters of Equation (A4) are k1=K1X1/K8, k−1=K−1/K8, k2=K2X1/K8, k−2=K−2/K8, k3=K3/K8, k4=K4X1/K8, k−4=K−4/K8, k5=K5X1/K8, k−5=K−5/K8, k6=K6X1/K

## Appendix C. Parameters of the Model
The dimensionless parameters of Equation (A4) are k1=K1X1/K8, k−1=K−1/K8, k2=K2X1/K8, k−2=K−2/K8, k3=K3/K8, k4=K4X1/K8, k−4=K−4/K8, k5=K5X1/K8, k−5=K−5/K8, k6=K6X1/K8, k−6=K−6/K8, k7=K7X1/K8, k−7=K−7/K8, k8=K8/K8=1, k9=K9/K8, k10=K10/X1, k11=K11/K8 and k12=K12/K8. K8 is the rate of final NHEJ process resulting in the production of the repaired dsDNA and the unwinding of all repair factors. The reason for the selection of this constant as a scaling factor is the assumed independence of this parameter on possible variations due to the competition of repair pathways at earlier stages. This assumption is mainly important in terms of performing future modifications to the model, when rate constants of early stages are planned to connect with the damage complexity.
The scaled reaction rates in Equation (A5) are p1=P1X1/K8, p−1=P−1/K8, p2=P2/K8, p3=P3X1/K8, p−3=P−3/K8, p4=P4/K8, p5=P5X1/K8, p−5=P−5/K8, p6=P6X1/K8, p−6=P−6/K8, p7=P7/K8, p8=P8X1/K8, p−8=P−8/K8, p9=X1/K8, p10=P10/K8, p11=P11/K8 and p12=P12/K8. The scaling factors X1 and K8 are chosen to perform parameter normalization.
The scaled reaction rates in Equation (A6) are q1=Q1X1/K8, q−1=Q−1/K8, q2=Q2X1/K8, q3=Q3X1/K8, q−3=Q−3/K8, q4=Q4/K8, q5=Q5X1/K8, q−5=Q−5/K8 and q6=Q6/K8. In this case, the same factors X1 and K8 are used for scaling rate constants.
The scaled reaction rates in Equation (A7) are r1=R1X1/K8, r−1=R−1/K8, r2=R2X1/K8, r3=R3/K8, and r4=R4X1/K8, r−4=R−4/K8 and r5=R5/K8. As in the other models, the same scaling factors X1 and K8 are chosen to perform parameter normalization.
The majority of the rate constants of enzymatic reactions were determined by fitting the corresponding model curves produced using Equations (A4)–(A7) to the experimental data regarding the kinetics of different stages of DSB repair. Other parameters characterizing the regularities of DSB induction were directly obtained from experimental measurements reviewed in the literature. For some of the parameters used, a dependence of their values on radiation dose is introduced. The functions representing these parameters are also shown in Table A1.
In order to estimate α(L), we used three sets of experimental data regarding DSB induction in GM38 and GM57 lines of human skin fibroblasts within the LET values ranging from 0.2 to 440 keV/µm [54,55,56]. The total DSB yield measured in these studies as Gy−1 per 109 bp was recalculated to Gy−1 per cell, taking into account the fact that a diploid human cell in G1 phase contains about 5 × 109 bp of DNA [54]. The experimental data were approximated using the exponential function α(L)=aexp(−bL) to obtain a continuous function within the stated LET range. The parameters of the function given in Table A1 were evaluated by adjusting the curve for α(L) to fit the results of the above-mentioned experimental measurements.
Table A1
Parameters of the model.
Parameters of the model.
Parameter
Value
Parameter
Value
a
27.5
P
−5
8.82 × 10−5 h−1
b
2.43 × 10−3
P
6
1.87 × 105 M−1 h−1
K
1
11.05 M−1 h−1
P
−6
1.55 × 10−3 h−1
K
−1
6.6×10−4 h−1
P
7
21.36 h−1
K
2
18.83×(1.09−e−21.42/D1.82) M−1 h−1
P
8
1.20 × 104 M−1 h−1
K
−2
5.26 × 10−1 h−1
P
−8
2.49 × 10−4 h−1
K
3
1.86 M−1 h−1
P
9
1.11×e6.16×10−6/D2.68−D0.03 h−1
K
4
1.20+4.48×105 e−12.70 D0.09 M−1 h−1
P
10
7.20 × 10−3 h−1
K
−4
3.86 × 10−4 h−1
P
11
6.06 × 10−4 h−1
K
5
15.24 M−1 h−1
P
12
2.76 × 10−1 h−1
K
−5
8.28 h−1
Q
1
7.80 × 103 M−1 h−1
K
6
18.06 M−1 h−1
Q
−1
1.71 × 10−4 h−1
K
−6
1.33 h−1
Q
2
3.00 × 104 M−1 h−1
K
7
2.73 × 105 M−1 h−1
Q
3
6.00 × 103 M−1 h−1
K
−7
3.20 h−1
Q
−3
6.06 × 10−4 h−1
K
8
5.52 × 10−1 h−1
Q
4
1.66 × 10−6 h−1
K
9
1.66 × 10−1 h−1
Q
5
8.40 × 104 M−1 h−1
K
10
1.93 × 10−7/Nir M
Q
−5
4.75 × 10−4 h−1
K
11
7.50 × 10−2 h−1
Q
6
11.58 h−1
K
12
11.10 h−1
R
1
2.39 × 103 M−1 h−1
P
1
1.75 × 103 M−1 h−1
R
−1
12.63 h−1
P
−1
1.33 × 10−4 h−1
R
2
4.07 × 104 M−1 h−1
P
2
7.21 h−1
R
3
9.82 h−1
P
3
1.37 × 104 M−1 h−1
R
4
1.47 × 105 M−1 h−1
P
−3
2.34 h−1
R
4
12.30 h−1
P
4
5.52 × 10−2 h−1
R
−4
2.72 h−1
P
5
1.20 × 105 M−1 h−1
R
5
1.65 × 10−1 h−1
N
irrep
0.12 e−2.48 D2.02−0.11 e−5.43 D0.76, D<10.01, D≥1

## Author ContributionsConceptualization, A.N.O. and O.B.; methodology, A.C. and O.B.; software, A.C. and O.B.; validation, A.C. and O.B.; formal analysis, O.B., A.C., M.P. and A.O.; investigation, O.B.,

## Author Contributions
Conceptualization, A.N.O. and O.B.; methodology, A.C. and O.B.; software, A.C. and O.B.; validation, A.C. and O.B.; formal analysis, O.B., A.C., M.P. and A.O.; investigation, O.B., A.C., M.P., A.O., P.E. and N.V.; resources, A.N.O.; data curation, A.C. and O.B.; writing—original draft preparation, O.B.; writing—review and editing, A.N.O.; visualization, A.C., A.O. and O.B.; supervision, A.N.O.; project administration, A.N.O.; funding acquisition, A.N.O. All authors have read and agreed to the published version of the manuscript.

## Institutional Review Board StatementNot applicable.

## Institutional Review Board Statement
Not applicable.

## Informed Consent StatementNot applicable.

## Informed Consent Statement
Not applicable.

## Data Availability StatementNot applicable.

## Data Availability Statement
Not applicable.

## Conflicts of InterestThe authors declare no conflict of interest.

## Conflicts of Interest
The authors declare no conflict of interest.

## Funding StatementThis research was funded by Russian Science Foundation, grant number 23-14-00078.

## Funding Statement
This research was funded by Russian Science Foundation, grant number 23-14-00078.

## FootnotesDisclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(

## Footnotes
Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.

## References1.Jeggo P.A., Löbrich M. DNA double-strand breaks: Their cellular and clinical impact? Oncogene. 2007;26:7717–7719. doi: 10.1038/sj.onc.1210868.2.Bushmanov A., Vorobyeva N., Molodtsova D., O

## References

## 1.Jeggo P.A., Löbrich M. DNA double-strand breaks: Their cellular and clinical impact? Oncogene. 2007;26:7717–7719. doi: 10.1038/sj.onc.1210868.2.Bushmanov A., Vorobyeva N., Molodtsova D., Osipov A.N.
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
12.
13.
14.
15.
16.
17.
18.
19.
20.
21.
22.
23.
24.
25.
26.
27.
28.
29.
30.
31.
32.
33.
34.
35.
36.
37.
38.
39.
40.
41.
42.
43.
44.
45.
46.
47.
48.
49.
50.
51.
52.
53.
54.
55.
56.

## Associated DataData Availability StatementNot applicable.

## Associated Data

## Data Availability StatementNot applicable.

## Data Availability Statement
Not applicable.