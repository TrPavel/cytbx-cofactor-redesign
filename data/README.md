# Data

Per-decoy scoring tables produced by the Rosetta design runs.

## Files

| File                                            | Run    | Decoys | Notes                                                |
| ----------------------------------------------- | ------ | -----: | ---------------------------------------------------- |
| [`znh_score_rmsd.dat`](znh_score_rmsd.dat)      | ZnPPIX |  8,500 | Whitespace-delimited; 3 columns                      |
| [`bcl_score_rmsd.dat`](bcl_score_rmsd.dat)      | BCL    | 10,000 | Whitespace-delimited; 3 columns                      |
| [`znh_energy_rmsd.xlsx`](znh_energy_rmsd.xlsx)  | ZnPPIX | 8,500  | Excel workbook with the same data plus pivot summaries |
| [`bcl_energy_rmsd.xlsx`](bcl_energy_rmsd.xlsx)  | BCL    | 10,000 | Excel workbook with the same data plus pivot summaries |

## File format (`.dat`)

Each line is one decoy:

```text
<total_score (kcal/mol)>   <ligand_RMSD (Å)>   <decoy_id>
```

For example:

```text
-608.816   0.074   11636339cytbx_znh15_0101
-607.077   0.071   11636343cytbx_znh19_0181
-606.799   0.072   11636326cytbx_znh2_0305
```

`decoy_id` encodes `<SLURM_JOBID>cytbx_<cofactor><array_task_id>_<decoy_index>` and matches the
silent-file decoy tag.

## Loading

```python
import numpy as np
score, rmsd = np.loadtxt("znh_score_rmsd.dat", usecols=(0, 1), unpack=True)
```

The reproducibility script
[`../scripts/plot_energy_landscapes.py`](../scripts/plot_energy_landscapes.py) reads these files
to regenerate the energy-landscape figures in [`../figures/`](../figures/).
