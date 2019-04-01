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
import networkx as nx
from cmath import isclose

from utils import load_image


class NetworkGraph(pygame.sprite.Sprite):
    """Displays a network graph"""
    def __init__(self, adj_matrix):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.adj_matrix = None
        self.solution = None
        self.graph = nx.Graph()
        self.graph_pos = None
        self.num_nodes = adj_matrix.shape[0] # Number of nodes in graph
        self.set_adj_matrix(adj_matrix)

    def update(self):
        colors = ['r' if self.solution[i] == 0 else 'b' for i in range(self.num_nodes)]
        self.draw_network_graph(colors)

    def set_adj_matrix(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.solution = np.zeros(self.num_nodes)

        fig = plt.figure(figsize=(5, 5))

        self.graph.add_nodes_from(np.arange(0, self.num_nodes, 1))

        # tuple is (i,j,weight) where (i,j) is the edge
        edge_list = []
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if not isclose(adj_matrix[i, j], 0.0):
                    edge_list.append((i, j, adj_matrix[i, j]))

        self.graph.add_weighted_edges_from(edge_list)

        # TODO: Factor out the line that repeats this one
        colors = ['r' if self.solution[i] == 0 else 'b' for i in range(self.num_nodes)]

        self.graph_pos = nx.spring_layout(self.graph)
        self.draw_network_graph(colors)

    def set_solution(self, solution):
        self.solution = solution

        colors = ['r' if self.solution[i] == 0 else 'b' for i in range(self.num_nodes)]
        self.draw_network_graph(colors)

    def draw_network_graph(self, colors):
        edge_labels = dict([((u, v,), self.adj_matrix[u, v]) for u, v, d in self.graph.edges(data=True)])
        nx.draw_networkx_edge_labels(self.graph, self.graph_pos, edge_labels=edge_labels)

        nx.draw_networkx(self.graph, node_color=colors, node_size=600, alpha=.8, pos=self.graph_pos, font_color='white')
        plt.axis('off')
        plt.savefig("utils/data/network_graph.png")

        self.image, self.rect = load_image('network_graph.png', -1)
        self.image.convert()

