# Results — Detailed Analysis

This document expands on the headline numbers in the
top-level [`README.md`](../README.md), providing the per-residue and
per-pocket detail behind the design conclusions.

## 1. ZnPPIX designs

### 1.1 Energy convergence

8,500 decoys converge to a tight low-energy basin. The five lowest-scoring models
all fall within ~5 kcal/mol of each other:

| Rank | Decoy ID                       | Total score (kcal/mol) | Ligand RMSD (Å) |
| ---- | ------------------------------ | ---------------------- | --------------- |
| 1    | `11636339_cytbx_znh15_0101`    | −608.82                | 0.074           |
| 2    | `11636343_cytbx_znh19_0181`    | −607.08                | 0.071           |
| 3    | `11636326_cytbx_znh2_0305`     | −606.80                | 0.072           |
| 4    | `11636325_cytbx_znh1_0141`     | −606.20                | 0.098           |
| 5    | `11636343_cytbx_znh19_0058`    | −605.98                | 0.093           |

PDB coordinates for the five top models are available in
[`structures/top_designs/znh/`](../structures/top_designs/znh/), and the full score table
is in [`data/znh_score_rmsd.dat`](../data/znh_score_rmsd.dat).

### 1.2 Mutation pattern

Aligning the top five models with both control models and the wild-type CytbX sequence
([`figures/znh_alignment.png`](../figures/znh_alignment.png),
[`sequences/znh_top_models.fasta`](../sequences/znh_top_models.fasta)) reveals a small,
tightly conserved set of recurring substitutions:

- **F76 → T or R** — replaces a bulky hydrophobic with a polar/charged residue, presumably
  to satisfy the Zn-coordinated propionate side chains.
- **F97 → T / V / M** — relieves steric clash near the lower porphyrin face.
- **A100 → L** — packs against the porphyrin macrocycle.

The native histidine network (H10, H38, H68, H96) is preserved across all top models, even
though only H38 and H96 were locked in the resfile. This is one of the strongest indicators
that the protocol is finding *physical* low-energy solutions rather than artefacts.

### 1.3 Surprising coordination switch

The starting model places ZnPPIX between **H38** and **H96** (the original heme upper
binding site). After design, every top-scoring model has the cofactor *translated through
the bundle* and now bridging **H10** and **H68**, the alternative pair belonging to the
lower heme site.

This was unexpected because:

- The resfile *only* preserved H38 and H96; H10 and H68 were repackable but not specifically
  privileged.
- The ligand `Transform` mover allows ≤ 4 Å RMSD displacement, but nearly all top models
  remain at ≤ 0.1 Å ligand RMSD — i.e. once Rosetta finds the alternative pocket, it does
  so on the very first dock attempt and stays there.

The interpretation is that the **H10/H68 pocket is genuinely better suited to ZnPPIX**: the
Zn–N axial coordination geometry is identical to Fe–N in heme, but the surrounding hydrophobic
shell is slightly tighter in the lower pocket, giving improved van der Waals packing and a
deeper energy minimum. This is an unanticipated structural-biology result delivered by the
design protocol itself.

## 2. BCL designs

### 2.1 Energy convergence

The BCL run produces a wider score distribution (the cofactor has more degrees of freedom
because of the phytyl tail and the larger chlorin macrocycle), but again converges to a
clear top cluster:

| Rank | Decoy ID                       | Total score (kcal/mol) | Ligand RMSD (Å) |
| ---- | ------------------------------ | ---------------------- | --------------- |
| 1    | `11720711_cytbx_bcl5_0006`     | −593.23                | 0.098           |
| 2    | `11720713_cytbx_bcl7_0388`     | −592.11                | 0.097           |
| 3    | `11720724_cytbx_bcl16_0401`    | −590.99                | 0.087           |
| 4    | `11720721_cytbx_bcl13_0013`    | −590.35                | 0.106           |
| 5    | `11720711_cytbx_bcl5_0274`     | −590.07                | 0.101           |

