from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
import matplotlib.pyplot as plt

# Use PySCF, a classical computational chemistry software
# package, to compute the one-body and two-body integrals in
# electronic-orbital basis, necessary to form the Fermionic operator
driver = PySCFDriver(
    atom='H .0 .0 .0; H .0 .0 0.735',   #equilibirum distance
    unit=DistanceUnit.ANGSTROM,
    basis='sto3g',
    charge=0,
    spin=0,
)
problem = driver.run()

# setup the qubit mapper
from qiskit_nature.second_q.mappers import ParityMapper, JordanWignerMapper

mapper = ParityMapper(num_particles=problem.num_particles)

# setup the classical optimizer for the VQE
from qiskit_algorithms.optimizers import L_BFGS_B, COBYLA, SLSQP

optimizer = L_BFGS_B()

# setup the estimator primitive for the VQE
from qiskit.primitives import Estimator

estimator = Estimator()

# setup the ansatz for VQE
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
ansatz = UCCSD(
    problem.num_spatial_orbitals,
    problem.num_particles,
    mapper,
    initial_state=HartreeFock(
        problem.num_spatial_orbitals,
        problem.num_particles,
        mapper,
    ),
)

#ansatz.decompose().draw("mpl", style="iqp")
#plt.show()

# set up our actual VQE instance
from qiskit_algorithms import VQE

vqe = VQE(estimator, ansatz, optimizer)
# ensure that the optimizer starts in the all-zero state which corresponds to
# the Hartree-Fock starting point
vqe.initial_point = [0.0] * ansatz.num_parameters

# prepare the ground-state solver and run it
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

algorithm = GroundStateEigensolver(mapper, vqe)

electronic_structure_result = algorithm.solve(problem)
electronic_structure_result.formatting_precision = 6
print(electronic_structure_result)


mapper = ParityMapper(num_particles=problem.num_particles)
fermionic_op = problem.hamiltonian.second_q_op()
qubit_jw_op = mapper.map(fermionic_op)
print(qubit_jw_op)
from qiskit.quantum_info import SparsePauliOp

H2_op = SparsePauliOp.from_list(
    [
        ("II", -1.052373245772859),
        ("IZ", 0.39793742484318045),
        ("ZI", -0.39793742484318045),
        ("ZZ", -0.01128010425623538),
        ("XX", 0.18093119978423156),
    ]
)
print('\n')
result = vqe.compute_minimum_eigenvalue(operator=H2_op)
print(result)