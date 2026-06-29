from __future__ import annotations

from pathlib import Path

from submission.problem1_random_unitary_scrambling import solve_problem_1
from submission.problem2_hamiltonian_projection import solve_problem_2
from submission.problem3_continuous_measurement_denoising import solve_problem_3


def test_submission_layer_does_not_import_development_package():
    submission_dir = Path(__file__).resolve().parents[1] / "submission"
    for path in submission_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "quantum_cylinder" not in text
        assert 'ROOT / "src"' not in text


def test_simple_submission_layer_smoke(tmp_path):
    problem1 = solve_problem_1(
        tmp_path / "problem1",
        n_samples=8,
        random_steps=2,
    )
    assert problem1["summary"].exists()
    assert problem1["plot"].exists()
    assert len(problem1["rows"]) == 3
    assert len(problem1["metric_rows"]) == 3
    assert len(problem1["resource_rows"]) == 3
    assert (tmp_path / "problem1" / "problem1_target_summary.csv").exists()
    assert (tmp_path / "problem1" / "problem1_target_samples.csv").exists()
    assert (tmp_path / "problem1" / "problem1_metric_checks.csv").exists()
    assert (tmp_path / "problem1" / "problem1_random_unitary_resources.csv").exists()

    problem2 = solve_problem_2(
        tmp_path / "problem2",
        n_samples=8,
        random_steps=2,
        time_points=3,
    )
    assert problem2["summary"].exists()
    assert len(problem2["rows"]) == 3
    assert len(problem2["resource_rows"]) == 2

    problem3 = solve_problem_3(
        tmp_path / "problem3",
        n_samples=8,
        random_steps=2,
        input_steps=[1],
        tau_points=3,
        theta_points=5,
        phi_points=6,
    )
    assert problem3["summary"].exists()
    assert len(problem3["rows"]) == 1
    assert problem3["overall"] in {"use_as_main", "fallback_only", "do_not_use_as_main"}
