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
from vqe_playground.utils.colors import BLUE, BLACK, WHITE, LIGHT_GREY
from vqe_playground.utils.fonts import *


class Button(pygame.sprite.Sprite):
    """Button that may be clicked"""
    def __init__(self, label, width, height, enabled=True):
        pygame.sprite.Sprite.__init__(self)
        self.label = None
        self.width = width
        self.height = height
        self._enabled = enabled

        self.image = pygame.Surface([self.width, self.height])
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rectangle = pygame.Rect(0, 0, self.width, self.height)

        self.font_color = WHITE
        self.font = ARIAL_36

        self.set_label(label)
        self.draw_button()

        def update(self):
            self.draw_button()

    def set_label(self, label):
        self.label = label

    def get_enabled(self):
        return self._enabled

    def set_enabled(self, enabled):
        self._enabled = enabled
        self.draw_button()

    def draw_button(self):
        self.image.fill(BLUE if self._enabled else LIGHT_GREY)
        pygame.draw.rect(self.image, BLACK, self.rectangle, 1)

        text_surface = self.font.render(self.label, False, self.font_color)
        text_xpos = (self.rect.width - text_surface.get_rect().width) / 2
        text_ypos = (self.rect.height - text_surface.get_rect().height) / 2
        self.image.blit(text_surface, (text_xpos, text_ypos))
