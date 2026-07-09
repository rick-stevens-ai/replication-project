# SCULPT paper — text extraction

**NOTE**: marker/nougat not available on uicgpu at replication time (2026-07-05); this extraction is from `pdftotext -layout paper.pdf` (900 lines, faithful reproduction of the two-column body text). All quantitative claims used by the replication were validated against this text plus manual inspection.

Lawrence Berkeley National Laboratory
LBL Publications

Title
An interactive machine learning platform for analyzing multi-particle coincidence data
from cold target recoil ion momentum spectroscopy.

Permalink
https://escholarship.org/uc/item/7976980f

Journal
The Review of scientific instruments, 97(5)

ISSN
0034-6748

Authors
Daoud, Hazem
Kumar, Sarvesh
Qian, Jin
et al.

Publication Date
2026-05-01

DOI
10.1063/5.0313735


Peer reviewed




 eScholarship.org                                 Powered by the California Digital Library
                                                                  University of California
   SCULPT:An Interactive Machine Learning Platform for Analyzing Multi-Particle
      Coincidence Data from Cold Target Recoil Ion Momentum Spectroscopy
                Hazem Daoud,∗ Sarvesh Kumar, Jin Qian, Daniel Slaughter, and Thorsten Weber†
                         Chemical Sciences Division, Atomic, Molecular and Optical Physics,
               Lawrence Berkeley National Laboratory, 1 Cyclotron Road, Berkeley, California 94720, USA

                                                      Tanny Chavez‡
                             Advanced Light Source, Lawrence Berkeley National Laboratory,
                                  1 Cyclotron Road, Berkeley, California 94720, USA
                                                 (Dated: June 3, 2026)
               We present SCULPT (Supervised Clustering and Uncovering Latent Patterns with Training),
            a comprehensive software platform for analyzing tabulated high-dimensional multi-particle coinci-
            dence data from Cold Target Recoil Ion Momentum Spectroscopy (COLTRIMS) experiments. The
            software addresses critical challenges in modern momentum spectroscopy by integrating advanced
            machine learning techniques with physics-informed analysis in an interactive web-based environ-
            ment. SCULPT implements Uniform Manifold Approximation and Projection (UMAP) for non-
            linear dimensionality reduction to reveal correlations in highly dimensional data. We also discuss
            potential extensions to deep autoencoders for feature learning, and genetic programming for auto-
            mated discovery of physically meaningful observables. A novel adaptive confidence scoring system
            provides quantitative reliability assessments by evaluating user-selected clustering quality metrics
            with predefined weights that reflect each metric’s robustness. The platform features configurable
            molecular profiles for different experimental systems, interactive visualization with selection tools,
            and comprehensive data filtering capabilities. Utilizing a subset of SCULPT’s capabilities, we ana-
            lyze photo double ionization data measured using the COLTRIMS method for 3-body dissociation
            of the D2 O molecule, revealing distinct fragmentation channels and their correlations with physics
            parameters. The software’s modular architecture and web-based implementation make it accessible
            to the broader atomic and molecular physics community, significantly reducing the time required
            for complex multi-dimensional analyses. This opens the door to finding and isolating rare events
            exhibiting non-linear correlations on the fly during experimental measurements, which can help steer
            exploration and improve the efficiency of experiments.


                   I.   INTRODUCTION                             components (px , py , pz for each of the five particles
                                                                 in each reaction), and the mass-to-charge ratio of each
   Cold Target Recoil Ion Momentum Spectroscopy                  ion. When combined with derived physical quantities
(COLTRIMS), often referred to as “reaction mi-                   such as kinetic energy release (KER), relative angles be-
croscopy”, has revolutionized our ability to study               tween particles, electron energy sharing, and others, the
atomic and molecular dynamics by enabling kinemati-              effective dimensionality can easily exceed 50 features per
cally complete measurements of multi-particle fragmen-           event. Modern COLTRIMS experiments routinely gen-
tation processes.[1–3] COLTRIMS allows the measure-              erate datasets containing tens of millions of such high-
ment of the three-dimensional momentum vectors of all            dimensional events. These events are represented as rows
ions and electrons produced in fundamental ionizing re-          in the list-mode file format, which records the events on
actions in gaseous atoms, molecules, and complexes, pro-         a shot-by-shot basis. The features (observables and de-
viding unprecedented insight into quantum mechanical             rived quantities) are stored in the columns of this large
processes, correlations, and coherences.[4, 5]                   table.[6]
   The comprehensive nature of COLTRIMS measure-                    The current well-established analysis approaches for
ments, while powerful, presents significant data analysis        COLTRIMS data have significant limitations:
challenges. For instance, a typical experiment studying
                                                                    1. Projection-based methods: Researchers typi-
the photo double ionization of water resulting in three-
                                                                       cally create one- or two-dimensional histograms of
body dissociation (H+ + O+ + H + 2e− or H+ + H+
                                                                       selected variables, potentially missing important
+ O + 2e− ), in which the 3D momentum of the neu-
                                                                       multi-dimensional correlations that reveal reaction
tral fragment was determined via momentum conserva-
                                                                       mechanisms.[7]
tion, produces events characterized by 15 momentum
                                                                    2. Sequential filtering: Applying cuts on selected
                                                                       parameters can introduce bias and obscure unex-
                                                                       pected patterns in the data.[8]
∗ HDaoud@lbl.gov
† TWeber@lbl.gov
                                                                    3. Manual feature engineering: The analysis re-
‡ TanChavez@lbl.gov
                                                                       lies heavily on domain expertise to construct rele-
                                                                                                                          2

      vant observables, potentially missing non-intuitive      vides high reproducibility, and meaningful organization
      relationships between observables or parameters.[9]      of clusters,[21] while preserving both local neighbor re-
                                                               lations and aspects of global structure. Applications
   Recent advances in machine learning,[10] particularly       in molecular dynamics simulations of biomacromolecules
in dimensionality reduction and unsupervised clustering,       have demonstrated UMAP’s superior performance when
offer promising solutions to these challenges.[11] The ap-     compared with linear reduction methods and compet-
plication of machine learning to high-dimensional exper-
                                                               itive performance with other nonlinear techniques.[23]
imental data analysis has seen remarkable growth across
                                                               In particle physics, machine learning has transformed
multiple domains of experimental physics, chemistry, bi-
                                                               data analysis and simulation, with applications rang-
ology and engineering.[12, 13] In X-ray scattering and
                                                               ing from boosted decision trees for classification to var-
spectroscopy, variational autoencoders and other dimen-
                                                               ious types of neural networks for pattern recognition
sionality reduction techniques have been successfully ap-
                                                               and event reconstruction.[24, 25] Reinforcement learn-
plied to learn latent representations of complex scatter-
                                                               ing approaches have been applied to hierarchical cluster-
ing patterns,[12] enabling researchers to identify similar
                                                               ing problems in particle physics, demonstrating that such
structures through latent space clustering and to gener-
                                                               tasks can be phrased as Markov Decision Processes.[26]
ate new structures through sampling and exploration of
                                                                  However, existing machine learning tools are typically
the learned manifold. Generative adversarial networks          not tailored to the specific requirements of tabulated
have been successfully applied to analyze ultrafast elec-      momentum spectroscopy data, lacking physics-informed
tron diffraction images, demonstrating the utility of deep     constraints, configurable molecular systems for differ-
learning approaches for extracting structural dynamics         ent experimental targets, adaptive quality assessment
from high-dimensional experimental data where tradi-           for clustering reliability, and interactive exploration tools
tional analysis methods face ambiguity.[14] For small-         for multi-dimensional correlations. In parallel with the
angle X-ray scattering (SAXS) data, variational autoen-        present work, Venkatachalam et al. [27] recently reported
coders have been employed to visualize large datasets in       on ML-assisted Coulomb explosion imaging (CEI) guided
low-dimensional latent spaces, enabling rapid capture of       by classical simulations to extract molecular geometries
key features such as similarity among scattering patterns      and distinguish between isomers of mid-sized molecules
and structural evolution trends.[15] In protein structure      from list-mode data. In another concurrent study, Li et
analysis, autoencoders trained to compress 3D shape in-        al. [28] employed a deep generative neural network to
formation into 200-dimensional latent spaces have been         infer molecular structures from ion momentum distribu-
combined with genetic algorithms to build 3D models            tions generated during the rapid Coulomb explosion of
consistent with scattering data,[16] demonstrating the         molecules with up to nine atoms. In both approaches,
power of latent space optimization for inverse problems.       the complete CEI, where all atomic ionic fragments of
   Recent efforts have focused on creating integrated web-     the molecule are detected, is currently a prerequisite,
