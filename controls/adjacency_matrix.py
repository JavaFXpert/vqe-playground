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
from controls import number_picker


class AdjacencyMatrix(pygame.sprite.RenderPlain):
    """UI control for maintaining adjacency matrix"""
    def __init__(self, xpos, ypos, adj_matrix):
        pygame.sprite.RenderPlain.__init__(self, self.number_pickers_array)
        self.adj_matrix = adj_matrix
        self.xpos = xpos
        self.ypos = ypos

        self.number_pickers_array = self.create_number_pickers()
        self.arrange()

    def create_number_pickers_array(self):
        self.number_pickers_array = np.empty_like(self.adj_matrix, dtype=number_picker)

    def arrange(self):
        next_xpos = self.xpos
        next_ypos = self.ypos
        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.rect.left = next_xpos
            sprite.rect.top = next_ypos
            next_xpos += sprite.rect.width