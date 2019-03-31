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
from controls.number_picker import NumberPicker


class AdjacencyMatrix(pygame.sprite.RenderPlain):
    """UI control for maintaining adjacency matrix"""
    def __init__(self, xpos, ypos, adj_matrix_numeric):
        self.adj_matrix_numeric = adj_matrix_numeric
        self.xpos = xpos
        self.ypos = ypos

        self.num_nodes = adj_matrix_numeric.shape[0]
        self.number_pickers_list = self.create_number_pickers_list()
        pygame.sprite.RenderPlain.__init__(self, self.number_pickers_list)
        self.arrange()

    def create_number_pickers_list(self):
        pickers = []
        for row in range(self.num_nodes):
            for col in range(self.num_nodes):
                pickers.append(NumberPicker(self.adj_matrix_numeric[row, col], 64, 64))
        return pickers

    def arrange(self):
        next_ypos = self.ypos
        for row in range(self.num_nodes):
            next_xpos = self.xpos
            for col in range(self.num_nodes):
                picker = self.number_pickers_list[row * self.num_nodes + col]
                picker.rect.left = next_xpos
                picker.rect.top = next_ypos
                next_xpos += picker.rect.width
            next_ypos += picker.rect.height

        # next_xpos = self.xpos
        # next_ypos = self.ypos
        # sprite_list = self.sprites()
        # for sprite in sprite_list:
        #     sprite.rect.left = next_xpos
        #     sprite.rect.top = next_ypos
        #     next_xpos += sprite.rect.width