based platforms for ML-driven analysis of experimen-
                                                               and based on this, the authors demonstrate its poten-
tal data at scientific user facilities. The MLExchange
                                                               tial to investigate molecular transformation in real-time
platform introduced a novel labeling pipeline that accel-
                                                               with unprecedented detail. Beyond complete CEI, which
erates annotation of large scientific datasets using AI-
                                                               is well suited for strong-field laser and XFEL CEI ex-
guided tagging techniques, with interconnected graphi-
                                                               periments, the momentum-spectroscopy community will
cal user interfaces for data reduction, classification, la-
                                                               benefit from an integrated platform that unifies modern
tent space exploration, and label assignment.[17] This
                                                               dimensionality-reduction methods with domain-specific
approach has proven instrumental for pattern recognition
                                                               analysis tools in an accessible, web-based environment
in X-ray scattering data, enabling scientists to label large
                                                               capable of correlating electrons, ions, and at least one
datasets efficiently while maintaining the ability to train
                                                               neutral fragment in a general and flexible way.
and fine-tune customizable ML models within the same              We present SCULPT, an integrated software platform
pipeline. Mass spectrometry imaging, which shares with         that bridges this gap by combining state-of-the-art ma-
COLTRIMS the challenge of high-dimensional, multi-             chine learning techniques with physics-informed analysis
parameter datasets, has benefited from variational au-         tools specifically designed for multi-particle coincidence
toencoder approaches that learn nonlinear spectral man-        list-mode data. The key innovations of SCULPT include:
ifolds to reveal biologically relevant clusters.[18] Convo-
lutional autoencoders have proven particularly effective          1. Physics-based dimensionality reduction: The
at aggregating features and preserving low-abundant sig-             integration of UMAP[20] with automated physics
nals in their latent space representations,[19] addressing           feature calculation ensures that dimensionality re-
challenges similar to those faced in identifying rare frag-          duction preserves physically meaningful structures.
mentation channels in COLTRIMS data.
   The Uniform Manifold Approximation and Projec-                 2. Adaptive and quantitative reliability assess-
tion (UMAP) technique[20] has emerged as a partic-                   ment: A confidence scoring system that evaluates
ularly powerful tool for dimensionality reduction in                 user-selected clustering quality metrics through
biological and physical sciences.[21, 22] Compared to                weighted combination provides interpretable reli-
other dimensionality reduction methods, UMAP pro-                    ability assessments of UMAP results.
                                                                                                                       3

   3. Interactive exploration of multidimensional                      B.        Machine Learning Components
      data by arbitrary dimensionality reduction:
      Dynamic visualization with selection and filter-
      ing tools enables a hypothesis-driven analysis un-                          1.   UMAP Implementation
      restricted by conventional 1-D or few-dimensional
      projections.
                                                                 SCULPT employs UMAP[20] for non-linear dimen-
   4. Flexible configurable molecular systems: A              sionality reduction of high-dimensional COLTRIMS
      profile-based system for defining arbitrary molecu-     data. UMAP constructs a topological representation
      lar configurations calculates appropriate mass- and     of the high-dimensional data by modeling each data
      charge-dependent features.                              point’s relationship to its nearest min, then optimizes
                                                              a low-dimensional embedding that preserves these local
   5. Automated feature discovery: Genetic pro-               neighborhood structures while maintaining global data
      gramming algorithms[29] that discover mathemati-        topology. This approach is particularly effective for
      cal combinations of input features aid in discovering   COLTRIMS data as it reveals non-linear correlations be-
      relevant clusters and correlations.                     tween momentum components and derived physics quan-
                                                              tities that are not apparent in traditional linear projec-
                                                              tion methods. The user selects a set of calculated physics
                                                              features (kinetic energies, angular distributions, correla-
     II.   SOFTWARE ARCHITECTURE AND
               IMPLEMENTATION
                                                              tion parameters) or original momentum components as
                                                              the inputs to be embedded into the UMAP algorithm.
                                                              The implementation preserves file labels throughout the
   SCULPT is implemented as a web-based application           dimensionality reduction process, enabling direct com-
using Python and Plotly Dash framework,[30] chosen for        parison of multiple datasets or experimental conditions
its ability to create reactive, interactive visualizations    within the same 2D visualization space. Key UMAP pa-
without requiring client-side programming. The platform       rameters including the number of neighbors (nneighbors ,
follows a modular design that integrates data processing,     controlling local versus global structure preservation) and
machine learning analysis, quality assessment, and inter-     minimum distance (min dist, controlling cluster com-
active visualization capabilities into a cohesive workflow    pactness) are user-configurable, with typical values of
for COLTRIMS data exploration.                                nneighbors = 15 and min dist = 0.1 providing effective
                                                              visualizations for COLTRIMS datasets.

      A.   Data Processing and Physics Feature
                    Calculation

  The data processing layer handles importing
COLTRIMS data files and implements a novel molecular                        2.    Deep Autoencoder Architecture
configuration system. Users can define molecular profiles
by specifying particle types, masses, and charges (see
Fig. 1).                                                         The autoencoder module implements a symmetric neu-
  Moreover, it enables accurate physics calculations for      ral network architecture using PyTorch for feature learn-
various molecular photoionization experiments, with tar-      ing from high-dimensional COLTRIMS data. The net-
gets such as different isotopologues (e.g., H2 O, D2 O,       work consists of an encoder that progressively compresses
HDO), as well as other molecular systems, without source      the input feature space through multiple hidden layers to
code modification.                                            a low-dimensional latent representation, and a symmet-
  The physics feature calculator automatically com-           ric decoder that reconstructs the original features from
putes:                                                        this compressed representation. The latent space dimen-
                                                              sionality (typically 2-10 dimensions) is user-configurable,
   • Individual particle kinetic energies: Ei = p2i /(2mi )   with the compression forcing the network to learn the
                                                              most salient features that capture the essential variance
   • Kinetic P
             Energy Release of dissociation processes:        in the fragmentation dynamics. Training employs mean
     KER = Eions                                              squared error reconstruction loss with the Adam opti-
                                                              mizer, and the resulting latent features can be visualized
   • Sum of electron energies: EESum =                        directly or used as input to subsequent UMAP projection
                                        P
                                           Eelectrons
                                                              and clustering analysis. This approach is particularly
   • Relative angles between all particle pairs               effective for discovering non-linear correlations between
                                                              momentum components and derived physics quantities
   • Energy sharing parameters such Pas electron energy       that may not be apparent through traditional feature se-
     sharing: EESharing = Eelectron / Eelectrons              lection methods.
                                                                                                                     4




                FIG. 1: Flowchart showing the molecular configuration and data processing workflow.


      3.   Genetic Programming for Feature Discovery          ulations of mathematical expressions through selection,
                                                              crossover, and mutation operations, the genetic program-
                                                              ming module can identify complex combinations of mo-
   SCULPT implements genetic programming using                mentum components, energies, and angular features that
symbolic regression to discover interpretable feature         capture underlying correlations in fragmentation pat-
combinations.[29, 31] Genetic programming has proven          terns, thereby enhancing the ability to distinguish be-
effective for automated feature construction in scien-        tween different quantum states or reaction pathways in
tific data analysis, particularly when the goal is to dis-    COLTRIMS data.
cover non-trivial mathematical relationships between in-
put variables that may not be apparent through tradi-
tional feature engineering.[32, 33] This approach is ex-
plicitly chosen to discover non-trivial features that might             C.   Adaptive Quality Assessment
provide superior cluster separation compared to stan-
dard physics parameters (like energy and momentum                A key innovation in SCULPT is the adaptive confi-
conservation). The method has been successfully ap-           dence scoring system that provides quantitative reliabil-
plied to experimental physics data, where dimensional         ity assessments for clustering results. The system eval-
consistency and physical interpretability of constructed      uates user-selected clustering quality metrics, each au-
features are critical requirements.[31] By evolving pop-      tomatically assigned predefined weights and reliability
                                                                                                                           5

