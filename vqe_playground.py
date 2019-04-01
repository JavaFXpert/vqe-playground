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
# TODO: Add user interaction:
# TODO:   - Selecting circuit node with mouse
# TODO:   - Same gate twice erases (e.g. pressing X key already on an X gate erases it)
# TODO:     - If gate was rotated, make unrotated (e.g. pressing X on rotated X gate makes X)
# TODO: Use NUM_STATE_DIMS everywhere
# TODO: Fix weights on network graph
# TODO: Create UI component for adjacency matrix
# TODO: Use better looking fonts
# TODO: Modify NetworkGraph to:
# TODO:     - move vertices to each's side of the cut
# TODO: Make TSP and other demos, including chemistry
# TODO: Make displays update during optimization
# TODO: Modify optimizer to fit pluggable Aqua framework
# TODO: Create network graph component?
# TODO: Update QSphere visualization and leverage it here
#
"""Demonstrate Variational Quantum Eigensolver (VQE) concepts using Qiskit and Pygame"""

from pygame.locals import *
from qiskit import ClassicalRegister
from qiskit import execute
from qiskit_aqua.translators.ising import maxcut
from containers import *
from controls.circuit_grid import *
from model.circuit_grid_model import *
from utils.gamepad import *
from utils.states import NUM_QUBITS, NUM_STATE_DIMS
from viz.expectation_grid import ExpectationGrid
from viz.network_graph import NetworkGraph
from controls.adjacency_matrix import AdjacencyMatrix

WINDOW_SIZE = 1660, 1000


