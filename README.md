# Nise Formation Reservoir Characterization & Dynamic Flow Simulation

Static-to-dynamic reservoir characterization of the Upper Cretaceous deep marine Nise Formation on the eastern Vøring Margin, Norwegian Sea: 
Petrophysical interpretation of 4 wells, a custom-built 3D geological grid, and gas flow simulation across 3 well-placement scenarios. 
Estimated Gas-in-Place: **320 million Sm³**.

This repository contains the original Python grid-generation script and OPM Flow simulation decks behind my MSc thesis at NTNU 
(Department of Geoscience and Petroleum). Graded A and supervised by NTNU and Equinor.

## Why the Nise Formation

The Nise Formation lies stratigraphically above most of the producing Jurassic fields on the Eastern Vøring Margin of the Norwegian Sea (Halten Terrace, Nordland Ridge) and is penetrated by a large share of ongoing exploration in the area, yet it has received very little dedicated characterization. 
Additionally, it has a regulatory dimension: wells passing through the Nise in hydrocarbon zones require effective plugging and abandonment to prevent gas migration into the well-casing annulus. Hence, its flow behavior matters beyond exploration upside alone.

![Structural map of the study area](https://github.com/lindahafrifa-code/Nise-Formation-Reservoir-Characterization-and-Flow-Simulation/blob/main/images/structural_map.png)

## Data & tools

•	Well log and core data for 4 wells: 6407/1-4, 6407/4-1, 6407/2-1 in the Halten Terrace, and 6610/3-1 in the Vestfjorden Basin, were obtained from NPD/DISKOS. 

•	Petrophysical interpretation (shale volume, porosity, water saturation, permeability, cut offs and net reservoir) was performed in Interactive Petrophysics (IP).

•	The 3D geological grid (2,250,000 cells) was built from scratch in Python (NumPy, GSTools, Matplotlib). 

•	Dynamic simulation was run in OPM Flow, the open-source reservoir simulator co-developed by Equinor, and the results were visualized in ResInsight. 

•	PVT and relative permeability data are from Equinor's Open Database License dataset.

**Note on data**: well-completion reports and raw LAS files were downloaded from DISKOS under confidentiality terms and aren't redistributed here. 
Seismic interpretation was used to constrain fan geometry and dimensions during the geological modelling process but is not included in this repository due to confidentiality restrictions.
Core photos are public-domain NPD material (NPD, 2024a) and are used below with that attribution. 
Everything else in this repository (code, simulation decks, and derived figures) is either original or carries an explicit open license.

## Tying core to log: defining the channel and lobe architecture

Lithofacies were first described from core photographs; lithology, grain size, sorting, and sedimentary structure. 
Then calibrated against the gamma-ray and resistivity log responses. 
This calibration allowed the same channel and lobe motifs to be recognized in the uncored well intervals.

![Core-to-log calibration for a channel interval](images/fig02_channel_core_log_calibration.png)
A blocky, cylindrical gamma-ray motif over a 3-4m interval in Well 6610/3-1 calibrates to a channel fill in core. The F3-C sandstone subfacies consist of poorly to well-sorted, fine to medium to coarse-grained, amalgamated white to dark grey sandstones. The F2 lithofacies are heterolithics of thin sandstone/siltstone layers (≤ 0.05 meters thick) interbedded with predominantly dark grey to black mudstones, exhibiting varying levels of bioturbation .

![Core-to-log calibration for a lobe interval](images/fig03_lobe_core_log_calibration.png)
A coarsening-upward "funnel" gamma-ray trend over an 8 m interval in the same well calibrates to a lobe complex, with F1-hemipelagic mudstone- capping an upward transition through F2 into F3-C sandstone. The F1 are 0.01-0.2m thick dark grey to black mudstone observed in the cores. The F2 heterolithics are thin sandstone/siltstone layers, whiles F3 lithofacies are sandstones. 

![Lithofacies thickness by well](images/lithofacies_thickness_per_well.png)
Lithofacies thickness varies considerably across the three cored wells. 6407/1-4 is dominated by heterolithics (F2), whereas 6610/3-1 shows the most extensive channel-to-lobe sandstone development. The dynamic model's channel and lobe dimensions are informed by well 6610/3-1 and the published analogs to reduce model uncertainty.

## Workflow

![Methodology workflow](images/fig05_methodology_workflow.png)

## Building the model

Petrel seismic interpretation showed the Nise fan system on the Eastern Vøring Margin was made up of moderately sized fans, a key input for the model's lateral geometry. 
Channel and lobe architectural elements (sand-bearing) were dimensioned using 3 key analog studies of the Frysjaodden Formation (Norway), the Karoo Basin (South Africa), and the Jaca and Ainsa Basins (Spain), and seismic interpretation (confidential), because the four wells alone couldn't constrain the lateral extent.
[`scripts/createGrid.py`](python/createGrid.py) builds a 150×300×50 cell grid (30m×100m×1m per cell) containing two stacked lobes and a feeder channel, assigns porosity through a Gaussian random field centered on facies-specific means (0.20 in the channel, 0.15 in the lobes), and derives permeability through a power-law fit calibrated against the IP well-log analysis (10-121 mD across the model).

![Reservoir realization grid](images/fig06_reservoir_realization_grid.png)

![ResInsight 3D model with well locations](images/fig07_resinsight_3d_model.png)

## Dynamic simulation & results

3 single-well scenarios in [`simulation/`](simulation/) test how placement affects recoverable gas: PROD A sits on the channel/lobe axis, PROD B is off-axis through two lobes, and PROD C sits at a lobe fringe near the gas-water contact. Each was run independently; the other two wells were shut. Initial pressure was 210 bar against a 190 bar BHP constraint, with no aquifer drive, over one year of production.
![Remaining gas-in-place](images/fig08_gas_in_place.png)

| Well | Position | Year-end cumulative production | Recovery factor |
|---|---|---|---|
| PROD A | Channel/lobe axis | 2.25 MMSm³ | 1.0% |
| PROD B | Two lobes, off-axis | 1.13 MMSm³ | 0.4% |
| PROD C | Lobe fringe, near GWC | 0.54 MMSm³ | 0.17% |

![PROD A production curve](images/fig09_prod_a_curve.png)

![PROD B production curve](images/fig10_prod_b_curve.png)

![PROD C production curve](images/fig11_prod_c_curve.png)

PROD A produced roughly four times PROD C's total, tracking the permeability and porosity falloff away from the channel axis (18–25% porosity and 50–121 mD in the channel versus 9–20% and 10–62 mD in the lobes). 
PROD C still produced a meaningful volume despite sitting at the lobe fringe, which points to the channel-lobe system staying hydraulically connected even where individual architectural elements are weaker on their own.
PROD C's position in a water-bearing zone illustrates a risk the thesis discussion highlights directly: upflank gas can still migrate into wells positioned in water zones, 
a finding relevant to plugging and abandonment planning for existing Nise penetrations.

## Key Results
• Average reservoir porosity approximately 15%

• Reservoir permeability ranging from approximately 10 mD to over 100 mD

• Thin-bedded turbidite architecture creates significant heterogeneity and compartmentalisation

• Simulations indicate the Nise Formation on the Eastern Vøring Margin can store significant hydrocarbon volumes and deliver producible gas rates

• Reservoir architecture may provide migration pathways and has implications for future well plug and abandonment activities

## Decisions & trade-offs

•	Object-based facies modeling was used instead of a pixel-based approach to tie channel and lobe geometry directly to a depositional concept (Walker's submarine fan model) rather than to a generic statistical texture. 

•	Where the four wells couldn't constrain lateral geometry, dimensions were borrowed from published analogs and Petrel seismic interpretation; a standard approach for sparse subsurface data, but one that carries irreducible uncertainty the model doesn't capture on its own. 

•	OPM Flow was chosen for both access and because it's the same open-source engine that Equinor develops and runs internally. 

•	The three scenarios are single-well, one-year runs rather than a full multi-well depletion schedule, enough to compare placement sensitivity, not enough to forecast field-level economics; that's a natural next step.

## Limitations

Four wells and three cores is a thin dataset for a formation this heterogeneous, and the lateral continuity assumptions lean on analogs rather than local data. 
A fuller assessment would bring in more wells, longer simulation horizons, and a proper sensitivity sweep on the analog-derived geometry parameters.

## Reproducing this

```bash
pip install numpy matplotlib gstools
python python/createGrid.py                # writes PORO.INC, PERM.INC, FIPNUM.INC
flow simulation/TWOPHASE3D_GAS_A.DATA      # requires OPM Flow; swap in _B or _C for the other scenarios
```

`PORO.INC`, `PERM.INC`, and `FIPNUM.INC` are regenerated rather than stored in this repo — each is 2,250,000 lines of raw per-cell values.

## Software and Tools

| Discipline                 | Software                      |
| -------------------------- | ----------------------------- |
| Petrophysical Analysis     | Interactive Petrophysics (IP) |
| Seismic & Geological Modelling       | Petrel                        |
| Stochastic Modelling       | Python, GSTools               |
| Reservoir Simulation       | OPM Flow                      |
| Result Visualisation       | ResInsight                    |



## Skills Demonstrated
• Reservoir Characterization • Petrophysical Interpretation • Core Description and Facies Analysis • Seismic interpretation • Geological Modelling • Stochastic Property Modelling
• Python for Geoscience Applications • Reservoir Simulation • Uncertainty Assessment • Technical Communication

## Background

MSc Thesis: *"Reservoir Characterization and Hydrocarbon Flow Potential of the Upper Cretaceous Nise Formation: Halten Terrace and Nordland Ridge, Offshore Mid-Norway"* (January 2025). 
Supervised by Arve Næss (Equinor) and Carl Fredrik Berg (NTNU). Full thesis available on request.

[LinkedIn](https://www.linkedin.com/in/linda-afrifa)