scores based on their robustness and general applicabil-              reliability or confidence in the validity of the met-
ity. Users select which metrics to calculate through the              ric. The weights sum to unity across all active met-
interface, allowing flexibility and balance between com-              rics, and reliability scores modulate the influence of
putational cost and analysis depth. The confidence score              each metric based on empirical performance across
is then computed as a weighted combination of only the                diverse clustering scenarios.
selected metrics, with weights normalized to account for
that subset of metrics. Metrics are organized into three           2. Hopkins Statistic H ∈ [0, 1]: This metric assesses
tiers based on their general reliability: Tier 1 metrics (sil-        the clustering tendency of the dataset by measur-
houette score, Hopkins statistic) are highly reliable and             ing the probability that the data is generated from a
recommended for all analyses; Tier 2 metrics (cluster sta-            uniform distribution versus containing meaningful
bility, physics consistency, Calinski-Harabasz index) pro-            clusters.[36, 37] The statistic compares the nearest-
vide additional validation with moderate reliability; and             neighbor distances for a sample of real data points
Tier 3 metrics (Davies-Bouldin index) are included with               against those for randomly generated points within
heavily reduced weight due to known limitations. The                  the same space. Values of H > 0.75 indicate strong
only automatic exclusion occurs for the physics consis-               clusterability (the data significantly deviates from
tency metric, which is omitted when physics features are              uniform randomness), while H < 0.5 suggests the
unavailable in the dataset. These reliability tiers and               data may be uniformly distributed with no inher-
associated weights were empirically determined through                ent cluster structure. This metric receives w = 0.25
validation on the D2 O double ionization dataset with                 and r = 0.85, reflecting its importance in deter-
known ground truth quantum state assignments.[34] The                 mining whether clustering is appropriate for the
tier assignments reflect performance patterns observed                dataset. Here, H refers specifically to the Hopkins
when separating the eight distinct dication states in this            statistic value.
well-characterized system, where the metrics’ ability to           Tier 2 metrics (moderate reliability, useful for com-
correctly identify physically meaningful clusters could be       prehensive assessment):
verified against established quantum state separations.
The adaptive confidence score is intended as a heuris-             1. Cluster Stability ∈ [0, 1]: Measures the repro-
tic guide for exploratory analysis rather than a rigorous             ducibility of cluster assignments under small per-
statistical measure of physical correctness. In practice,             turbations by injecting Gaussian noise (5% of fea-
scores are categorized as follows: ≥ 0.65 (High) indi-                ture standard deviation) into the data and com-
cates reliable cluster separation suitable for drawing pre-           paring the resulting cluster assignments with the
liminary conclusions; 0.50–0.65 (Moderate) suggests rea-              original using the Adjusted Rand Index.[38] High
sonably reliable results that warrant further validation;             stability values (> 0.8) indicate robust clusters that
0.35–0.50 (Low) indicates results should be used with                 are insensitive to minor variations in the data, while
caution and may benefit from alternative feature selec-               low values suggest the clustering may be capturing
tion or UMAP parameters; and ≤ 0.35 (Very Low) sug-                   noise rather than genuine structure. This metric
gests the clustering may not capture meaningful struc-                receives w = 0.15 and r = 0.7.
ture.
                                                                   2. Physics Consistency ∈ [0, 1]: This metric is au-
   Tier 1 metrics (highest reliability, recommended for               tomatically excluded when physics features are un-
all analyses):                                                        available in the dataset (e.g., when analyzing au-
                                                                      toencoder latent representations). It is a domain-
   1. Silhouette Score S ∈ [−1, 1]: This metric mea-                  specific validation metric that measures the ratio
      sures both cluster cohesion (how similar a point                of within-cluster variance to between-cluster vari-
      is to others in its own cluster) and separation (how            ance for key physics parameters. The metric evalu-
      dissimilar it is to points in neighboring clusters).[35]        ates a predefined set of physics quantities: KER,
      For each data point i, the silhouette coefficient is            EESum, EESharing, individual particle energies
                                b(i)−a(i)
      calculated as s(i) = max{a(i),b(i)} , where a(i) is the         (ions and electrons), and total energy. For each
      mean distance to other points in the same clus-                 available physics parameter, the metric calculates
                                                                                    Varbetween
      ter and b(i) is the mean distance to points in the              P Ci = Varbetween  +Varwithin , where Varbetween is the
      nearest neighboring cluster. The overall silhouette             variance of cluster means weighted by cluster size,
      score is the mean across all points. Values near                and Varwithin is the weighted average of within-
      +1 indicate well-separated clusters, values near 0              cluster variances. The overall physics consistency
      suggest overlapping clusters, and negative values               is the mean across all evaluated parameters. Values
      indicate potential misclassification. This metric re-           near 1 indicate that clusters correspond to physi-
      ceives a weight of w = 0.35 (contributing 35% to                cally distinct states with homogeneous physics pa-
      the final confidence score) and a reliability score of          rameter distributions within each cluster, even if
      r = 0.9 (indicating 90% confidence in its assess-               these physics parameters were not explicitly used
      ment validity). The weight w is the contribution to             as clustering features. This provides an indepen-
      the overall confidence score, and r represents the              dent validation that the clustering captures mean-
                                                                                                                           6

      ingful physical differences rather than arbitrary
      data structure. This metric receives w = 0.2 and                                   P
      r = 0.8.                                                                            i wi · r i · n i
                                                                                   C=     P                ,             (1)
                                                                                            i wi · r i
   3. Calinski-Harabasz Index ∈ [0, ∞): Measures
      cluster separation by computing the ratio of                 where wi is the weight for metric i, ri is its reliability
      between-cluster dispersion to within-cluster disper-     score, and ni is the normalized value of metric i. The
      sion in the UMAP latent space.[39] The index is          sum ranges only over the metrics selected by the user for
                            tr(Bk )     −k                     calculation. The normalization function ni transforms
      defined as CH = tr(W      k)
                                    × Nk−1 , where Bk is
                                                               each metric to a [0, 1] scale using metric-specific scaling
      the between-cluster dispersion matrix, Wk is the         functions designed to provide realistic assessments across
      within-cluster dispersion matrix, N is the num-          the full range of possible values.
      ber of data points, and k is the number of clus-             The system incorporates several advanced features to
      ters. Higher values indicate better-defined clusters     ensure robust assessment:
      with greater separation in the reduced-dimensional           Adaptive normalization employs metric-specific
      space. This metric receives w = 0.1 and r = 0.6.         scaling functions that account for the different value
  Tier 3 metrics (lower reliability, heavily down-             ranges and distributions of each metric. For the sil-
weighted):                                                     houette score, the transformation is nS = 0.5(S + 1),
                                                               mapping [−1, 1] to [0, 1]. For the Hopkins statistic,
   1. Davies-Bouldin Index ∈ [0, ∞): Measures the              nH = H (already in [0, 1]). For the Calinski-Harabasz in-
      average similarity ratio between each cluster and its    dex, a logarithmic transformation nCH = min(1, log(1 +
      most similar neighbor, where similarity is defined       CH)/ log(1000)) prevents extremely large values from
      as the ratio of within-cluster scatter to between-       dominating. For the Davies-Bouldin index, nDB =
      cluster separation.[40] Lower values indicate bet-       max(0, 1 − DB/3) transforms lower-is-better to higher-
      ter clustering. However, this metric is known to         is-better with appropriate scaling. These functions avoid
      be sensitive to cluster shape assumptions (favoring      overly harsh penalties for moderate clustering while pre-
      spherical clusters) and can produce misleading re-       serving sensitivity to exceptional results, with normalized
      sults for elongated or irregular cluster geometries      values capped at 0.98 to reserve perfect scores for theo-
      common in UMAP embeddings.[41] Due to these              retical limits.
      limitations, it receives minimal weight (w = 0.005)          Critical threshold management applies contextual
      and low reliability (r = 0.4).                           penalties to prevent overconfident assessments of poor
                                                               clusterings. Severe failures (silhouette score S < −0.1
   Additionally, the system tracks the Noise Ratio ∈           or Hopkins statistic H < 0.3) cap the confidence at 0.4,
