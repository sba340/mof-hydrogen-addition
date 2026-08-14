# MOF Hydrogen Addition

DFT-based analysis of hydrogen addition and water adsorption in metal-organic frameworks, using VASP.

## Contents

| Notebook | Description |
|---|---|
| `notebooks/mof_hydrogen_addition.ipynb` | [Describe: DFT setup / structures / analysis for H addition on the MOF surface] |
| `notebooks/bader_charge_analysis.ipynb` | Bader charge analysis for CuTA and MgTA metal-triazolate MOFs, comparing hydrated vs. dehydrated structures to quantify charge redistribution on water adsorption |

## Repository structure

```
mof-hydrogen-addition/
├── README.md
├── notebooks/
│   ├── mof_hydrogen_addition.ipynb
│   └── bader_charge_analysis.ipynb
├── data/
│   ├── cuta/
│   │   ├── POSCAR_hydr
│   │   ├── POSCAR_dehy
│   │   ├── ACF_hydr_CuTA.dat
│   │   └── ACF_dehy_CuTA.dat
│   └── mgta/
│       ├── POSCAR_hydr
│       ├── POSCAR_dehy
│       ├── ACF_hydr_MgTA.dat
│       └── ACF_dehy_MgTA.dat
└── results/
    ├── cuta_charges_comparison.csv
    └── mgta_charges_comparison.csv
```

## Bader charge analysis

`notebooks/bader_charge_analysis.ipynb` reads VASP `POSCAR` structures and Henkelman-group `ACF.dat` Bader charge output, computes net atomic charge (formal valence − Bader charge) for each atom, and compares hydrated vs. dehydrated structures. It reports:

- A per-element mean net-charge comparison table (dehydrated vs. hydrated, with the difference)
- Per-atom charge detail for matched atoms across the two states
- Charges for water atoms present only in the hydrated structure
- A summary CSV per system, written to `results/`

**Requirements:** `numpy`, `pandas`

**To run:** place the four input files for each system (`POSCAR_hydr`, `POSCAR_dehy`, `ACF_hydr_<name>.dat`, `ACF_dehy_<name>.dat`) in `data/cuta/` or `data/mgta/`, then run the notebook top to bottom. Formal valences are set per system in the `CuTA` and `MgTA` cells — verify these against `ZVAL` in each system's `OUTCAR` before trusting the results, since they depend on the VASP pseudopotentials used.

## Requirements

- Python 3
- `numpy`, `pandas`
- VASP output: `POSCAR`, Bader `ACF.dat` (via the Henkelman group's Bader charge analysis code)

## Notes

This repository accompanies ongoing DFT work on ligand passivation, water adsorption, and phase behavior in metal-organic framework systems.
