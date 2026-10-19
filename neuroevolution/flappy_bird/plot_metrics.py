"""Plots the training metrics from metrics.csv.

    python -m neuroevolution.flappy_bird.plot_metrics [path/to/metrics.csv]
"""
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / 'metrics.csv'
    rows = load(path)
    if not rows:
        print(f'No data in {path} - has the training started yet?')
        return

    generation = [int(r['generation']) for r in rows]
    score = [int(r['score']) for r in rows]
    highscore = [int(r['highscore']) for r in rows]
    best = [float(r['best_fitness']) for r in rows]
    mean = [float(r['mean_fitness']) for r in rows]
    mean_pipes = [float(r['mean_pipes']) for r in rows]

    fig, (ax_score, ax_fitness) = plt.subplots(2, 1, sharex=True, figsize=(9, 6))

    ax_score.plot(generation, score, marker='o', markersize=3, linewidth=1, label='Score')
    ax_score.plot(generation, highscore, linestyle='--', label='Highscore')
    ax_score.plot(generation, mean_pipes, label='Mean pipes (whole population)')
    ax_score.set_ylabel('Pipes passed')
    ax_score.legend()
    ax_score.grid(alpha=0.3)

    ax_fitness.plot(generation, best, label='Best fitness')
    ax_fitness.plot(generation, mean, label='Mean fitness')
    ax_fitness.set_xlabel('Generation')
    ax_fitness.set_ylabel('Frames survived')
    ax_fitness.legend()
    ax_fitness.grid(alpha=0.3)

    fig.suptitle(f'Neuroevolution - {len(rows)} generations')
    fig.tight_layout()
    out = path.with_suffix('.png')
    fig.savefig(out, dpi=120)
    print(f'saved: {out}')
    plt.show()


if __name__ == '__main__':
    main()
