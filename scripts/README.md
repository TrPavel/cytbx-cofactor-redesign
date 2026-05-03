# Scripts

Reproducibility helpers used to regenerate figures and summary statistics from the
score data committed under [`../data/`](../data/).

## Available scripts

| Script                                                       | Purpose                                                                                  |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| [`plot_energy_landscapes.py`](plot_energy_landscapes.py)     | Reads `data/{znh,bcl}_score_rmsd.dat` and writes the energy-landscape figures used in `../README.md`. |

## Setup

```bash
python -m pip install -r requirements.txt
```

## Running

```bash
# from the repository root
python scripts/plot_energy_landscapes.py
```

Outputs are written to [`../figures/znh_energy_landscape.png`](../figures/znh_energy_landscape.png)
and [`../figures/bcl_energy_landscape.png`](../figures/bcl_energy_landscape.png).
