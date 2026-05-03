"""Plot energy vs. RMSD landscapes for ZnPPIX and BCL design runs.

Reads the Rosetta score-and-RMSD data files in ``data/`` and writes the
resulting figures into ``figures/``. Each figure pairs a 2D density plot
of ligand RMSD vs. total Rosetta score with a histogram of the score
distribution, highlighting the lowest-energy (best) design.

Usage:
    python scripts/plot_energy_landscapes.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
FIG_DIR = REPO_ROOT / "figures"


def load_scores(path: Path) -> tuple[np.ndarray, np.ndarray]:
    scores, rmsds = [], []
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            scores.append(float(parts[0]))
            rmsds.append(float(parts[1]))
        except ValueError:
            continue
    return np.array(scores), np.array(rmsds)


def plot_landscape(
    score: np.ndarray,
    rmsd: np.ndarray,
    title: str,
    out_path: Path,
    accent: str,
) -> None:
    score_lo, score_hi = np.percentile(score, [0.5, 99.5])
    score_pad = (score_hi - score_lo) * 0.05
    score_range = (score_lo - score_pad, score_hi + score_pad)

    fig = plt.figure(figsize=(10, 5), dpi=140)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.6, 1.0], wspace=0.3)
    ax_scatter = fig.add_subplot(gs[0, 0])
    ax_hist = fig.add_subplot(gs[0, 1])

    hb = ax_scatter.hexbin(
        rmsd,
        score,
        gridsize=45,
        cmap="viridis",
        mincnt=1,
        extent=(rmsd.min(), rmsd.max(), score_range[0], score_range[1]),
    )
    cb = fig.colorbar(hb, ax=ax_scatter, pad=0.02)
    cb.set_label("Models per bin", fontsize=9)

    best_idx = int(np.argmin(score))
    ax_scatter.scatter(
        rmsd[best_idx],
        score[best_idx],
        s=110,
        facecolor="white",
        edgecolor=accent,
        linewidth=2.0,
        zorder=5,
        label=f"Best: {score[best_idx]:.2f} kcal/mol\n@ RMSD {rmsd[best_idx]:.3f} Å",
    )

    ax_scatter.set_xlabel("Ligand RMSD (Å)", fontsize=11)
    ax_scatter.set_ylabel("Rosetta Total Score (kcal/mol)", fontsize=11)
    ax_scatter.set_title(title, fontsize=12, pad=8)
    ax_scatter.grid(True, linestyle="--", alpha=0.25)
    ax_scatter.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax_scatter.set_ylim(score_range)

    ax_hist.hist(
        score,
        bins=80,
        range=score_range,
        orientation="horizontal",
        color=accent,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.3,
    )
    ax_hist.axhline(score[best_idx], color="black", linestyle="--", linewidth=1)
    ax_hist.set_xlabel("Model count", fontsize=11)
    ax_hist.set_title("Score distribution", fontsize=11, pad=8)
    ax_hist.grid(True, linestyle="--", alpha=0.25, axis="x")
    ax_hist.set_ylim(score_range)
    ax_hist.tick_params(labelleft=False)

    fig.text(
        0.01,
        0.01,
        f"n = {len(score):,} models",
        fontsize=9,
        color="#444",
    )

    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)

    runs = [
        {
            "name": "ZnPPIX",
            "data": DATA_DIR / "znh_score_rmsd.dat",
            "out": FIG_DIR / "znh_energy_landscape.png",
            "title": "ZnPPIX Designs — Energy vs. Ligand RMSD",
            "accent": "#1f7a8c",
        },
        {
            "name": "BCL",
            "data": DATA_DIR / "bcl_score_rmsd.dat",
            "out": FIG_DIR / "bcl_energy_landscape.png",
            "title": "Bacteriochlorophyll A Designs — Energy vs. Ligand RMSD",
            "accent": "#a23b72",
        },
    ]

    for run in runs:
        score, rmsd = load_scores(run["data"])
        plot_landscape(score, rmsd, run["title"], run["out"], run["accent"])
        print(
            f"{run['name']}: n={len(score):,} | "
            f"best={score.min():.2f} | mean={score.mean():.2f} | "
            f"saved {run['out'].relative_to(REPO_ROOT)}"
        )


if __name__ == "__main__":
    main()
