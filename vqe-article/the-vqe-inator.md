### The Variational Quantum Eigensolver-inator: Examining the inner-workings of the VQE algorithm

#### Why are you reading this?

Seriously, life choices you've made so far have brought you to reading about how a quantum computing algorithm named Variational Quantum Eigensolver works. Maybe it's time to evaluate your life choices, or if you're good with them, please read on! 

The Variational Quantum Eigensolver, or VQE for short, is a quantum computing algorithm that is well suited for solving certain classes of problems using quantum computers available in the near term. VQE may be used for problems involving modeling nature, including chemistry, as [Dr. Richard Feynmann challenged the world to do](https://en.wikipedia.org/wiki/Quantum_computing#Timeline). VQE is also great at finding optimal combinations of things, for example finding the shortest route for visiting a list of cities. This is known as the [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem), and mathematicians call these sorts of challenges [combinatorial optimization](https://en.wikipedia.org/wiki/Combinatorial_optimization) problems.

#### Stuff Physicists say

Some words that we'll use here such as [Hamiltonian](https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)) are bandied about by physicists, mathematicians, and theoretical computer scientists, but in most cases they are just fancy words that represent straightforward concepts. There are some concepts and notations used in this article, however, that we'll assume that you're familiar with. You can get up to speed on these in the [Learning Qiskit: for Developers](https://learnqiskit.gitbook.io/developers) guide, working through all of the material up to and including the *Getting Started with Qiskit* section.

#### Using VQE to solve a coloring puzzle

Take a few moments to solve the following graph coloring puzzle that involves filling in some of its circles (vertices) with one color, and the rest of its circles with another color. We'll use the colors *red* and *blue* in this discussion. Solving the puzzle successfully requires achieving the highest possible score, which is defined as the total of the numbers (weights) on the lines (edges) connecting circles that have different colors.

<img src="images/graph-coloring.png" alt="graph-coloring" width="600"/>

*Fig 1: Graph coloring puzzle*

Hint: The highest possible score for the preceding puzzle (or problem if you prefer) is 13, and there are two possible solutions. Please get out your crayons and solve this puzzle before peeking at one of these solutions shown in the next drawing.

##### The relevance of this graph coloring problem

Coloring the vertices of this graph with two colors can model real world problems such as social network interactions and marketing influencers. It is another way of expressing the [MaxCut problem](https://en.wikipedia.org/wiki/Maximum_cut), in which the score is calculated by adding up the weights on the edges that are cut by a line drawn between vertices of different colors:

<img src="images/graph-coloring-maxcut.png" alt="graph-coloring" width="600"/>

*Fig 2: MaxCut solution to our coloring problem*

##### Using physics to solve this problem

One way of thinking about this problem is in the context of magnetism, specifically [antiferromagnetism](https://en.wikipedia.org/wiki/Antiferromagnetism), where the natural tendency is for neighboring electrons to have spins pointing in opposite directions (e.g. *up* and *down*). Using this analogy, the color of a given vertex could correspond to an electron's spin orientation, with blue vertices representing *spin up*, and red vertices representing *spin down*. The strength of an interaction between neighboring vertices is represented by the weight of the edge between them. Because the natural tendency  in this analogy is for neighboring vertices to have opposite colors, and the strength of that tendency is the weight on the edge between them, the [lowest energy (ground) state](https://en.wikipedia.org/wiki/Ground_state) of our graph corresponds to its MaxCut solutions. Let's take a look at one way that physisicts find the lowest energy states of a system.

##### There is no *H* in quantum computing

Actually, there are an overabundance of terms in quantum computing that begin with the letter *H*: [Hadamard gates](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate), [Hermitian matrices](https://en.wikipedia.org/wiki/Hermitian_matrix), [Hilbert spaces](https://en.wikipedia.org/wiki/Hilbert_space) and [Hamiltonian operators](https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)) to name a few. We'll now examine how to leverage that last term, Hamiltonian operators, to find the lowest energy state of our graph. Let's consider a graph with three vertices and weights as shown in the following diagram.

<img src="images/graph-three-vertices.png" alt="graph-coloring" width="150"/>

The graph has already been colored with one of its MaxCut solutions, namely, 3, as the sum of the cuts between nodes of different colors is 3.  

$$
\begin{bmatrix}
  2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & -1 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
 \end{bmatrix}
$$

#### Glossary

| Term                                                     | Meaning                                             |
| -------------------------------------------------------- | --------------------------------------------------- |
| [Ansatz](https://en.wikipedia.org/wiki/Ansatz)           | Educated guess that is made more accurate over time |
| [MaxCut](https://en.wikipedia.org/wiki/Maximum_cut)      |                                                     |
| MaxCut shift                                             |                                                     |
| Hamiltonian                                              |                                                     |
| [Ising model](https://en.wikipedia.org/wiki/Ising_model) |                                                     |
|                                                          |                                                     |

