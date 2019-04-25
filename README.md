# Variational Quantum Eigensolver Playground

Variational Quantum Eigensolver (VQE) Playground: Gaining intuition about VQE.
(based on [Qiskit](https://qiskit.org/), the "Quantum Information Science Kit")

**License:** Apache 2.0

## Running locally from a command prompt

Requires pip installing qiskit-aqua, qiskit, matplotlib, and pygame. Then run
`vqe_start.py` using Python 3.

## Running locally after installing as a Python package

Installing this Python package registers an entry point `vqe-playground`.
Running it starts a pygame based graphical interface.

## Running on CoCalc

You have to create an environment for graphical applications via an `*.x11` file,
see [Graphical Application](https://doc.cocalc.com/x11.html).
You can also open the file [cocalc.x11](./cocalc.x11), which launches this application automatically.
Otherwise, run `vqe-playground` in the terminal.
