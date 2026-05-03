# Sequences

FASTA files and Clustal Ω alignments for the top-scoring designs of each cofactor run.

## Files

| File                                                     | Description                                                  |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| [`znh_top_models.fasta`](znh_top_models.fasta)           | Top 5 ZnPPIX designs, 2 controls, and the wild-type sequence |
| [`bcl_top_models.fasta`](bcl_top_models.fasta)           | Top 5 BCL designs, 2 controls, and the wild-type sequence    |
| [`znh_alignment_clustal.txt`](znh_alignment_clustal.txt) | Clustal Ω alignment of the ZnPPIX FASTA                      |
| [`bcl_alignment_clustal.txt`](bcl_alignment_clustal.txt) | Clustal Ω alignment of the BCL FASTA                         |

The PNG renderings of these alignments (with conservation, quality and consensus tracks added in
Jalview) are committed alongside the README in
[`../figures/znh_alignment.png`](../figures/znh_alignment.png) and
[`../figures/bcl_alignment.png`](../figures/bcl_alignment.png).

## Sequence numbering

The wild-type CytbX sequence has 113 residues (M1–Q113). The four transmembrane segments span
residues 4–26, 32–52, 63–84 and 90–108 (see
[`../design/znh/cytbx_znh.span`](../design/znh/cytbx_znh.span)).

Histidines mentioned in the README and `docs/results.md`:

| Histidine | Position | Helix     | Role in native CytbX                                       |
| --------- | -------- | --------- | ---------------------------------------------------------- |
| H10       | 10       | TM-1      | Lower heme axial ligand (paired with H68)                  |
| H38       | 38       | TM-2      | Upper heme axial ligand (paired with H96, **resfile-locked**) |
| H68       | 68       | TM-3      | Lower heme axial ligand (paired with H10)                  |
| H96       | 96       | TM-4      | Upper heme axial ligand (paired with H38, **resfile-locked**) |
