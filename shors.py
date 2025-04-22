#qiskit has a built-in Shor's algorithm implementation
from qiskit_aqua_algorithms import Shor

# Factor N = 15
shor = Shor(N=15)
result = shor.run()
print("Factors:", result['factors'])