Top-scoring PDBs are in
[`structures/top_designs/bcl/`](../structures/top_designs/bcl/) and the full score data in
[`data/bcl_score_rmsd.dat`](../data/bcl_score_rmsd.dat).

### 2.2 Mutation pattern

The alignment of the top five BCL designs with controls
([`figures/bcl_alignment.png`](../figures/bcl_alignment.png),
[`sequences/bcl_top_models.fasta`](../sequences/bcl_top_models.fasta)) yields a different
mutation signature:

- **A42 → H** — *unique to BCL*; introduces an additional histidine to the binding pocket,
  likely contributing an H-bond to the chlorin keto carbonyl.
- **F39 → V / I** — loosens the pocket to accommodate the larger macrocycle.
- **F76 → T** — convergent with the ZnPPIX run; serves as a polar partner.
- **A100 → L** — also convergent with ZnPPIX; packs against the macrocycle face.

### 2.3 Coordination switch — Mg²⁺ prefers oxygen

In the BCL run, the cofactor is *not* retained at any of the four CytbX histidines. Instead,
top models systematically displace BCL by **~10–15 Å** from the histidine cluster, into a
new pocket enriched in **Thr, Asn, and Ser** side chains.

This is consistent with the well-known coordination preference of Mg²⁺ for hard
oxygen-donor ligands (water, carbonyl, hydroxyl) over the softer nitrogen donors that Zn²⁺
and Fe²⁺ favour. Magnesium in chlorophyll a is itself coordinated by His or by water in
natural reaction centres, so a designed pocket that delivers an oxygen-rich coordination
shell is biologically plausible.

The BCL pocket also requires **23 residues within 3 Å** of the cofactor (vs. 13 for ZnPPIX)
— a direct consequence of the larger chlorin and the protruding phytyl tail.

## 3. Comparison to controls

In both runs, two **control models** (poorly scoring decoys, near the upper tail of the
score distribution) were retained as a baseline. Their sequences differ from the top
designs at exactly the residues identified above (F76, F97/A42, A100), and structurally
they:

- For ZnPPIX, leave the cofactor in the original H38/H96 pocket but with steric clashes
  unresolved.
- For BCL, retain the cofactor near the histidines despite the unsatisfied Mg²⁺ coordination.

The control sequences are at the bottom of each FASTA file in
[`sequences/`](../sequences/) and visible in the alignment PNGs.

## 4. Cross-cofactor convergence

A small but interesting set of mutations is convergent between the two design campaigns:

- **F76 → T** (both runs) — F76 sits at the periphery of both pockets and benefits from a
  polar substitution regardless of the cofactor.
- **A100 → L** (both runs) — improves macrocycle packing for either porphyrin or chlorin.

This suggests that part of the apo CytbX scaffold is *generally* suboptimal for tetrapyrrole
binding, and that improvement at these positions is independent of the metal centre. By
contrast, **F76R**, **F97 → T/V/M**, and **A42H** are cofactor-specific.

## 5. Limitations & caveats

- **No experimental validation.** All conclusions are computational. Wet-lab confirmation
  (expression, UV-Vis, EPR, crystallography) is the natural next step.
- **Single starting placement per cofactor.** A more thorough study would dock from multiple
  initial poses and assess whether the H10/H68 switch (ZnPPIX) or the oxygen-pocket switch
  (BCL) survive sampling diversification.
- **Fixed backbone except for a 7 Å minimisation shell.** Larger cofactors (BCL especially)
  may benefit from explicit backbone redesign or a flexible-backbone protocol such as
  `BackrubMover` or `FastRelax`.
- **Implicit membrane.** `franklin2019` represents the bilayer as a depth-dependent
  Lazaridis-style implicit solvent. A molecular-dynamics follow-up in an explicit POPC/POPE
  bilayer would be the natural validation step.
