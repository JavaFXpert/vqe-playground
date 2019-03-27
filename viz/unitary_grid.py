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
# DEVELOPER NOTE: The displayed transition (stochastic) matrix is the transposed unitary matrix
#
import pygame
import numpy as np
from qiskit import BasicAer, execute

from utils.colors import *
from utils.fonts import *
from utils.states import PITCH_STATE_NAMES, NUM_QUBITS, NUM_STATE_DIMS


class UnitaryGrid(pygame.sprite.Sprite):
    """Displays a unitary matrix grid"""
    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.basis_states = PITCH_STATE_NAMES
        self.unitary = None
        self.desired_stochastic_matrix = np.zeros((2 ** NUM_QUBITS, 2 ** NUM_QUBITS))
        self.set_circuit(circuit)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit):
        backend_unit_sim = BasicAer.get_backend('unitary_simulator')
        job_sim = execute(circuit, backend_unit_sim)
        result_sim = job_sim.result()

        self.unitary = result_sim.get_unitary(circuit, decimals=3).transpose()
        # self.desired_matrix = np.zeros((len(self.unitary), len(self.unitary)))
        # print('unitary: ', unitary)

        self.draw_unitary_grid(None, None)

        print('in set_circiut, mse: ', self.cost_desired_vs_unitary())

    def draw_unitary_grid(self, init_bit_str, meas_bit_str):
        self.image = pygame.Surface([100 + len(self.unitary) * 50, 100 + len(self.unitary) * 50])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        block_size = 30
        x_offset = 50
        y_offset = 50
        for y in range(len(self.unitary)):
            text_surface = ARIAL_30.render(self.basis_states[y], False, (0, 0, 0))
            text_surface.convert()
            self.image.blit(text_surface,(x_offset, (y + 1) * block_size + y_offset))
            for x in range(len(self.unitary)):
                text_surface = ARIAL_30.render(self.basis_states[x], False, (0, 0, 0))
                text_surface.convert()
                self.image.blit(text_surface, ((x + 1) * block_size + x_offset, y_offset))
                rect = pygame.Rect((x + 1) * block_size + x_offset,
                                   (y + 1) * block_size + y_offset,
                                   abs(self.unitary[y][x]) * block_size,
                                   abs(self.unitary[y][x]) * block_size)
                if abs(self.unitary[y][x]) > 0:
                    pygame.draw.rect(self.image, BLACK, rect, 1)
                    if init_bit_str and meas_bit_str:
                        if y == int(init_bit_str, 2) and x == int(meas_bit_str, 2):
                            pygame.draw.rect(self.image, BLACK, rect, 5)

                # Draw where touched on Roli Block
                if self.desired_stochastic_matrix[y][x] != 0:
                    radius = int(self.desired_stochastic_matrix[y][x] * 8)
                    x_pos = int((x + 1) * block_size + x_offset + (block_size / 2))
                    y_pos = int((y + 1) * block_size + y_offset + (block_size / 2))
                    circle_color = pygame.Color(0, 0, 255)
                    pygame.draw.circle(self.image, circle_color, (x_pos, y_pos), radius)

    def highlight_measured_state(self, init_bit_str, meas_bit_str):
        self.draw_unitary_grid(init_bit_str, meas_bit_str)

    def cost_desired_vs_unitary(self):
        mse = np.square(self.desired_stochastic_matrix -
                        np.square(np.abs(self.unitary))).mean()
        return mse

    def zero_desired_unitary(self):
        self.desired_stochastic_matrix = np.zeros((2 ** NUM_QUBITS, 2 ** NUM_QUBITS))

    """Make sum of matrix equal number of quantum state dimensions"""
    def normalize_desired_unitary(self):
        matrix_sum = self.desired_stochastic_matrix.sum()
        if matrix_sum != 0:
            scale_factor = NUM_STATE_DIMS / matrix_sum * 2
            self.desired_stochastic_matrix *= scale_factor
            print("desired_matrix.sum(): ", self.desired_stochastic_matrix.sum())
        else:
            print("desired_matrix.sum() was 0")


