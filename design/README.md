# Design files

Rosetta protocols and cluster job scripts used in this study.

## Layout

| Subfolder      | Contents                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------- |
| [`znh/`](znh/) | Full ZnPPIX design protocol (RosettaScripts XML, span file, resfile, flag file, SLURM script) |
| [`bcl/`](bcl/) | BCL design flag file and SLURM script                                                         |

## ZnPPIX (`znh/`)

| File                                                       | Purpose                                              |
| ---------------------------------------------------------- | ---------------------------------------------------- |
| [`ZNH_ligand.xml`](znh/ZNH_ligand.xml)                     | RosettaScripts protocol (movers, scoring, packing)   |
| [`cytbx_znh_flags.txt`](znh/cytbx_znh_flags.txt)           | Rosetta command-line flags                           |
| [`cytbx_znh_resfile.txt`](znh/cytbx_znh_resfile.txt)       | Resfile defining mutable / fixed positions           |
| [`cytbx_znh.span`](znh/cytbx_znh.span)                     | Membrane spanfile (4 transmembrane segments)         |
| [`cytbx_znh.sh`](znh/cytbx_znh.sh)                         | SLURM array-job script for BlueCrystal4              |

## BCL (`bcl/`)

| File                                                       | Purpose                                              |
| ---------------------------------------------------------- | ---------------------------------------------------- |
| [`cytbx_bcl_flags.txt`](bcl/cytbx_bcl_flags.txt)           | Rosetta command-line flags                           |
| [`cytbx_bcl.sh`](bcl/cytbx_bcl.sh)                         | SLURM array-job script for BlueCrystal4              |

The BCL protocol re-uses the same RosettaScripts XML topology as ZnPPIX with the ligand
chain swapped — the corresponding `BCL_ligand.xml` should be derived from
[`znh/ZNH_ligand.xml`](znh/ZNH_ligand.xml) by replacing `ZNH` with `BCL`. The shared spanfile
([`znh/cytbx_znh.span`](znh/cytbx_znh.span)) is reused since the protein backbone is identical.

## Regenerating ligand parameter files

`ZNH.params` and `BCL.params` are intentionally *not* committed because they are tightly coupled
to the specific Rosetta build. Regenerate them locally:

```bash
$ROSETTA/main/source/scripts/python/public/molfile_to_params.py \
    -n ZNH --keep-names \
    ../structures/cofactors/ZNH.mol2

$ROSETTA/main/source/scripts/python/public/molfile_to_params.py \
    -n BCL --keep-names \
    ../structures/cofactors/BCL.mol2
```

Place the resulting `.params` files in the same directory as the corresponding flag file before
launching Rosetta.

## Running the protocol

```bash
# from inside design/znh/
sbatch cytbx_znh.sh
```

The array contains 20 tasks. Increase `-nstruct` in the flag file (or re-submit) to scale up;
the production runs in this study generated 8,500 decoys for the ZnPPIX target and 10,000 for
the BCL target.