[0, 1], representing the fraction of points classified as      indicating fundamental clustering problems. Borderline
noise by the clustering algorithm. SCULPT implements           cases are identified as those with 0.2 < S < 0.4 or 0.5 <
DBSCAN (Density-Based Spatial Clustering of Applica-           H < 0.7, which receive moderate penalties (confidence
tions with Noise)[42] as the primary clustering algorithm,     capped at ≤ 0.7) to reflect ambiguous cluster quality.
which automatically identifies noise points as those not           Performance bonuses are applied using asymptotic
belonging to any dense region. For the main UMAP anal-         scaling to reward exceptional clustering without inflat-
ysis and custom scatter plots, DBSCAN uses automatic           ing confidence unrealistically. Four bonus conditions are
parameter optimization where the algorithm searches            evaluated: exceptional silhouette scores (S > 0.6, +0.1
for the optimal epsilon value (distance threshold) while       bonus), very low noise ratios (noise < 0.05, +0.05 bonus),
maintaining a fixed minimum sample requirement of 5            high stability (stability > 0.8, +0.05 bonus), and strong
neighbors. The optimization procedure tests epsilon val-       clustering tendency (H > 0.8, +0.05 bonus). The bonus
ues in the range [0.1, 1.0] and selects the configuration      system uses asymptotic scaling: Cnew = C + (0.95 − C) ·
                                                               bonus
that maximizes the number of clusters while keeping the          0.95 to maintain realistic confidence bounds and prevent
noise ratio below 50%. In the advanced genetic program-        scores from approaching 1.0.
ming module, users have full control over both the ep-             Uncertainty quantification provides confidence in-
silon and minimum samples parameters, allowing for fine-       tervals around the final score to communicate the reli-
tuning based on specific dataset characteristics. Points       ability of the assessment. The base uncertainty is cal-
are labeled as noise if they have fewer than the mini-         culated as σbase = 0.1 + max(0, (3 − nmetrics )) × 0.05,
mum number of neighbors within the specified radius.           where nmetrics is the number of active metrics used in
The noise ratio influences both reliability assessment and     the calculation. This function was empirically derived
performance bonuses, with very low noise ratios (< 0.05)       through iterative testing on the eight known dication
indicating clean cluster separation.                           states in the D2 O double ionization dataset,[34] where
   The adaptive confidence score C serves as a summary         the uncertainty model parameters (0.1 baseline and 0.05
metric that combines all individual quality assessments        penalty per missing metric) were tuned to reflect ob-
into a single interpretable value. It employs a reliability-   served variations in metric reliability. The 0.1 base-
weighted calculation:                                          line represents the estimated inherent measurement un-
                                                                                                                             7

certainty, while the penalty term increases uncertainty          and direct feature scatter plots. The implementation uses
when fewer metrics are available (reflecting reduced in-         efficient grid-based density estimation that operates on
formation). The base uncertainty is further adjusted             any two-dimensional data representation:
for the average reliability of active metrics: σ Ptotal =
                                                     i ri
σbase + max(0, (0.8 − ravg )) × 0.1, where ravg = nmetrics .
This adjustment increases uncertainty when relying on                                          N
less reliable metrics.                                                                     1 X
                                                                           ρ(xi , yi ) =         Gσ (xi − xj , yi − yj ),   (2)
                                                                                           N j=1

     D.   Advanced Data Filtering and Selection
                                                                    where Gσ is a Gaussian kernel with bandwidth param-
   SCULPT incorporates sophisticated data filtering ca-          eter σ (user-adjustable from 0.01 to 1.0), and (xi , yi ) rep-
pabilities that enable users to refine datasets at mul-          resents coordinates in either the 2D UMAP embedding
tiple stages of the analysis pipeline, enhancing both            space or direct feature space (e.g., energy vs. angle scat-
computational efficiency and analytical focus. The sys-          ter plots). The system creates a 100×100 grid histogram
tem provides three primary filtering mechanisms: (1)             of the selected coordinates, applies Gaussian smoothing
feature-based selection, (2) density-based filtering, and        with σsmooth = 10σ, and assigns density values to each
(3) physics parameter filtering.                                 point based on grid interpolation.
                                                                    Points are filtered using a percentile-based threshold
                                                                 τp , where users specify the percentile (0-100%) of den-
              1.    Feature Selection Framework                  sity values to retain. Points with density ρ ≥ τp are pre-
                                                                 served, effectively removing sparse outliers while main-
   The feature selection system organizes available vari-        taining the core cluster structure. This approach signif-
ables into hierarchical categories based on their physical       icantly reduces computational overhead for subsequent
significance and computational origin. Features are au-          analyses, while preserving essential clustering patterns.
tomatically categorized as follows:                                 For scatter plot applications, density filtering enables
   Original Momentum Components: Raw momen-                      users to focus on statistically significant regions within
tum measurements (px , py , pz ) for each detected particle,     the original feature space by removing experimental noise
providing the fundamental kinematic information from             and low-statistics outliers that might otherwise obscure
experimental data.                                               underlying physical correlations. The same mathemat-
   Momentum q Magnitudes: Derived scalar quanti-                 ical framework applies whether filtering UMAP embed-
      pi | = p2x,i + p2y,i + p2z,i for each particle, offering
ties |⃗                                                          dings or direct two-dimensional projections of calculated
                                                                 physics parameters.
magnitude-based clustering without directional bias.
   Energy Variables: Comprehensive energy features
including individual particle kinetic energies, Kinetic En-
ergy Release representing the sum of ion energies, elec-
tron energy sum, electron energy sharing ratios, and total                      3.   Physics Parameter Filtering
system energy.
   Angular Features: Laboratory-frame polar an-                     Physics parameter filtering enables domain-specific
gles θi = arccos(pz,i /|⃗   pi |) and azimuthal angles ϕi =      data selection based on physically meaningful quantities.
arctan 2(py,i , px,i ) for each particle, enabling analysis of   The system supports filtering on commonly used physics
angular distributions and correlations.                          parameters including kinetic energy release (KER), in-
   Correlation Features: Inter-particle relationships            dividual particle kinetic energies for ions and electrons,
including dot products p⃗i ·⃗   pj , momentum differences, and   electron energy sums and energy sharing ratios, inter-
                                               ⃗ ·⃗
                                               p  p
angles between particle pairs cos(αij ) = |⃗pii||⃗pjj | .        particle angular correlations, and momentum differences
   The system provides hierarchical selection controls           between particles. This filtering capability enables selec-
with category-level selection and individual feature tog-        tion of specific energy regimes, geometric configurations,
gling, which enables efficient exploration of the high-          or correlation patterns corresponding to different physi-
dimensional feature spaces, while maintaining the inter-         cal processes.
pretability of the selected subset.                                 For each selected parameter, the system automatically
                                                                 determines the data range and provides an interactive
                                                                 range slider with intelligent binning. The parameter
                   2.   Density-Based Filtering                  range is dynamically calculated as [⌊min(P )⌋, ⌈max(P )⌉]
                                                                 where P represents the selected parameter values across
  Density-based filtering addresses the challenge of com-        all loaded datasets. The filtering condition retains data
putational scalability and noise reduction by selectively        points where Pmin ≤ Pi ≤ Pmax , based on user-specified
retaining high-density regions in both UMAP projections          bounds.
                                                                                                                       8

              4.   Integrated Filtering Pipeline               choices implemented in SCULPT.
                                                               Confidence score weighting: The tiered metric sys-
   The filtering system operates through an integrated         tem emphasizes local density structure (silhouette score,
pipeline where filters can be applied sequentially:            weight 0.35) and intrinsic clusterability (Hopkins statis-
   1. Feature Selection: Users first select relevant fea-      tic, weight 0.25) because these properties are most
tures for dimensional reduction, reducing computational        relevant for identifying physically distinct fragmenta-
complexity and focusing on scientifically relevant dimen-      tion channels in momentum space. Metrics known to
sions.                                                         be sensitive to cluster shape assumptions, such as the
   2. UMAP Projection: The selected features un-               Davies-Bouldin index, are heavily downweighted (weight
dergo UMAP embedding to create the 2D visualization            0.005) since UMAP embeddings frequently produce non-
space.                                                         spherical cluster geometries. This weighting scheme may
   3. Density Filtering: Optional density-based filter-        undervalue clustering quality in datasets where global
ing removes low-density outliers from the UMAP space,          structure is more important than local density, or where
improving signal-to-noise ratio.                               clusters have highly uniform, spherical shapes.
   4. Physics Filtering: Optional parameter-based fil-         DBSCAN parameter selection: The automatic ep-
tering selects physically meaningful subsets for targeted      silon optimization maximizes the number of detected
analysis.                                                      clusters subject to a 50% noise threshold. This heuris-
   Each filtering step preserves data provenance, main-        tic favors segmentation—revealing fine structure that
