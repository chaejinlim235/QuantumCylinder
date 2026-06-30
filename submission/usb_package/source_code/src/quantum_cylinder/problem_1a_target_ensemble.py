"""Default Problem 1(a) target ensemble implementation.

The current baseline uses the Qiskit implementation. The original NumPy matrix
implementation is preserved under `implementations/numpy/`.
"""

from quantum_cylinder.implementations.qiskit.problem_1a_target_ensemble import target_ensemble, target_state_circuit

__all__ = ["target_ensemble", "target_state_circuit"]
