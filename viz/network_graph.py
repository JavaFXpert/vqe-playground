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
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import networkx as nx

from utils import load_image


class NetworkGraph(pygame.sprite.Sprite):
    """Displays a network graph"""
    def __init__(self, adj_matrix):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.adj_matrix = None
        self.set_adj_matrix(adj_matrix)

    def set_adj_matrix(self, adj_matrix):
        self.adj_matrix = adj_matrix

        # def draw_network_graph(self):
        fig = plt.figure(figsize=(5, 5))
        ax = plt.subplot(111)

        n = 4  # Number of nodes in graph
        G = nx.Graph()
        G.add_nodes_from(np.arange(0, n, 1))
        elist = [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
        # tuple is (i,j,weight) where (i,j) is the edge
        G.add_weighted_edges_from(elist)

        colors = ['r' for node in G.nodes()]
        pos = nx.spring_layout(G)
        default_axes = plt.axes(frameon=True)

        nx.draw_networkx(G, node_color=colors, node_size=600, alpha=.8, ax=default_axes, pos=pos)
        plt.savefig("utils/data/network_graph.png")

        self.image, self.rect = load_image('network_graph.png', -1)
        self.rect.inflate_ip(-100, -100)
        self.image.convert()
