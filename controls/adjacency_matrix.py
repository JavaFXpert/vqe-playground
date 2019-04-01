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
from cmath import isclose
from controls.number_picker import NumberPicker
from controls.matrix_label import MatrixLabel
from utils.labels import NETWORK_GRAPH_NODES
from utils.fonts import ARIAL_36


class AdjacencyMatrix(pygame.sprite.RenderPlain):
    ELEMENT_WIDTH_HEIGHT = 48
    """UI control for maintaining adjacency matrix"""
    def __init__(self, xpos, ypos, adj_matrix_numeric):
        self.adj_matrix_numeric = adj_matrix_numeric
        self.xpos = xpos
        self.ypos = ypos

        self.adj_matrix_graph_dirty = False
        self.num_nodes = adj_matrix_numeric.shape[0]
        self.row_labels_list = self.create_row_labels_list()
        self.col_labels_list = self.create_col_labels_list()
        self.number_pickers_list = self.create_number_pickers_list()
        pygame.sprite.RenderPlain.__init__(self,
                                           self.row_labels_list,
                                           self.col_labels_list,
                                           self.number_pickers_list)
        self.arrange()

    def create_number_pickers_list(self):
        pickers = []
        for row in range(self.num_nodes):
            for col in range(self.num_nodes):
                pickers.append(NumberPicker(self.adj_matrix_numeric[row, col],
                                            self.ELEMENT_WIDTH_HEIGHT,
                                            self.ELEMENT_WIDTH_HEIGHT,
                                            row != col))
        return pickers

    def create_row_labels_list(self):
        row_labels = []
        for row in range(self.num_nodes):
            row_labels.append(MatrixLabel(NETWORK_GRAPH_NODES[row],
                                        self.ELEMENT_WIDTH_HEIGHT,
                                        self.ELEMENT_WIDTH_HEIGHT))
        return row_labels

    def create_col_labels_list(self):
        col_labels = []
        for col in range(self.num_nodes):
            col_labels.append(MatrixLabel(NETWORK_GRAPH_NODES[col],
                                        self.ELEMENT_WIDTH_HEIGHT,
                                        self.ELEMENT_WIDTH_HEIGHT))
        return col_labels

    def arrange(self):
        for col in range(self.num_nodes):
            col_label = self.col_labels_list[col]
            col_label.rect.left = self.xpos + (col + 1) * col_label.rect.width
            col_label.rect.top = self.ypos

        for row in range(self.num_nodes):
            row_label = self.row_labels_list[row]
            row_label.rect.left = self.xpos
            row_label.rect.top = self.ypos + (row + 1) * row_label.rect.height

        next_ypos = self.ypos + self.ELEMENT_WIDTH_HEIGHT
        for row in range(self.num_nodes):
            next_xpos = self.xpos + self.ELEMENT_WIDTH_HEIGHT
            for col in range(self.num_nodes):
                picker = self.number_pickers_list[row * self.num_nodes + col]
                picker.rect.left = next_xpos
                picker.rect.top = next_ypos
                next_xpos += picker.rect.width
            next_ypos += picker.rect.height

    def handle_element_clicked(self, picker):
        for idx, picker_in_list in enumerate(self.number_pickers_list):
            if picker == picker_in_list:
                row = idx // self.num_nodes
                col = idx % self.num_nodes
                if row != col:
                    if isclose(picker_in_list.number, 0):
                        picker_in_list.number = 1
                        self.adj_matrix_graph_dirty = True
                    elif picker_in_list.number < 3:
                        picker_in_list.number += 1
                    else:
                        picker_in_list.number = 0
                        self.adj_matrix_graph_dirty = True

                    picker_in_list.draw_number_picker()
                    self.adj_matrix_numeric[row, col] = picker_in_list.number

                    # Also update the other side
                    other_idx = col * self.num_nodes + row
                    other_picker = self.number_pickers_list[other_idx]
                    other_picker.number = picker_in_list.number
                    other_picker.draw_number_picker()
                    self.adj_matrix_numeric[col, row] = picker_in_list.number
