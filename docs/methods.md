# Methods

This document expands on the methodology summary in the top-level
[`README.md`](../README.md), giving the parameter-level detail required to
reproduce the design runs.

## 1. Starting model

The design template is the X-ray-derived model of CytbX, a four-helix-bundle de novo membrane
protein engineered to bind two b-type heme groups
([`structures/starting/cytbx.pdb`](../structures/starting/cytbx.pdb)). For redesign, the heme
groups were stripped to give an apo scaffold
([`structures/starting/cytbx_no_heme.pdb`](../structures/starting/cytbx_no_heme.pdb)), and the
target cofactor was manually placed in the binding pocket using PyMOL, oriented to mimic the
positions of the original hemes. The resulting bound complexes are
[`structures/starting/cytbx_znh.pdb`](../structures/starting/cytbx_znh.pdb) and
[`structures/starting/cytbx_bcl.pdb`](../structures/starting/cytbx_bcl.pdb).

## 2. Cofactor preparation

For each cofactor:

1. The reference structure was downloaded from the PDB Chemical Component Dictionary in
   `mol2`/`sdf`/`cif` form ([`structures/cofactors/`](../structures/cofactors/)).
2. **Conformer libraries** of up to 50 conformers per cofactor were generated using the
   [Frog2 web server](https://mobyle2.rpbs.univ-paris-diderot.fr/portal.py?form=Frog2) and saved
   as multi-model PDB files
   ([`ZNH_conformers.pdb`](../structures/cofactors/ZNH_conformers.pdb),
   [`BCL_conformers.pdb`](../structures/cofactors/BCL_conformers.pdb)).
3. **Rosetta parameter files** (`ZNH.params`, `BCL.params`) were generated with
   `molfile_to_params.py` from the Rosetta tools distribution. *These are not committed to
   the repository because Rosetta-generated `.params` files are tightly coupled to the local
   Rosetta version; regenerate them locally before re-running the protocol.*

## 3. Membrane definition

A 4-segment spanfile was derived from the X-ray topology and is committed at
[`design/znh/cytbx_znh.span`](../design/znh/cytbx_znh.span):

```text
4 113
antiparallel
n2c
    4   26
   32   52
   63   84
   90  108
```

The same spanfile was reused for the BCL run (the protein backbone is shared).

## 4. Mutable interface

The resfile [`design/znh/cytbx_znh_resfile.txt`](../design/znh/cytbx_znh_resfile.txt) defines:

- All residues default to `NATAA` (repackable, no mutation).
- **H38, H96** and **L50** are locked as `NATRO` (no rotamer movement) — these include the two
  histidines that originally coordinate the upper heme axial site, plus a structural leucine.
- **Ten interface positions** (18, 21, 24, 42, 76, 79, 82, 83, 97, 100) are designated `ALLAAxC`
  — any amino acid is allowed except cysteine.

The `DetectProteinLigandInterface` task operation in the RosettaScripts XML further extends the
mutable shell concentrically: positions within 6 Å are designed, 6–8 Å are repacked, 8–10 Å are
held fixed but minimised, and beyond 12 Å are held fully fixed.

## 5. RosettaScripts protocol

The full protocol XML is [`design/znh/ZNH_ligand.xml`](../design/znh/ZNH_ligand.xml). The high-level
ordering is:

1. `AddMembraneMover` — instantiates the implicit membrane.
2. `MembranePositionFromTopologyMover` — orients the protein in the membrane.
3. `FavorNativeResidue` (bonus = 1.00) — adds a small per-residue bonus for retaining the
   wild-type identity, so mutations are only proposed when they yield a clear energetic gain.
4. `Transform` — low-resolution ligand docking inside a 20 Å box (500 cycles, 1 Å translation
   step, 5° rotation step, T = 5).
5. `HighResDocker` — high-resolution side-chain repacking around the docked ligand
   (`ligand_soft_rep` score function, 6 cycles, repack every 3rd cycle).
6. `PackRotamersMover` — full design pass on the interface (`ligand` hard-rep score function).
7. `FinalMinimizer` — gradient minimisation of the side chains and a 7 Å backbone shell
   (Cα restraints = 0.3) under the hard-rep scorefunction.
8. `InterfaceScoreCalculator` — separates protein–ligand interaction energy from total score.

A flat `ClassicGrid` (50 Å, vdW weight = 1.0) is used for the ligand-grid scoring during docking.

## 6. Scoring and flag files

The Rosetta command-line flags are committed alongside each XML
([`design/znh/cytbx_znh_flags.txt`](../design/znh/cytbx_znh_flags.txt),
[`design/bcl/cytbx_bcl_flags.txt`](../design/bcl/cytbx_bcl_flags.txt)). Notable settings:

- `-mp:scoring:hbond true` — explicit membrane-aware hydrogen-bonding term.
- `-mp:lipids:has_pore false` — disable water-channel modelling.
- `-relax:jump_move true` — allow rigid-body movement of the ligand jump during relax.
- `-packing:pack_missing_sidechains 0` — don't try to add absent side chains.
- `-linmem_ig 20` — linear-memory interaction graph, scaled at 20.
- `-extra_res_fa ZNH.params` — load the cofactor parameter file.
- `-qsar:grid_dir grids` — directory in which to materialise the QSAR/scoring grids.

Score function: **`franklin2019`** — a membrane-protein-aware re-fit of the Talaris score
function (Alford *et al.*, 2019).

## 7. Production runs

Each cofactor was run as a SLURM array job on **BlueCrystal4** (University of Bristol ACRC).
The job script for ZnPPIX is [`design/znh/cytbx_znh.sh`](../design/znh/cytbx_znh.sh):

```bash
#SBATCH --array=1-20
#SBATCH --time=3-0:0:00
#SBATCH --mem=5GB
srun rosetta_scripts.serialization.linuxgccrelease @cytbx_znh_flags.txt \
  -out:suffix $SLURM_ARRAY_TASK_ID \
  -out:prefix $SLURM_JOBID \
  -out:file:silent struct_500_$SLURM_ARRAY_TASK_ID \
  -out:path:all output
```

The combined yields after silent-file consolidation were:

- **ZnPPIX run**: 8,500 successfully scored decoys.
- **BCL run**: 10,000 successfully scored decoys.

Score and ligand-RMSD pairs are committed in
[`data/znh_score_rmsd.dat`](../data/znh_score_rmsd.dat) and
[`data/bcl_score_rmsd.dat`](../data/bcl_score_rmsd.dat) (one decoy per line:
`total_score`  `ligand_RMSD`  `decoy_id`).

## 8. Post-processing

1. **Filtering.** Decoys were ranked by `total_score`; the top 0.5 % were extracted as silent files
   and converted back to PDB.
2. **Clustering & visualisation** in PyMOL (per-run `.pse` sessions are referenced in
   the report appendices).
3. **Multiple sequence alignment** of the top 5 designs + 2 control models + the wild-type sequence
   using **Clustal Ω** (output:
   [`sequences/znh_alignment_clustal.txt`](../sequences/znh_alignment_clustal.txt),
   [`sequences/bcl_alignment_clustal.txt`](../sequences/bcl_alignment_clustal.txt)).
4. **Conservation rendering** in **Jalview** (PNGs:
   [`figures/znh_alignment.png`](../figures/znh_alignment.png),
   [`figures/bcl_alignment.png`](../figures/bcl_alignment.png)).
5. **Energy-vs-RMSD plotting** with `matplotlib` — see
   [`scripts/plot_energy_landscapes.py`](../scripts/plot_energy_landscapes.py).
