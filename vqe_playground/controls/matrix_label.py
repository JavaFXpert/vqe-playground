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
from cmath import isclose
from vqe_playground.utils.colors import WHITE, BLACK
from vqe_playground.utils.fonts import *


class MatrixLabel(pygame.sprite.Sprite):
    """Displays a label on the headers of a matrix"""
    def __init__(self, label, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.label = label
        self.width = width
        self.height = height

        self.image = None
        self.rect = None
        # self.background_color = WHITE
        self.background_color = BLACK
        self.font_color = BLACK
        self.font = ARIAL_36

        self.draw_matrix_label()

    def draw_matrix_label(self):
        self.image = pygame.Surface([self.width, self.height])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        text_surface = self.font.render(self.label, False, BLACK)
        text_xpos = (self.rect.width - text_surface.get_rect().width) / 2
        text_ypos = (self.rect.height - text_surface.get_rect().height) / 2
        self.image.blit(text_surface, (text_xpos, text_ypos))