taining links between filtered subsets and original ex-        might otherwise be merged—over conservative clustering
perimental data. The system provides detailed filtering        that minimizes false positives. For applications requir-
statistics, which includes retention percentages and per-      ing high-purity cluster assignments, users should consider
file event counts, enabling users to assess the impact of      manually adjusting epsilon toward larger values or using
each filtering operation.                                      the advanced analysis module where full control over DB-
   This multi-stage filtering approach enables efficient ex-   SCAN parameters is available.
ploration of large experimental datasets while maintain-       UMAP parameters: The default values (nneighbors =
ing physical interpretability and statistical rigor, sup-      15, min dist = 0.1) balance local and global struc-
porting both exploratory data analysis and hypothesis-         ture preservation for typical COLTRIMS dataset sizes
driven investigation of specific reaction mechanisms.          (104 –106 events). Smaller nneighbors values emphasize lo-
                                                               cal structure and may reveal finer sub-clustering, while
                                                               larger values preserve more global topology at the cost of
  E.   Interactive Visualization and Selection Tools           local detail. These parameters should be adjusted based
                                                               on dataset size and the scale of structure being investi-
  SCULPT provides multiple visualization modes with            gated.
consistent interaction patterns:                               The current defaults may perform poorly for datasets
                                                               with highly imbalanced cluster sizes, where small but
   1. Scatter plots: Interactive 2D projections with           physically important clusters may be classified as noise;
      lasso and box selection tools                            for data with continuous gradients rather than discrete
                                                               clusters; or for very small datasets (< 1000 events) where
   2. Density heatmaps: Kernel density estimation for          the Hopkins statistic and stability metrics become un-
      identifying high-density regions                         reliable. In such cases, users should rely more heavily
                                                               on visual inspection and physics-based validation rather
   Selection tools are implemented using Plotly’s built-
                                                               than the confidence score alone. Additionally, the filter-
in selection capabilities. These tools empower the user
                                                               ing features incorporated in SCULPT serve to aid users
to identify and isolate groups of events and save them
                                                               identify clusters that would otherwise be challenging to
in separate files for further processing. To further un-
                                                               isolate.
derstand the physics that correlates events in any one
cluster, SCULPT enables the user to visualize events in
scatter plots or heat maps according to any of the orig-          III.   USER INTERFACE AND WORKFLOW
inal features such as total energy, kinetic energy release
(KER), etc. This allows for vetting the data, visualizing
                                                                             A.   Interface Organization
the clusters identified by SCULPT on lower-dimensional
phase spaces and understanding the physics behind the
clustering.                                                       SCULPT’s interface is organized into five main sec-
                                                               tions (see Fig. 2):
                                                                  1. Data & Configuration: File upload and molec-
  F.   Design Philosophy and Default Parameters                      ular profile management
                                                                  2. Basic Analysis: Probabilistic machine learning
  In this section we shed light on the default parameter             (UMAP embedding) and custom feature plots
                                                                                                                             9

   3. Selection & Filtering: Interactive data selection                           A.     Experimental Data
      and filtering tools
   4. Advanced Analysis: Re-analysis of selected sub-                The dataset, consisting of the eight aforementioned
      sets                                                        files, contains around 1,900,000 coincidence events where
                                                                  four of the five particles were detected: D+ + D+ + O +
   5. Machine Learning: Autoencoder and genetic                   e− + e− . Each event is characterized by 15 momentum
      programming modules                                         components (px , py , pz for each of the five particles). For
                                                                  computational efficiency, all of the UMAP analyses pre-
                                                                  sented here were conducted on a random 1% sample of
            B.    Typical Analysis Workflow                       the full dataset. This sampling approach allows for rapid
                                                                  iterative exploration while preserving the essential clus-
  A typical analysis workflow proceeds as follows:                tering structure of the data. The sample size is chosen
                                                                  to provide reasonably low statistical uncertainties and
   1. Data Import: Upload COLTRIMS data files and                 sufficient density over the measured phase space to visu-
      select appropriate molecular configuration                  alize clusters. After identifying clusters of interest on a
                                                                  sampled subset, we recommend users to re-run UMAP
   2. Initial Exploration: Run UMAP to visualize
                                                                  with different sampling fractions (ideally up to the full
      data structure.
                                                                  dataset) to verify that the cluster structure is preserved.
   3. Cluster Identification: Use DBSCAN with auto-
      matic parameter optimization or just rely on man-
      ual data separation by identifying clusters visually.                         B.    Analysis Results

   4. Quality Assessment: Review confidence scores
      and individual metrics.                                        To demonstrate SCULPT’s capabilities while main-
                                                                  taining computational efficiency, all UMAP analyses pre-
   5. Refinement: Select interesting regions for de-              sented here were conducted on a random 1% sample of
      tailed analysis.                                            the full dataset. This sampling approach allows for rapid
                                                                  iterative exploration while preserving the essential clus-
   6. Feature Discovery: Optionally, apply genetic
                                                                  tering structure of the data.
      programming to attempt to discover new correla-
      tions.
   7. Validation: Verify results by understanding                                  1.    UMAP Visualization
      the underlying physics, for example via plotting
      the identified clusters on physics-informed phase              The initial UMAP analysis revealed five distinct clus-
      spaces.                                                     ters, separated by white space in the 2D projection, as
                                                                  shown in Fig. 3. This UMAP analysis was run by se-
   8. Export: Save filtered datasets and discovered fea-
                                                                  lecting the features KER, EESum, Total Energy (KER
      tures as labeled list-mode data for further process-
                                                                  + EESum), and the angle between α12 between the ion
      ing.
                                                                  1 and ion 2 momenta. Two of the clusters consist of one
All these steps are to be reiterated with the data in saved       quantum state exclusively, while the other three clusters
files for further processing.                                     include two or more quantum states. These clusters need
                                                                  to be further analyzed to isolate each of the quantum
                                                                  states contained in them. Typically, the user would at-
IV.    CASE STUDY: D2 O DOUBLE IONIZATION                         tempt to separate quantum states within large clusters
                                                                  while being guided by the confidence score and the visual
  To demonstrate SCULPT’s capabilities with a well-               check of achieving clear separations in UMAP plots. As
conditioned example, we present a reanalysis of the D2 O          an example, in Fig. 4, we show the cluster containing the
double ionization following single photon absorption at           three states that was separated with the Lasso selection
61 eV. Particularly, we considered the D2 O2+ → D+ +              tool.
D+ + O dissociation channel that was previously ana-                 After isolating this cluster, we run UMAP on it again,
lyzed for H2 O by Reedy et. al.[34] We created ground             this time while selecting the features KER, EESum, and
truth data based on the analysis in that work to isolate          Total Energy. The result, depicted in Fig. 5, shows that
each of the quantum states of the water dication follow-          the group is now separated into two distinct clusters. One
ing dissociative photo- double ionization. This resulted          of the clusters contains the two states producing the oxy-
in eight event list data files, containing the 3D momen-          gen atom in the 1 D state, specifically the water dication
tum vector components of each particle for each event,            states 1 B2 (light-blue in Fig. 5) and 21 A1 (orange). The
for each quantum state: 3 A2 ,3 B1 , 3 B2 (producing oxy-         calculated confidence score is 0.70 confirming a high con-
gen O 3 P),11 A1 , 21 A1 , 1 B1 , 1 B2 (producing O 1 D), 31 A1   fidence in separating the data according to the selected
(producing O 1 S).                                                features. We select the cluster containing the two states
                                                                                                                     10




                 FIG. 2: Flowchart showing the interactive analysis and quality assessment workflow.


and run UMAP analysis on it, again using the features        + D+ + O fragmentation channel:
KER, EESum, Total Energy, and α12 . The cluster is             Cluster 1 (dark-blue in Fig. 3, 2.6% of events):
subsequently separated into two distinct clusters, each      D2 O2+ (1 B1 ) dissociating to D+ + D+ + O(1 D)
containing a single quantum state, as shown in Fig. 6.
A high confidence score of 0.79 is calculated. Following        • A singlet dication state that dissociates with a peak
the same general procedures described for the examples            KER of ∼ 4.3 eV and a β of ∼ 149◦ . The kine-
above, all eight quantum states in the present data are           matic signatures of this state overlap with those of
separable into individual clusters.                               the triplet dication states 3 B1 and 31 A1 , making
                                                                  clean separation more challenging than some other
                                                                  examples presented here.
   2.   Cluster Identification and Physics Interpretation
                                                               Cluster 2 (red in Fig. 3, 3.0% of events): D2 O2+ (3 B1 )
                                                             dissociating to D+ + D+ + O(3 P)
  A detailed analysis of the data enabled the isolation of
