from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from scripts.run_problem_3_hamiltonian_variant_candidates import run, summarize


def test_hamiltonian_variant_candidates_include_mixture_and_two_way(tmp_path: Path) -> None:
    args = argparse.Namespace(
        output_dir=tmp_path,
        seeds=[1],
        input_steps=[1],
        n_samples=8,
        sigma=0.10,
        angle_scale=float(np.pi),
        tau_min=0.05,
        tau_max=0.5,
        tau_points=2,
        theta_points=3,
        phi_points=4,
        second_tau_points=2,
        random_kick_angle_scales=[0.02, 0.05],
        min_mean_success=0.05,
        min_diversity=0.20,
    )

    rows = run(args)
    summaries = summarize(rows)
    methods = {row["method"] for row in rows}

    assert "continuous_postselection_reference" in methods
    assert "hamiltonian_then_random_final_kick" in methods
    assert "hamiltonian_two_way_postselection" in methods
    assert len(summaries) == 3
