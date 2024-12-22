from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='1eed55196e8d2e774cb9392e0d30a1c2541e55b15be9d77518f7b9375a5516c760d48d30d9e06d3fc2233b5d2bde5518f99b13a1afdb320208337194ae616ba6'
)
job = service.job('ct5yd5w3b8m0008bvxd0')
job_result = job.result()

for idx, pub_result in enumerate(job_result):
    print(f"Expectation values for pub {idx}: {pub_result.data.evs}")