the following clusters stemming from the D2 O2+ → D+            • A triplet dication state with a peak KER of ∼ 4.3
                                                                                                                     11




FIG. 3: UMAP projection of D2 O double ionization data showing five identified clusters. The calculated confidence
         score is 0.71. Colors represent different dication states and are for visualization purposes only.




   FIG. 4: Selected cluster containing three dication            FIG. 5: UMAP projection of D2 O double ionization
states. Colors represent different dication states and are    data of the selected cluster. Separation into two clusters
             for visualization purposes only.                  is evident. The bottom cluster contains data from two
                                                              dication states. The calculated confidence score is 0.70.
                                                                 Colors represent different dication states and are for
      eV and a β of ∼ 146◦ . It is characterized by a                        visualization purposes only.
      narrow β distribution.
  Cluster 3 (dark-green in Fig. 3, 4.6% of events):
D2 O2+ (31 A1 ) dissociating to D+ + D+ + O(1 S)                Cluster 5 (orange in Figs 3 - 6, 10.7% of events):
                                                              D2 O2+ (21 A1 ) dissociating to D+ + D+ + O(1 D)
    • The only dication state leading to the O(1 S) asymp-
      tote. It is a singlet state with a peak KER of ∼ 11.4      • A singlet dication state characterized by a high
      eV and a β of ∼ 111◦ .                                       β (protons nearly opposite directions) and a peak
                                                                   KER of ∼ 7.7 eV.
  Cluster 4 (purple in Fig. 3, 8.2% of events): D2 O2+
( A2 ) dissociating to D+ + D+ + O(1 D)
1                                                               Cluster 6 (light-blue in Figs 3 - 6, 18.2% of events):
                                                              D2 O2+ (1 B2 ) dissociating to D+ + D+ + O(1 D)
    • A singlet dication state with a peak KER of ∼ 7.6
      eV and a β of ∼ 126◦ .                                     • A singlet dication state with a peak KER of ∼ 9.8
                                                                                                                     12

                                                                • Davies Bouldin: 0.7306

                                                                As clusters containing multiple quantum states are
                                                             progressively separated through iterative analysis, the
                                                             reliability score increases. For example, the confidence
                                                             score for the UMAP embedding in Fig. 5 is 0.70, and
                                                             when it is further sub-clustered, as shown in Fig. 6, the
                                                             confidence score becomes 0.79. In contrast, selecting only
                                                             KER, EESum and Total Energy as UMAP features re-
                                                             sults in poor separation, as shown in Fig. 7, and a poor
                                                             score of 0.14. Hence, the confidence score, combined with
                                                             visual inspection of cluster separation, guides the itera-
                                                             tive selection of data subsets and appropriate features for
                                                             subsequent clustering refinement.
                                                                It is important to note that individual metrics may
                                                             exhibit low absolute values while the overall clustering
                                                             remains physically meaningful. This is expected to be
                                                             common in COLTRIMS data where quantum states ex-
FIG. 6: UMAP projection of the lower cluster in Fig. 5.      hibit inherent overlap in momentum space. For example,
   Separation of the data into two dication states is        the silhouette score of 0.13 observed in Fig. 3 reflects
   achieved. The calculated confidence score is 0.79.        the fact that several dication states share similar kine-
 Colors represent different dication states and are for      matic signatures (e.g., the 3 B1 and 1 B1 states both have
              visualization purposes only.                   peak KER ∼ 4.3 eV), resulting in genuinely overlapping
                                                             clusters in the UMAP projection. The confidence score
                                                             accounts for this by weighting multiple complementary
                                                             metrics—notably the Hopkins statistic (0.98 in Fig. 3),
      eV and a β of ∼ 143◦ . It is a strong contributor to
                                                             which indicates strong underlying clustering tendency de-
      the O(1 D) asymptote.
                                                             spite the modest silhouette value. The iterative refine-
  Cluster 7 (pink in Fig. 3, 19% of events): D2 O2+          ment workflow demonstrated in Section IV shows how
( A2 ) dissociating to D+ + D+ + O(3 P)
3                                                            progressively isolating clusters leads to improved confi-
                                                             dence scores (0.70→0.79) as overlapping states are sepa-
    • A triplet dication state with a peak KER of ∼ 8 eV     rated.
      and a β of ∼ 121◦ .

  Cluster 8 (light-green in Figs 3 - 6, 33.7% of events):
D2 O2+ (3 B2 ) dissociating to D+ + D+ + O(3 P)

    • A triplet dication state with a peak KER of ∼ 9.7
      eV and a β of ∼ 139◦ . It is a strong contributor to
      the O(3 P) asymptote.


                   3.     Quality Metrics

   SCULPT’s adaptive confidence scoring provided the
following assessment for the initial UMAP analysis in
Fig. 3. These values can vary slightly from run to run
due to the random sampling approach.

    • Overall confidence: 0.71 (High reliability)

    • Silhouette score: 0.1324
                                                               FIG. 7: UMAP projection of D2 O double ionization
    • Hopkins statistic: 0.9769                                data showing poor clustering resulting from selecting
                                                                 only KER, EESum and Total Energy as UMAP
    • Stability: 0.9996                                      features. The calculated confidence score is 0.14. Colors
                                                                   represent different dication states and are for
    • Physics consistency: 0.3184                                           visualization purposes only.
    • Calinski Harabasz: 2338.4791
                                                                                                                     13

                  V.   CONCLUSIONS                            tional manual analysis of the experimental data alone.
                                                                 Preliminary investigations using SCULPT indicate
   SCULPT represents a significant advance in the anal-       that the three clusters corresponding to these dication
ysis of multi-particle coincidence data from momentum         states exhibit varying degrees of overlap or separation
spectroscopy experiments. By combining modern ma-             in UMAP representations, depending on the choice of
chine learning techniques with physics-based parameters       correlated features. The agent will be tasked with au-
for dimensionality reduction, the software enables re-        tonomously analyzing these UMAP patterns in conjunc-
searchers to extract detailed information from highly-        tion with the digital-twin to identify shared characteris-
dimensional data more efficiently than previously estab-      tics among the clusters in feature space. This approach
lished analytical tools. We expect that SCULPT could          provides a data-driven pathway to detect events that vio-
also enable the identification and isolation of quantum       late the axial-recoil-approximation without relying on ab
states and dynamical mechanisms that could otherwise          initio calculations, and it enables the systematic identi-
be left hidden in congested momentum spectra. The             fication of non-axial fragmentation dynamics in complex
adaptive confidence scoring system provides quantitative      molecular systems that are beyond the reach of such so-
reliability assessments, addressing a critical need for ob-   phisticated theoretical methods.
jective quality metrics in exploratory data analysis.            In this regard As such, the SCULPT platform ex-
   The case study of D2 O double ionization demonstrates      emplifies a transformative approach to analyzing high-
SCULPT’s ability to identify subtle fragmentation chan-       dimensional tabulated data, with broad implications
nels, with several being diffuse or diluted by competing      across both fundamental science and industry. As and
processes, and discover non-intuitive feature combina-        outlook,We believe that this work lays the foundation
tions that enhance cluster separation. The web-based          for AI-driven discovery in multi-particle quantum dy-
implementation and modular architecture make the soft-        namics, emphasizing real-time, physics-informed anal-
ware accessible to the broader community while enabling       ysis of complex experimental datasets. In the long
customization for specific experimental requirements.         term, its modular, web-based architecture and adap-
                                                              tive clustering tools will not only accelerate insight in
                                                              COLTRIMS experiments but also potentially offer scal-
            VI.   FUTURE DIRECTIONS                           able solutions for applications and industries where un-
                                                              covering rare events and nonlinear correlations in large
   We have not utilized the entire spectrum of capabilities   tabulated multi-parameter datasets are critical, such as
