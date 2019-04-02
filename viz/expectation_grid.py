#!/usr/bin/env python
#
# Copyright 2019 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pygame
import numpy as np
from qiskit import BasicAer, execute
from qiskit_aqua.translators.ising import maxcut
from utils.colors import WHITE, BLACK
from utils.fonts import ARIAL_36
from utils.states import comp_basis_states, NUM_QUBITS, NUM_STATE_DIMS


class ExpectationGrid(pygame.sprite.Sprite):
    """Displays a grid that contains basis states, eigenvalues, and probabilities"""
    def __init__(self, circuit, adj_matrix):
        pygame.sprite.Sprite.__init__(self)
        self.eigenvalues = None
        self.maxcut_shift = None
        self.image = None
        self.rect = None
        self.basis_states = comp_basis_states(NUM_QUBITS)
        self.quantum_state = None
        self.cur_basis_state_idx = 0
        self.basis_state_dirty = False

        # When setting circuit this first time,
        # don't calculate the expectation value
        # or draw the expectation grid, as the
        # adjacency matrix hasn't yet been supplied
        self.set_circuit(circuit, recalc=False)
        self.set_adj_matrix(adj_matrix)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit, recalc=True):
        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim)
        result_sim = job_sim.result()
        self.quantum_state = result_sim.get_statevector(circuit, decimals=3)

        if recalc:
            self.calc_expectation_value()
            self.draw_expectation_grid()

    def set_adj_matrix(self, adj_matrix):
        maxcut_op, self.maxcut_shift = maxcut.get_maxcut_qubitops(adj_matrix)
        # print("maxcut_op: ", maxcut_op, ", maxcut_shift: ", maxcut_shift)

        # TODO: Find different approach of calculating and retrieving diagonal
        maxcut_op._paulis_to_matrix()
        self.eigenvalues = maxcut_op._dia_matrix

        self.calc_expectation_value()
        self.draw_expectation_grid()

    def draw_expectation_grid(self):
        self.image = pygame.Surface([(NUM_QUBITS + 1) * 50 + 100, 100 + NUM_STATE_DIMS * 50])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        block_size = 26
        x_offset = 250
        y_offset = 10
        for y in range(NUM_STATE_DIMS):
            text_surface = ARIAL_36.render(self.basis_states[y] + ":  " + str(self.eigenvalues[y] + self.maxcut_shift), False, (0, 0, 0))
            self.image.blit(text_surface, (x_offset, (y + 1) * block_size + y_offset))

            prop_square_side = abs(self.quantum_state[y]) * block_size
            rect = pygame.Rect(x_offset + 20 - (prop_square_side / 2) + NUM_QUBITS * 30,
                               y * block_size + 35 + ((block_size - prop_square_side) / 2),
                               prop_square_side,
                               prop_square_side)
            if abs(self.quantum_state[y]) > 0:
                pygame.draw.rect(self.image, BLACK, rect, 2)

    def calc_expectation_value(self):
        statevector_probs = np.absolute(self.quantum_state) ** 2
        exp_val = np.sum(self.eigenvalues * statevector_probs)

        basis_state_idx = np.argmax(statevector_probs)

        if basis_state_idx != self.cur_basis_state_idx:
            self.basis_state_dirty = True
            self.cur_basis_state_idx = basis_state_idx

        # print ("in calc_expectation_value, exp_val: ", exp_val, ", basis state: ", self.basis_states[basis_state_idx])
        return exp_val, self.basis_states[basis_state_idx]

