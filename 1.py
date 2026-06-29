import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

N = 100
sigma = 0.10 

S_0 = []

for i in range(N):
    qc = QuantumCircuit(2)
    
    for q in range(2):
        delta_y = np.random.normal(0, sigma)
        delta_z = np.random.normal(0, sigma)
        
        qc.ry(delta_y, q)
        qc.rz(delta_z, q)
    
    state = Statevector.from_instruction(qc)
    S_0.append(state)

print(f"앙상블 S_0 크기: {len(S_0)}")
print(f"첫 번째 샘플의 상태 벡터: \n{S_0[0].data}")