class VQEPlayground():
    """Main object for application"""
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.background = pygame.Surface(self.screen.get_size())
        self.circuit_grid_model = None
        self.circuit_grid = None
        self.top_sprites = None
        self.right_sprites = None
        self.expectation_grid = None
        self.network_graph = None
        self.adjacency_matrix = None
        self.optimization_desired = False

    def main(self):
        if not pygame.font: print('Warning, fonts disabled')
        if not pygame.mixer: print('Warning, sound disabled')

        pygame.init()

        pygame.joystick.init()
        num_joysticks = pygame.joystick.get_count()

        joystick = False
        if num_joysticks > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(WHITE)

        pygame.font.init()

        self.circuit_grid_model = CircuitGridModel(NUM_QUBITS, 19)

        pygame.display.set_caption('VQE Playground')

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Prepare objects
        clock = pygame.time.Clock()

        # self.circuit_grid_model.set_node(0, 1, CircuitGridNode(node_types.X))
        # self.circuit_grid_model.set_node(1, 1, CircuitGridNode(node_types.X))
        # self.circuit_grid_model.set_node(2, 1, CircuitGridNode(node_types.X))
        # self.circuit_grid_model.set_node(3, 1, CircuitGridNode(node_types.X))
        # self.circuit_grid_model.set_node(4, 1, CircuitGridNode(node_types.X))
        # self.circuit_grid_model.set_node(5, 1, CircuitGridNode(node_types.X))

        self.circuit_grid_model.set_node(0, 0, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(1, 0, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(2, 0, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(3, 0, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(4, 0, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(5, 0, CircuitGridNode(node_types.Y))

        self.circuit_grid_model.set_node(1, 1, CircuitGridNode(node_types.X, 0, 0))
        self.circuit_grid_model.set_node(2, 2, CircuitGridNode(node_types.X, 0, 1))
        self.circuit_grid_model.set_node(3, 3, CircuitGridNode(node_types.X, 0, 2))
        self.circuit_grid_model.set_node(4, 4, CircuitGridNode(node_types.X, 0, 3))
        self.circuit_grid_model.set_node(5, 5, CircuitGridNode(node_types.X, 0, 4))

        self.circuit_grid_model.set_node(0, 6, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(1, 6, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(2, 6, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(3, 6, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(4, 6, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(5, 6, CircuitGridNode(node_types.Y))

        self.circuit_grid_model.set_node(1, 7, CircuitGridNode(node_types.X, 0, 0))
        self.circuit_grid_model.set_node(2, 8, CircuitGridNode(node_types.X, 0, 1))
        self.circuit_grid_model.set_node(3, 9, CircuitGridNode(node_types.X, 0, 2))
        self.circuit_grid_model.set_node(4, 10, CircuitGridNode(node_types.X, 0, 3))
        self.circuit_grid_model.set_node(5, 11, CircuitGridNode(node_types.X, 0, 4))

        self.circuit_grid_model.set_node(0, 12, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(1, 12, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(2, 12, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(3, 12, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(4, 12, CircuitGridNode(node_types.Y))
        self.circuit_grid_model.set_node(5, 12, CircuitGridNode(node_types.Y))

        circuit = self.circuit_grid_model.compute_circuit()

        # adj_matrix = np.array([
        #     [0.0, 0.0, 4.0, 1.0, 0.0, 0.0],
        #     [0.0, 0.0, 0.0, 0.0, 3.0, 0.0],
        #     [4.0, 0.0, 0.0, 1.0, 1.0, 5.0],
        #     [1.0, 0.0, 1.0, 0.0, 2.0, 1.0],
        #     [0.0, 3.0, 1.0, 2.0, 0.0, 0.0],
        #     [0.0, 0.0, 5.0, 1.0, 0.0, 0.0]
        # ])

        initial_adj_matrix = np.array([
            [0.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 0.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 0.0]
        ])

        # adj_matrix = np.array([
        #     [0.0, 1.0, 0.0, 1.0],
        #     [1.0, 0.0, 1.0, 0.0],
        #     [0.0, 1.0, 0.0, 1.0],
        #     [1.0, 0.0, 1.0, 0.0]
        # ])

        # adj_matrix = np.array([
        #     [0.0, 1.0, 1.0, 1.0],
        #     [1.0, 0.0, 1.0, 0.0],
        #     [1.0, 1.0, 0.0, 1.0],
        #     [1.0, 0.0, 1.0, 0.0]
        # ])

        # adj_matrix = np.array([
        #     [0.0, 1.0, 1.0, 1.0],
        #     [1.0, 0.0, 1.0, 1.0],
        #     [1.0, 1.0, 0.0, 1.0],
        #     [1.0, 1.0, 1.0, 0.0]
        # ])

        maxcut_op, maxcut_shift = maxcut.get_maxcut_qubitops(initial_adj_matrix)
        # print("maxcut_op: ", maxcut_op, ", maxcut_shift: ", maxcut_shift)

        # TODO: Find different approach of calculating and retrieving diagonal
        maxcut_op._paulis_to_matrix()
        eigenvectors = maxcut_op._dia_matrix

        self.expectation_grid = ExpectationGrid(circuit, eigenvectors, maxcut_shift)

        self.adjacency_matrix = AdjacencyMatrix(1000, 63, initial_adj_matrix)

        self.network_graph = NetworkGraph(self.adjacency_matrix.adj_matrix_numeric)

        # TODO: Put this flag in expectation_grid, making methods to
        # TODO:     update respective matrices?
        # self.optimization_desired = True

        self.top_sprites = HBox(500, 0, self.network_graph)
        self.right_sprites = VBox(1400, 0, self.expectation_grid)

        self.circuit_grid = CircuitGrid(10, 500, self.circuit_grid_model)
        self.screen.blit(self.background, (0, 0))

        self.top_sprites.draw(self.screen)
        self.right_sprites.draw(self.screen)
        self.circuit_grid.draw(self.screen)
        self.adjacency_matrix.draw(self.screen)
        pygame.display.flip()

        gamepad_repeat_delay = 100
        gamepad_neutral = True
        gamepad_pressed_timer = 0
        gamepad_last_update = pygame.time.get_ticks()

        # Main Loop
        going = True
        while going:
            clock.tick(30)

            pygame.time.wait(10)

            if joystick:
                gamepad_move = False
                joystick_hat = joystick.get_hat(0)

                if joystick_hat == (0, 0):
                    gamepad_neutral = True
                    gamepad_pressed_timer = 0
                else:
                    if gamepad_neutral:
                        gamepad_move = True
                        gamepad_neutral = False
                    else:
                        gamepad_pressed_timer += pygame.time.get_ticks() - gamepad_last_update
                if gamepad_pressed_timer > gamepad_repeat_delay:
                    gamepad_move = True
                    gamepad_pressed_timer -= gamepad_repeat_delay
                if gamepad_move:
                    if joystick_hat == (-1, 0):
                        self.move_update_circuit_grid_display(MOVE_LEFT)
                    elif joystick_hat == (1, 0):
                        self.move_update_circuit_grid_display(MOVE_RIGHT)
                    elif joystick_hat == (0, 1):
                        self.move_update_circuit_grid_display(MOVE_UP)
                    elif joystick_hat == (0, -1):
                        self.move_update_circuit_grid_display(MOVE_DOWN)
                gamepad_last_update = pygame.time.get_ticks()

                # Check left thumbstick position
                # left_thumb_x = joystick.get_axis(0)
                # left_thumb_y = joystick.get_axis(1)

            # Handle Input Events
            for event in pygame.event.get():
                pygame.event.pump()

                # if event.type != MOUSEMOTION:
                #     print("event: ", event)
                if event.type == QUIT:
                    going = False

                elif event.type == MOUSEBUTTONDOWN:
                    for idx, picker in enumerate(self.adjacency_matrix.number_pickers_list):
                        if picker.rect.collidepoint(event.pos):
                            self.adjacency_matrix.handle_element_clicked(picker)
                            self.update_circ_viz()
                            if self.adjacency_matrix.adj_matrix_graph_dirty:
                                self.network_graph.set_adj_matrix(self.adjacency_matrix.adj_matrix_numeric)
                                self.adjacency_matrix.adj_matrix_graph_dirty = False
                                # TODO: Remove
                                self.expectation_grid.basis_state_dirty = True

                elif event.type == JOYBUTTONDOWN:
                    if event.button == BTN_A:
                        # Place X gate
                        self.circuit_grid.handle_input_x()
                        self.update_circ_viz()
                    elif event.button == BTN_X:
                        # Place Y gate
                        self.circuit_grid.handle_input_y()
                        self.update_circ_viz()
                    elif event.button == BTN_B:
                        # Place Z gate
                        self.circuit_grid.handle_input_z()
                        self.update_circ_viz()
                    elif event.button == BTN_Y:
                        # Place Hadamard gate
                        self.circuit_grid.handle_input_h()
                        self.update_circ_viz()
                    elif event.button == BTN_RIGHT_TRIGGER:
                        # Delete gate
                        self.circuit_grid.handle_input_delete()
                        self.update_circ_viz()
                    elif event.button == BTN_RIGHT_THUMB:
                        # Add or remove a control
                        self.circuit_grid.handle_input_ctrl()
                        self.update_circ_viz()

                elif event.type == JOYAXISMOTION:
                    # print("event: ", event)
                    if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) >= 0.95:
                        self.circuit_grid.handle_input_rotate(np.pi / 8)
                        self.update_circ_viz()
                    if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) <= -0.95:
                        self.circuit_grid.handle_input_rotate(-np.pi / 8)
                        self.update_circ_viz()
                    if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) <= -0.95:
                        self.circuit_grid.handle_input_move_ctrl(MOVE_UP)
                        self.update_circ_viz()
                    if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) >= 0.95:
                        self.circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                        self.update_circ_viz()

                elif event.type == KEYDOWN:
                    index_increment = 0
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key == K_a:
                        self.move_update_circuit_grid_display(MOVE_LEFT)
                    elif event.key == K_d:
                        self.move_update_circuit_grid_display(MOVE_RIGHT)
                    elif event.key == K_w:
                        self.move_update_circuit_grid_display(MOVE_UP)
                    elif event.key == K_s:
                        self.move_update_circuit_grid_display(MOVE_DOWN)
                    elif event.key == K_x:
                        self.circuit_grid.handle_input_x()
                        self.update_circ_viz()
                    elif event.key == K_y:
                        self.circuit_grid.handle_input_y()
                        self.update_circ_viz()
                    elif event.key == K_z:
                        self.circuit_grid.handle_input_z()
                        self.update_circ_viz()
                    elif event.key == K_h:
                        self.circuit_grid.handle_input_h()
                        self.update_circ_viz()
                    elif event.key == K_BACKSLASH:
                        self.circuit_grid.handle_input_delete()
                        self.update_circ_viz()
                    elif event.key == K_c:
                        # Add or remove a control
                        self.circuit_grid.handle_input_ctrl()
                        self.update_circ_viz()
                    elif event.key == K_UP:
                        # Move a control qubit up
                        self.circuit_grid.handle_input_move_ctrl(MOVE_UP)
                        self.update_circ_viz()
                    elif event.key == K_DOWN:
                        # Move a control qubit down
                        self.circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                        self.update_circ_viz()
                    elif event.key == K_LEFT:
                        # Rotate a gate
                        self.circuit_grid.handle_input_rotate(-np.pi/8)
                        self.update_circ_viz()
                    elif event.key == K_RIGHT:
                        # Rotate a gate
                        self.circuit_grid.handle_input_rotate(np.pi / 8)
                        self.update_circ_viz()
                    elif event.key == K_o:
                        self.optimization_desired = True

            if self.optimization_desired:
                self.expectation_grid.draw_expectation_grid()

                # TODO: Apply optimization
                rotation_gate_nodes = self.circuit_grid_model.get_rotation_gate_nodes()

                # initial_rotations = np.zeros(len(rotation_gate_nodes))
                initial_rotations = np.full(len(rotation_gate_nodes), np.pi)

                rotation_bounds = np.zeros((len(rotation_gate_nodes), 2))

                opt_rotations = self.optimize_rotations(self.expectation_value_objective_function,
                                                        initial_rotations, self.circuit_grid,
                                                        self.expectation_grid, rotation_gate_nodes)

                # print('opt_rotations: ', opt_rotations)

                cost, basis_state_str = self.expectation_grid.calc_expectation_value()
                print('cost: ', cost, 'basis_state_str: ', basis_state_str)


                solution = np.zeros(NUM_STATE_DIMS)
                for idx, char in enumerate(basis_state_str):
                    solution[idx] = int(char)

                self.network_graph.set_solution(solution)

                self.update_circ_viz()

                self.optimization_desired = False

            if self.expectation_grid.basis_state_dirty:
                cost, basis_state_str = self.expectation_grid.calc_expectation_value()

                solution = np.zeros(NUM_STATE_DIMS)
                for idx, char in enumerate(basis_state_str):
                    solution[idx] = int(char)

                self.network_graph.set_solution(solution)

                self.update_circ_viz()
                self.expectation_grid.basis_state_dirty = False

        pygame.quit()

    def optimize_rotations(self, objective_function, x0, circuit_grid, expectation_grid, rotation_gate_nodes):

        # Tries to be plug-compatible with scipy.optimize.fmin_l_bfgs_b
        optimization_epochs = 1
        move_radians = np.pi / 8

        optimized_rotations = np.copy(x0)

        # For each rotation this will be either 1 or -1, signifying direction of movement
        unit_direction_array = np.ones(len(optimized_rotations))

        min_distance = objective_function(optimized_rotations, circuit_grid, expectation_grid, rotation_gate_nodes)

        for epoch_idx in range(optimization_epochs):
            for rotations_idx in range(len(optimized_rotations)):
                cur_ang_rad = optimized_rotations[rotations_idx]
                proposed_cur_ang_rad = cur_ang_rad

                # Decide whether to increase or decrease angle
                unit_direction_array[rotations_idx] = 1
                if cur_ang_rad > np.pi:
                    unit_direction_array[rotations_idx] = -1
                proposed_cur_ang_rad += move_radians * unit_direction_array[rotations_idx]
                if 0.0 <= proposed_cur_ang_rad < np.pi * 2:
                    optimized_rotations[rotations_idx] = proposed_cur_ang_rad

                    temp_distance = objective_function(optimized_rotations, circuit_grid, expectation_grid, rotation_gate_nodes)
                    if temp_distance > min_distance:
                        # Moving in the wrong direction so restore the angle in the array and switch direction
                        optimized_rotations[rotations_idx] = cur_ang_rad
                        unit_direction_array[rotations_idx] *= -1
                    else:
                        # Moving in the right direction so use the proposed angle
                        cur_ang_rad = proposed_cur_ang_rad
                        min_distance = temp_distance

                    finished_with_while_loop = False
                    loop_iterations = 0
                    while not finished_with_while_loop:
                        loop_iterations += 1
                        proposed_cur_ang_rad += move_radians * unit_direction_array[rotations_idx]
                        if 0.0 <= proposed_cur_ang_rad < np.pi * 2:
                            optimized_rotations[rotations_idx] = proposed_cur_ang_rad
                            temp_distance = objective_function(optimized_rotations, circuit_grid, expectation_grid, rotation_gate_nodes)
                            if temp_distance > min_distance:
                                # Distance is increasing so restore the angle in the array and leave the loop
                                optimized_rotations[rotations_idx] = cur_ang_rad
                                finished_with_while_loop = True
                            elif loop_iterations > np.pi * 2 / move_radians:
                                print("Unexpected: Was in while loop over ",  loop_iterations, " iterations")
                                finished_with_while_loop = True
                            else:
                                # Distance is not increasing, so use the proposed angle
                                cur_ang_rad = proposed_cur_ang_rad
                                min_distance = temp_distance
                        else:
                            finished_with_while_loop = True
            # print('min_distance: ', min_distance)

            objective_function(optimized_rotations, circuit_grid, expectation_grid, rotation_gate_nodes)
            # print('exp_val: ', expectation_grid.calc_expectation_value())
        return optimized_rotations

    def expectation_value_objective_function(self, rotations_radians, circuit_grid,
                                             expectation_grid, rotation_gate_nodes):
        for idx in range(len(rotation_gate_nodes)):
            circuit_grid.rotate_gate_absolute(rotation_gate_nodes[idx], rotations_radians[idx])
            expectation_grid.set_circuit(circuit_grid.circuit_grid_model.compute_circuit())
            cost, basis_state = expectation_grid.calc_expectation_value()

            # print("rotations_radians: ", rotations_radians, ", cost: ", cost, ", basis_state: ", basis_state)
        return cost

    def update_circ_viz(self):
        self.screen.blit(self.background, (0, 0))
        circuit = self.circuit_grid_model.compute_circuit()
        self.expectation_grid.set_circuit(circuit)
        self.top_sprites.arrange()
        self.right_sprites.arrange()
        self.top_sprites.draw(self.screen)
        self.right_sprites.draw(self.screen)
        self.adjacency_matrix.arrange()
        self.adjacency_matrix.draw(self.screen)
        self.circuit_grid.draw(self.screen)
        pygame.display.flip()

    def move_update_circuit_grid_display(self, direction):
        self.circuit_grid.move_to_adjacent_node(direction)
        self.circuit_grid.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    VQEPlayground().main()