and options of SCULPT in our analysis just yet. Near          quantum information science,[44] pharmaceuticals,[45–
future studies on different datasets will explore other       47] medicine,[48] aerospace. [49, 50] SCULPT can bridge
capabilities of SCULPT such as advanced data filter-          experimental physics with data-centric innovation, posi-
ing and the implementation of deep autoencoders. As           tioning itself as a model for cross-sector impact. We have
momentum spectroscopy techniques continue to be fur-          made SCULPT available on GitHub to encourage com-
ther developed, producing ever-larger and more complex        munity contributions and to ensure that the software can
datasets, tools like SCULPT will become essential for         evolve with the field’s needs.
extracting physical insights.
   The next development step will incorporate digital-
twin and agent-based capabilities. A digital-twin sim-                      ACKNOWLEDGMENTS
ulation module, based on a classical Newtonian disso-
ciation model, will predict experimental outcomes from           This work was supported by the Laboratory Di-
user input and/or outputs of the Data Analysis & Fea-         rected Research and Development (LDRD) program at
turization module. This module will guide the cluster-        Lawrence Berkeley National Laboratory. We acknowl-
ing process, and together they will form an interactive       edge the computational resources provided by the Ad-
machine-learning loop that supports the validation and        vanced Light Source and the National Energy Research
interpretation of measured results while identifying rele-    Scientific Computing Center (NERSC), which both are
vant features and underlying physical processes.              a DOE Office of Science User Facility under contract
   In particular, the agent will be employed to isolate       no. DE-AC02-05CH11231. In particular we acknowl-
and characterize dissociation dynamics in the concerted       edge NERSC award ERCAP-0031498. We also thank the
fragmentation pathway of water that remained inacces-         ALS Photon Science Computing Group for their valuable
sible using conventional, by-hand experimental analysis.      feedback.
Only detailed ab initio theoretical investigations revealed
that three of the eight water dication states exhibit non-
standard dissociation behavior associated with a break-
down of the axial-recoil-approximation. This behavior                        DATA AVAILABILITY
arises from a so-called “slingshot mechanism,” which in-
verts the kinematics of the reaction products [43]. No-         The data that support the findings of this study are
tably, this effect could not be identified through tradi-     available from the corresponding author upon reasonable
                                                                                                                                  14

request. Example datasets and tutorials are available at            https://github.com/AMOS-experiment/CoInML/.




 [1] R. Dörner, V. Mergel, O. Jagutzki, L. Spielberger, J. Ull-         J. Lasenby, J. Leskovec, T.-Y. Liu, A. Manrai, D. Marks,
     rich, R. Moshammer, and H. Schmidt-Böcking, Cold Tar-              B. Ramsundar, L. Song, J. Sun, J. Tang, P. Veličković,
     get Recoil Ion Momentum Spectroscopy: a ‘momentum                   M. Welling, L. Zhang, C. W. Coley, Y. Bengio, and
     microscope’ to view atomic collision dynamics, Physics              M. Zitnik, Scientific discovery in the age of artificial in-
     Reports 330, 95 (2000).                                             telligence, Nature 620, 47 (2023).
 [2] J. Ullrich, R. Moshammer, A. Dorn, R. D Rner, L. P. H.         [12] Z. Chen, N. Andrejevic, N. C. Drucker, T. Nguyen, R. P.
     Schmidt, and H. Schmidt-B Cking, Recoil-ion and elec-               Xian, T. Smidt, Y. Wang, R. Ernstorfer, D. A. Tennant,
     tron momentum spectroscopy: reaction-microscopes, Re-               M. Chan, and M. Li, Machine learning on neutron and x-
     ports on Progress in Physics 66, 1463 (2003).                       ray scattering and spectroscopies, Chemical Physics Re-
 [3] T. Jahnke, A. Czasch, M. Schöffler, S. Schössler,                 views 2, 031301 (2021).
     M. Käsz, J. Titze, K. Kreidi, R. E. Grisenti, A. Staudte,     [13] M. Hu, J. Fan, Y. Tong, Z. Sun, and H. Jiang, Deep
     O. Jagutzki, L. P. H. Schmidt, S. K. Semenov, N. A.                 learning for ultrafast X-ray scattering and imaging with
     Cherepkov, H. Schmidt-Böcking, and R. Dörner, Pho-                intense X-ray FEL pulses, Advanced Optical Technolo-
     toelectron and ICD electron angular distributions from              gies 14, 1546386 (2025).
     fixed-in-space neon dimers, Journal of Physics B: Atomic,      [14] H. Daoud, D. Sirohi, E. Mjeku, J. Feng, S. Oghbaey, and
     Molecular and Optical Physics 40, 2597 (2007).                      R. J. D. Miller, Novel applications of generative adver-
 [4] M. S. Schöffler, J. Titze, N. Petridis, T. Jahnke, K. Cole,        sarial networks (GANs) in the analysis of ultrafast elec-
     L. P. H. Schmidt, A. Czasch, D. Akoury, O. Jagutzki,                tron diffraction (UED) images, The Journal of Chemical
     J. B. Williams, N. A. Cherepkov, S. K. Semenov, C. W.               Physics 159, 044107 (2023).
     McCurdy, T. N. Rescigno, C. L. Cocke, T. Osipov, S. Lee,       [15] C. Zhao, W. Yu, and L. Li, Visualization of small-angle
     M. H. Prior, A. Belkacem, A. L. Landers, H. Schmidt-                X-ray scattering datasets and processing-structure map-
     Böcking, T. Weber, and R. Dörner, Ultrafast Probing of            ping of isotactic polypropylene films by machine learning,
     Core Hole Localization in N2 , Science 320, 920 (2008).             Materials & Design 228, 111828 (2023).
 [5] T. Weber, A. O. Czasch, O. Jagutzki, A. K. Müller,            [16] H. He, C. Liu, and H. Liu, Model Reconstruction from
     V. Mergel, A. Kheifets, E. Rotenberg, G. Meigs,                     Small-Angle X-Ray Scattering Data Using Deep Learning
     M. H. Prior, S. Daveau, A. Landers, C. L. Cocke,                    Methods, iScience 23, 100906 (2020).
     T. Osipov, R. Dı́ez Muiño, H. Schmidt-Böcking, and           [17] T. Chavez, Z. Zhao, R. Jiang, W. Koepp, D. McReynolds,
     R. Dörner, Complete photo-fragmentation of the deu-                P. H. Zwart, D. B. Allan, E. H. Gann, N. Schwarz,
     terium molecule, Nature 431, 437 (2004).                            D. Ushizima, E. S. Barnard, A. Mehta, S. Sankara-
 [6] K. Fehre, D. Trojanowskaja, J. Gatzke, M. Kunitski,                 narayanan, and A. Hexemer, A machine-learning-driven
     F. Trinter, S. Zeller, L. P. H. Schmidt, J. Stohner,                data labeling pipeline for scientific analysis in MLEx-
     R. Berger, A. Czasch, O. Jagutzki, T. Jahnke, R. Dörner,           change, Journal of Applied Crystallography 58, 731
     and M. S. Schöffler, Absolute ion detection efficiencies of        (2025).
     microchannel plates and funnel microchannel plates for         [18] W. M. Abdelmoula, B. G.-C. Lopez, E. C. Randall,
     multi-coincidence detection, Review of Scientific Instru-           T. Kapur, J. N. Sarkaria, F. M. White, J. N. Agar, W. M.
     ments 89, 045112 (2018).                                            Wells, and N. Y. R. Agar, Peak learning of mass spec-
 [7] P. V. Demekhin, S. D. Stoychev, A. I. Kuleff, and                   trometry imaging data using artificial neural networks,
     L. S. Cederbaum, Exploring Interatomic Coulombic De-                Nature Communications 12, 5544 (2021).
     cay by Free Electron Lasers, Physical Review Letters           [19] V. Bitto, P. Hönscheid, M. J. Besso, C. Sperling,
     107, 273002 (2011).                                                 I. Kurth, M. Baumann, and B. Brors, Enhancing mass
 [8] A. Czasch, M. Schöffler, M. Hattass, S. Schössler,                spectrometry imaging accessibility using convolutional
     T. Jahnke, T. Weber, A. Staudte, J. Titze, C. Wimmer,               autoencoders for deriving hypoxia-associated peptides
     S. Kammer, M. Weckenbrock, S. Voss, R. E. Grisenti,                 from tumors, npj Systems Biology and Applications 10,
     O. Jagutzki, L. P. H. Schmidt, H. Schmidt-Böcking,                 57 (2024).
     R. Dörner, J. M. Rost, T. Schneider, C.-N. Liu, I. Bray,      [20] L. McInnes, J. Healy, and J. Melville, UMAP: Uniform
     A. S. Kheifets, and K. Bartschat, Partial Photoionization           Manifold Approximation and Projection for Dimension
     Cross Sections and Angular Distributions for Double Ex-             Reduction (2020), arXiv:1802.03426 [stat].
     citation of Helium up to the N = 13 Threshold, Physical        [21] E. Becht, L. McInnes, J. Healy, C.-A. Dutertre, I. W. H.
     Review Letters 95, 243003 (2005).                                   Kwok, L. G. Ng, F. Ginhoux, and E. W. Newell, Dimen-
 [9] L. P. H. Schmidt, T. Jahnke, A. Czasch, M. Schöffler,              sionality reduction for visualizing single-cell data using
     H. Schmidt-Böcking, and R. Dörner, Spatial Imaging of             UMAP, Nature Biotechnology 37, 38 (2019).
     the H 2 + Vibrational Wave Function at the Quantum             [22] B. Szubert, J. E. Cole, C. Monaco, and I. Drozdov,
     Limit, Physical Review Letters 108, 073202 (2012).                  Structure-preserving visualisation of high dimensional
