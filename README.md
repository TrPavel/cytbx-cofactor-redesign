# Computational Design of Functional Artificial Membrane Proteins

Computational redesign of the de novo membrane protein **CytbX** to specifically bind two novel cofactors — **Zinc Protoporphyrin IX (ZnPPIX)** and **Bacteriochlorophyll A (BCL)** — using Rosetta protein design software.

> 📄 Research project completed at the **University of Bristol**, School of Biochemistry.  
> Supervised by **Dr. Paul Curnow**.

---

## Overview

CytbX is a de novo designed four-helix bundle membrane protein originally engineered to bind b-type heme cofactors. This project explored whether the CytbX scaffold could be computationally repurposed to accommodate structurally and chemically distinct cofactors:

- **Zinc Protoporphyrin IX (ZnPPIX)** — structurally similar to heme but with zinc replacing iron, relevant to biosensing and photodynamic therapy.
- **Bacteriochlorophyll A (BCL)** — a larger, more complex cofactor with magnesium coordination, critical in photosynthetic energy transfer.

<p align="center">
  <img src="figures/cytbx_structure.png" alt="CytbX Structure" width="600"/>
  <br>
  <em>Figure 1: Structure of CytbX coordinating two b-type heme cofactors (cyan) within its four-helix bundle.</em>
</p>

---

## Approach

1. **Cofactor preparation** — Generated 50 conformers per cofactor using the Frog2 web server, converted to Rosetta-compatible parameter files.
2. **Manual placement** — Positioned each cofactor into the apo-CytbX binding pocket using PyMOL, mimicking the orientation of the original heme groups.
3. **Computational redesign** — Used RosettaScripts with the `franklin2019` membrane protein score function. Residues within 3Å of each cofactor were designated as mutable; key histidine residues (His10, His38, His68, His96) were preserved.
4. **Production runs** — ~8,500 models for ZnPPIX and 10,000 models for BCL on the BlueCrystal4 HPC cluster.
5. **Analysis** — Energy vs. RMSD landscape evaluation, multiple sequence alignment (Clustal Omega + Jalview), structural analysis in PyMOL.

---

## Key Results

### Zinc Protoporphyrin IX (ZnPPIX)

| Metric | Value |
|---|---|
| Initial energy score | +857.97 kcal/mol |
| Best design score | −608.82 kcal/mol |
| Energy improvement | ~1,466 kcal/mol |
| Top design RMSD | 0.074 Å |
| Sequence convergence | >94% identity among top models |

**Key mutations:** F76T/R, F97T/V/M, A100L

**Surprising finding:** Rosetta consistently preferred coordination at the **His10/His68** binding pocket over the initially targeted His38/His96 site — discovering a more energetically favorable binding mode.

<p align="center">
  <img src="figures/znh_energy_landscape.png" alt="ZnPPIX Energy Landscape" width="500"/>
  <br>
  <em>Energy vs. RMSD plot for ZnPPIX designs showing a clear energy funnel.</em>
</p>

<p align="center">
  <img src="figures/znh_binding_comparison.png" alt="ZnPPIX Binding Comparison" width="600"/>
  <br>
  <em>Comparison of best-scoring (green, pink, orange) and worst-scoring (red, yellow) ZnPPIX designs.</em>
</p>

### Bacteriochlorophyll A (BCL)

| Metric | Value |
|---|---|
| Initial energy score | +5,144.30 kcal/mol |
| Best design score | −593.23 kcal/mol |
| Energy improvement | ~5,737 kcal/mol |
| Top design RMSD | 0.098 Å |
| Sequence convergence | >94% identity among top models |

**Key mutations:** A42H (BCL-specific), F39V/I, F76T, A100L

**Key insight:** BCL designs showed significant cofactor repositioning away from histidine coordination sites, favoring an oxygen-rich environment with polar residues (Thr, Asn, Ser) — consistent with magnesium's coordination preferences.

<p align="center">
  <img src="figures/bcl_energy_landscape.png" alt="BCL Energy Landscape" width="500"/>
  <br>
  <em>Energy vs. RMSD plot for BCL designs.</em>
</p>

<p align="center">
  <img src="figures/bcl_binding_comparison.png" alt="BCL Binding Comparison" width="600"/>
  <br>
  <em>Comparison of BCL positioning across best-scoring and control models.</em>
</p>

---

## Cofactor-Specific Coordination Strategies

| Feature | ZnPPIX (Zinc) | BCL (Magnesium) |
|---|---|---|
| Preferred coordination | Histidine-based (His10/His68) | Oxygen-rich (Thr, Asn, Ser) |
| Key unique mutation | F76R (polar functionality) | A42H (additional H-bonding) |
| Cofactor repositioning | Shifted to alternative His pocket | Displaced ~10–15 Å from His sites |
| Binding pocket residues | 13 within 3 Å | 23 within 3 Å |

---

## Tools & Technologies

- **Rosetta 3.71** — Protein design and scoring (RosettaScripts, RosettaLigand)
- **PyMOL** — Molecular visualization and cofactor placement
- **Frog2** — Ligand conformer generation
- **Clustal Omega** — Multiple sequence alignment
- **Jalview** — Alignment visualization
- **BlueCrystal4 HPC** — University of Bristol high-performance computing cluster

---

## Repository Structure

```
├── README.md
├── figures/
│   ├── cytbx_structure.png
│   ├── znh_conformers.png
│   ├── znh_energy_landscape.png
│   ├── znh_binding_comparison.png
│   ├── bcl_energy_landscape.png
│   └── bcl_binding_comparison.png
└── report/
    └── research_report.pdf
```

---

## Full Report

The complete research report with detailed methodology, results, and discussion is available in [`report/research_report.pdf`](report/Computational%20Design%20(no%20first%20page).pdf).

---

## Acknowledgments

- **Dr. Paul Curnow** — Supervisor, University of Bristol
- **Advanced Computing Research Centre (ACRC)** — BlueCrystal4 HPC access
- **School of Biochemistry, University of Bristol**
