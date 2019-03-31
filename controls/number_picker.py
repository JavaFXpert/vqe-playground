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
from utils.colors import WHITE, BLACK
from utils.fonts import *


class NumberPicker(pygame.sprite.Sprite):
    """Displays a number that may be modified by clicking and dragging"""
    def __init__(self, number, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.number = None
        self.width = width
        self.height = height

        self.image = None
        self.rect = None
        self.background_color = WHITE
        self.font_color = BLACK
        self.font = ARIAL_30

        self.set_number(number)
        self.draw_number_picker()

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_number(self, number):
        self.number = number

    def draw_number_picker(self):
        self.image = pygame.Surface([self.width, self.height])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        rectangle = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.image, BLACK, rectangle, 1)

        # TODO: Perhaps calculate these positions, centering text
        text_xpos = 18
        text_ypos = 20

        text_surface = ARIAL_36.render(str(self.number), False, BLACK)
        self.image.blit(text_surface, (text_xpos, text_ypos))