[10] Y. LeCun, Y. Bengio, and G. Hinton, Deep learning, Na-              single-cell datasets, Scientific Reports 9, 8914 (2019).
     ture 521, 436 (2015).                                          [23] F. Trozzi, X. Wang, and P. Tao, UMAP as a Dimension-
[11] H. Wang, T. Fu, Y. Du, W. Gao, K. Huang, Z. Liu,                    ality Reduction Tool for Molecular Dynamics Simulations
     P. Chandak, S. Liu, P. Van Katwyk, A. Deac, A. Anand-               of Biomacromolecules: A Comparison Study, The Jour-
     kumar, K. Bergen, C. P. Gomes, S. Ho, P. Kohli,                     nal of Physical Chemistry B 125, 5022 (2021).
                                                                                                                               15

[24] D. Bourilkov, Machine and deep learning applications in            36 (1990).
     particle physics, International Journal of Modern Physics     [38] L. Hubert and P. Arabie, Comparing partitions, Journal
     A 34, 1930019 (2019).                                              of Classification 2, 193 (1985).
[25] D. Guest, K. Cranmer, and D. Whiteson, Deep Learning          [39] T. Calinski and J. Harabasz, A dendrite method for clus-
     and Its Application to LHC Physics, Annual Review of               ter analysis, Communications in Statistics - Theory and
     Nuclear and Particle Science 68, 161 (2018).                       Methods 3, 1 (1974).
[26] J. Brehmer, S. Macaluso, D. Pappadopulo, and K. Cran-         [40] D. L. Davies and D. W. Bouldin, A Cluster Separation
     mer, Hierarchical clustering in particle physics through           Measure, IEEE Transactions on Pattern Analysis and
     reinforcement learning (2020), arXiv:2011.08191 [cs].              Machine Intelligence PAMI-1, 224 (1979).
[27] A. S. Venkatachalam, L. Greenman, J. Stallbaumer,             [41] O. Arbelaitz, I. Gurrutxaga, J. Muguerza, J. M. Pérez,
     A. Rudenko, D. Rolles, and H. V. S. Lam, enExploit-                and I. Perona, An extensive comparative study of cluster
     ing correlations in multi-coincidence Coulomb explosion            validity indices, Pattern Recognition 46, 243 (2013).
     patterns for differentiating molecular structures using       [42] M. Ester, H.-P. Kriegel, J. Sander, and X. Xu, A density-
     machine learning, Nature Communications 16, 11366                  based algorithm for discovering clusters in large spatial
     (2025).                                                            databases with noise, in Proceedings of the Second Inter-
[28] X. Li, T. Jahnke, R. Boll, J. Han, M. Xu, M. Meyer,                national Conference on Knowledge Discovery and Data
     M. N. Piancastelli, D. Rolles, A. Rudenko, F. Trinter,             Mining, KDD’96 (AAAI Press, Portland, Oregon, 1996)
     T. J. A. Wolf, J. B. Thayer, J. P. Cryan, S. Ermon, and            pp. 226–231.
     P. J. Ho, Generative Modeling Enables Molecular Struc-        [43] Z. L. Streeter, F. Yip, R. L. Lucchese, B. Gervais, T. N.
     ture Retrieval from Coulomb Explosion Imaging (2025),              Rescigno, and C. W. Mc McCurdy, Dissociation dynam-
     arXiv:2511.00179 [physics].                                        ics of the water dication following one-photon double ion-
[29] F.-A. Fortin, F.-M. De Rainville, M.-A. G. Gardner,                ization. I. Theory, Physical Review A 98, 10.1103/Phys-
     M. Parizeau, and C. Gagné, DEAP: evolutionary algo-               RevA.98.053429 (2018).
     rithms made easy, J. Mach. Learn. Res. 13, 2171 (2012).       [44] M. Sennary, J. Rivera-Dean, M. ElKabbash, V. Pervak,
[30] Plotly Technologies Inc., Collaborative Data Science               M. Lewenstein, and M. T. Hassan, Attosecond quan-
     (2015).                                                            tum uncertainty dynamics and ultrafast squeezed light
[31] N. Cherrier, J.-P. Poli, M. Defurne, and F. Sabatié, Con-         for quantum communication, Light: Science & Applica-
     sistent Feature Construction with Constrained Genetic              tions 14, 350 (2025).
     Programming for Experimental Physics, in 2019 IEEE            [45] J. A. Berlin, S. C. Glasser, and S. S. Ellenberg, Adverse
     Congress on Evolutionary Computation (CEC) (2019)                  Event Detection in Drug Development: Recommenda-
     pp. 1650–1658.                                                     tions and Obligations Beyond Phase 3, American Journal
[32] W. La Cava and J. H. Moore, Learning feature spaces for            of Public Health 98, 1366 (2008).
     regression with genetic programming, Genetic Program-         [46] C. Feng, L. Li, and A. Sadeghpour, A comparison of
     ming and Evolvable Machines 21, 433 (2020).                        residual diagnosis tools for diagnosing regression mod-
[33] N. Makke and S. Chawla, Interpretable scientific discov-           els for count data, BMC Medical Research Methodology
     ery with symbolic regression: a review, Artificial Intelli-        20, 175 (2020).
     gence Review 57, 2 (2024).                                    [47] A. V. Sadybekov and V. Katritch, Computational ap-
[34] D. Reedy, J. B. Williams, B. Gaire, A. Gatton, M. Weller,          proaches streamlining drug discovery, Nature 616, 673
     A. Menssen, T. Bauer, K. Henrichs, P. Burzynski,                   (2023).
     B. Berry, Z. L. Streeter, J. Sartor, I. Ben-Itzhak,           [48] Y. Huang, J. Li, M. Li, and R. R. Aparasu, Application
     T. Jahnke, R. Dörner, T. Weber, and A. L. Landers, Dis-           of machine learning in predicting survival outcomes in-
     sociation dynamics of the water dication following one-            volving real-world data: a scoping review, BMC Medical
     photon double ionization. II. Experiment, Physical Re-             Research Methodology 23, 268 (2023).
     view A 98, 053430 (2018).                                     [49] A. Srivastava, R. Akella, V. Diev, S. Kumaresan,
[35] P. J. Rousseeuw, Silhouettes: A graphical aid to the in-           D. McIntosh, E. Pontikakis, Zuobing Xu, and Yi
     terpretation and validation of cluster analysis, Journal of        Zhang, Enabling the Discovery of Recurring Anomalies
     Computational and Applied Mathematics 20, 53 (1987).               in Aerospace Problem Reports using High-Dimensional
[36] B. Hopkins and J. G. Skellam, A New Method for de-                 Clustering Techniques, in 2006 IEEE Aerospace Confer-
     termining the Type of Distribution of Plant Individuals,           ence (IEEE, Big Sky, MT, USA, 2006) pp. 1–17.
     Annals of Botany 18, 213 (1954).                              [50] V. M. Janakiraman and D. Nielsen, Anomaly detec-
[37] R. G. Lawson and P. C. Jurs, New index for clustering              tion in aviation data using extreme learning machines,
     tendency and its application to chemical problems, Jour-           in 2016 International Joint Conference on Neural Net-
     nal of Chemical Information and Computer Sciences 30,              works (IJCNN) (IEEE, Vancouver, BC, Canada, 2016)
                                                                        pp. 1993–2000.
