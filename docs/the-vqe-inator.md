### The Variational Quantum Eigensolver: Examining the inner-workings of the VQE algorithm

#### Why are you reading this?

Seriously, life choices you've made so far have brought you to reading about how a quantum computing algorithm named Variational Quantum Eigensolver works. Maybe it's time to evaluate your life choices, or if you're good with them, please read on! 

The Variational Quantum Eigensolver, or VQE for short, is a quantum computing algorithm that is well suited for solving certain classes of problems using quantum computers available in the near term. VQE may be used for problems involving modeling nature, including chemistry, as [Dr. Richard Feynmann challenged the world to do](https://en.wikipedia.org/wiki/Quantum_computing#Timeline). VQE is also great at finding optimal combinations of things, for example finding the shortest route for visiting a list of cities. This is known as the [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem), and mathematicians call these sorts of challenges [combinatorial optimization](https://en.wikipedia.org/wiki/Combinatorial_optimization) problems.

The open source [Qiskit Aqua library](https://qiskit.org/aqua) contains an implementation of the VQE algorithm, so you may use VQE without understanding how it works. Given that you're still reading this, however, we'd suggest using the Aqua VQE code as a reference to see how the inner workings described here are implemented in code. 

#### Stuff Physicists say

Some words that we'll use here such as [Hamiltonian](https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)) are bandied about by physicists, mathematicians, and theoretical computer scientists, but in most cases they are just fancy words that represent straightforward concepts. There are some concepts and notations used in this article, however, that we'll assume that you're familiar with. You can get up to speed on these in the [Learning Qiskit: for Developers](https://learnqiskit.gitbook.io/developers) guide, working through all of the material up to and including the *Getting Started with Qiskit* section.

#### Using VQE to solve a coloring puzzle

Take a few moments to solve the following graph coloring puzzle that involves filling in some of its circles (vertices) with one color, and the rest of its circles with another color. We'll use the colors *red* and *blue* in this discussion. Solving the puzzle successfully requires achieving the highest possible score, which is defined as the total of the numbers (weights) on the lines (edges) connecting circles that have different colors.

<img src="images/graph-coloring.png" alt="graph-coloring" width="600"/>

*Fig 1: Graph coloring puzzle*

Hint: The highest possible score for the preceding puzzle (or problem if you prefer) is 13, and there are two possible solutions with that score. Please get out your crayons and solve this puzzle before peeking at one of these solutions shown in the next drawing.

##### The relevance of this graph coloring problem

Coloring the vertices of this [weighted graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Weighted_graph) with two colors can model real world problems such as social network interactions and marketing influencers. It is another way of expressing the [MaxCut problem](https://en.wikipedia.org/wiki/Maximum_cut), in which the score is calculated by adding up the weights on the edges that are cut by a line drawn between vertices of different colors:

<img src="images/graph-coloring-maxcut.png" alt="graph-coloring" width="600"/>

*Fig 2: MaxCut solution to our coloring problem*

##### Using physics to solve this problem

One way of thinking about this problem is in the context of magnetism, specifically [antiferromagnetism](https://en.wikipedia.org/wiki/Antiferromagnetism), where the natural tendency is for neighboring electrons to have spins pointing in opposite directions (e.g. *up* and *down*). Using this analogy, the color of a given vertex could correspond to an electron's spin orientation, with blue vertices representing *spin up*, and red vertices representing *spin down*. The strength of an interaction between neighboring vertices is represented by the weight of the edge between them. Because the natural tendency  in this analogy is for neighboring vertices to have opposite colors, and the strength of that tendency is the weight on the edge between them, the [lowest energy (ground) state](https://en.wikipedia.org/wiki/Ground_state) of our graph corresponds to its MaxCut solutions. Let's take a look at one way that physisicts find the lowest energy states of a system.

##### There is no *H* in quantum computing

Actually, there are an overabundance of terms in quantum computing that begin with the letter *H*: [Hadamard gates](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate), [Hermitian matrices](https://en.wikipedia.org/wiki/Hermitian_matrix), [Hilbert spaces](https://en.wikipedia.org/wiki/Hilbert_space) and [Hamiltonian operators](https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)) to name a few. We'll now examine how to leverage that last term, Hamiltonian operators, to find the lowest energy state of our graph. Let's consider a graph with three vertices and weights as shown in the following diagram.

<img src="images/graph-three-vertices.png" alt="graph-coloring" width="150"/>

*Fig 3: Graph with three vertices and weights*

The graph has already been colored with one of its MaxCut solutions, namely, 3, which is the best we can do with this graph. The energy for that coloring is $-1$, because negating the weight total between opposite color vertices yields $-3$ and the weight total between same color vertices is 1. Adding these totals (and dividing by 2 TODO: Determine how to explain why?) yields $-1$.

There are $2^3$ combinations with which the vertices in our graph may be colored. The energy states for each of these combinations are represented on the [main diagonal](https://en.wikipedia.org/wiki/Main_diagonal) of the following Hermitian matrix.  
$$
\begin{bmatrix}
  2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & -1 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & -1 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
 \end{bmatrix}
 \begin{matrix}
 CBA \\
 \vert000\rangle \\
 \vert001\rangle \\
 \vert010\rangle \\
 \vert011\rangle \\
 \vert100\rangle \\
 \vert101\rangle \\
 \vert110\rangle \\
 \vert111\rangle \\
 \\
 \end{matrix}
$$

*Fig 4: Hermitian matrix with energy states*

This matrix serves as our *Hamiltonian operator*, as we'll use it in operations to determine energy values of our graph. To the right of the matrix are basis states that represent the possible color combinations, with $0$ denoting red and $1$ denoting blue. For example the fourth row of the matrix represents the energy state ($-1$) of our graph when the A and B vertices are colored blue, and the C vertex is colored red. To obtain the energy value from this matrix for a given basis state, we'll first multiply the matrix by a column vector that represents the basis state. For example, the following operation yields a vector that contains the energy value for the $\vert011\rangle$ basis state.
$$
\begin{bmatrix}
  2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & -1 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & -1 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
 \end{bmatrix}
 \cdot
 \begin{bmatrix}
 0 \\
 0 \\
 0 \\
 1 \\
 0 \\
 0 \\
 0 \\
 0
 \end{bmatrix}
 =
 \begin{bmatrix}
 0 \\
 0 \\
 0 \\
 -1 \\
 0 \\
 0 \\
 0 \\
 0
 \end{bmatrix}
$$
*Fig 5: Obtaining an energy value from the Hamiltonian (step 1)* 

> Note: Multiplying this vector with this matrix yields the same result as multiplying this vector with a scalar, in this case $-1$. Therefore, this vector is an [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of the matrix, and the eigenvalue of this eigenvector is $-1$. In fact, this matrix has exactly eight eigenvectors, with their associated eigenvalues appearing on the main diagonal. We'll use the Variational Quantum Eigensolver algorithm to find an eigenvector with the lowest eigenvalue.

To obtain the energy value as a scalar from the vector that contains it above, we'll take the inner product of it with a row vector that represents the $\vert011\rangle$ basis state.
$$
\begin{bmatrix}
  0 & 0 & 0 & 1 & 0 & 0 & 0 & 0
 \end{bmatrix}
 \cdot
 \begin{bmatrix}
 0 \\
 0 \\
 0 \\
 -1 \\
 0 \\
 0 \\
 0 \\
 0
 \end{bmatrix}
 = -1
$$

*Fig 6: Obtaining an energy value from the Hamiltonian (step 2)* 

To express these calculations more succinctly, we'll use [Dirac bra-ket](https://en.wikipedia.org/wiki/Bra%E2%80%93ket_notation) notation, where the row vector is expressed as a *bra* and the column vector is expressed as a *ket*. 

> Note: Excluding complex numbers, an element in a *bra* (row vector) contains the same number as its associated element in a *ket* (column vector), and vice-versa. When an element contains a complex number, the element in a *bra* contains the complex conjugate (changing the sign of the imaginary component) of its associated element in a *ket*, and vice-versa.  

The ***H*** symbol is our Hamiltonian operator, which is multiplied by the ket vector, and the resultant vector multiplied by the bra vector. These are the same operations performed previously, only this time expressed with Dirac notation:

$\langle011\vert H\vert011\rangle=-1$

> Note: This expression take the form $\langle\psi\vert H\vert\psi\rangle$ and is known as the [expectation value](https://en.wikipedia.org/wiki/Expectation_value_(quantum_mechanics)). Here we expect the energy value for the given basis state, but as demonstrated later, an expectation value is the average of all the possible outcomes of a measurement weighted by their likelihood.

#### It's time to play

Enough theory about VQE (for the moment anyway)! Let's get some hands-on intuition by using an open source application named [VQE Playground](https://github.com/JavaFXpert/vqe-playground). As shown in the following screenshot, this application provides an interactive visualization of how VQE can find the MaxCut of a graph.

> ![Screenshot of VQE Playground](images/vqe-playground-initial.png)

*Fig 7: Screenshot of the VQE Playground application* 

Included in this visualization are a graph with five vertices, an adjacency matrix that defines the graph's edges and their weights, and a list of the eigenvectors and eigenvalues in the Hamiltonian operator for the graph. This visualization also has a quantum circuit with several ***Ry*** gates that will be rotated as the algorithm seeks the lowest eigenvalue.

> Note: This quantum circuit, with its initial rotation angles, is an example of an [ansatz](https://en.wikipedia.org/wiki/Ansatz), which is a term that physicists and mathematicians use that means "educated guess", or more colloquially, [SWAG](https://en.wikipedia.org/wiki/Scientific_wild-ass_guess). As the algorithm progresses, our ansatz will be iteratively updated with rotations that result in increasingly better guesses. 

Take a look at this short video of VQE Playground in action.

><iframe src="https://player.vimeo.com/video/332727564?title=0&byline=0&portrait=0" width="800" height="448" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

<p><a href="https://vimeo.com/332727564">VQE Playground demo</a> from <a href="https://vimeo.com/javafxpert">James L. Weaver</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

*Fig 8: Video of the VQE Playground application* 

In this video, we first demonstrate how to add an edge to the graph and adjust its weight by clicking a cell repeatedly in the adjacency matrix. Clicking a blank cell adds an edge with a weight value of $1$ between the vertices corresponding to the cell's row and column header labels. Every additional click adds $1$ to the weight, and clicking on a cell with a weight value of $4$ causes that cell to be blank, which removes the corresponding edge from the graph.

> Note: Because this adjacency matrix models an undirected graph (edges don't have arrows), the weight of a cell in a given row and column is the same as the cell in the corresponding column and row. Expressed more succinctly, $A_{ij} = A_{ji}$.

Notice that as the adjacency matrix is modified, the eigenvalues corresponding to the basis states are recalculated. We'll discuss the details of this calculation later, but as you would expect, it uses the weights in the adjacency matrix to compute the energy for each combination of graph coloring.

##### The Optimizer

Clicking the **Optimize** button results in executing the VQE algorithm, which relies upon an optimizer to manage the process of seeking the lowest eigenvalue. The optimizer's job is to turn the available knobs (the ***Ry*** gates in this example) in such a way that the **Weighted average** (expectation value) on the screen continually decreases. In the video we see the optimizer focusing attention on a given ***Ry*** gate, often rotating it in some direction, and moving to the next ***Ry*** gate. While this is happening, the graphical squares in the **Prob**ability column grow, shrink, appear, and disappear. The area of a given square represents the probability that a measurement will result in the basis state next to the square. These squares are a graphical illustration of the expectation value expression,  $\langle\psi\vert H\vert\psi\rangle$ , mentioned earlier. To see why this is true, review the calculations in *Fig 7* and *Fig 8*, noting that each energy value ends up being multiplied by the square of the absolute value of its corresponding amplitude in the state vector.

While the optimizer uses a classical algorithm running on a classical computer, the circuit containing the ansatz is executed and measured on a quantum computer or simulator. This is why VQE is known as a hybrid algorithm, consisting of quantum and classical components, 

> Note: The [VQE algorithm implementation in Qiskit Aqua](https://qiskit.org/documentation/aqua/algorithms.html#vqe) provides [several optimizers from which you may choose](https://qiskit.org/documentation/aqua/optimizers.html#optimizers), as well as the ability to plug in your own optimizer.

##### Poking around a Hilbert space

Turning our attention to the quantum circuit, notice that it contains a pattern of gates that is repeated a few times. The structure of this circuit follows one of several standard [variational forms available in Qiskit Aqua](https://qiskit.org/documentation/aqua/variational_forms.html#variational-forms). As shown in *Fig 7*, the variational form that VQE Playground uses is a series of ***Ry*** gates with linear entanglement maps. Entanglement allows an ansatz to visit nooks and crannies of the Hilbert space that it wouldn't otherwise be able to do.

An ansatz that leverages a good variational form will efficiently explore a Hilbert space at it searches for increasingly lower expectation values. Apparently, lowering ones expectations is a good thing in this context!

#### **Creating a Hamiltonian from the adjacency matrix**

There are $2^n$ energy states in our Hamiltonian (more specifically an [Ising Hamiltonian](https://en.wikipedia.org/wiki/Ising_model)), where $n$ is the number of vertices in the graph. These energy states are computed from the weights on the graph's edges, which are expressed in the adjacency matrix. To accomplish this, Qiskit Aqua leverages the [Pauli Z matrix](https://en.wikipedia.org/wiki/Pauli_matrices), and the [identity matrix](https://en.wikipedia.org/wiki/Identity_matrix) as demonstrated in the following example containing three vertices shown in *Fig 9*.

![](images/three-vertices-adj-matrix.png)

*Fig 9: Three-vertex graph and its adjacency matrix*

As previously discussed, when two vertices are connected by an edge, the energy between them corresponds to the edge's weight. The energy is positive if the vertices are the same color, and negative if the vertices are different colors. We'll model this characteristic by representing each edge with a pair of Pauli Z matrices, beginning with the edge that connects vertices **A** and **B**, whose weight is $1$.  We'll then  scale the matrix by 0.5. (TODO: Why?)
$$
C\phantom{........}B\phantom{.........}A\phantom{.........} \\
\begin{bmatrix}
  1 & 0 \\
  0 & 1
\end{bmatrix}
\cdot
\begin{bmatrix}
  1 & 0 \\
  0 & -1
\end{bmatrix}
\cdot
\begin{bmatrix}
  1 & 0 \\
  0 & -1
\end{bmatrix}
\cdot
0.5
=
$$

$$
\begin{bmatrix}
  0.5 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & -0.5 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & -0.5 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0.5 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0.5 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & -0.5 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & -0.5 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0.5 \\
 \end{bmatrix}
\begin{matrix}
 CBA \\
 \vert000\rangle \\
 \vert001\rangle \\
 \vert010\rangle \\
 \vert011\rangle \\
 \vert100\rangle \\
 \vert101\rangle \\
 \vert110\rangle \\
 \vert111\rangle \\
 \\
 \end{matrix}
$$

*Fig 10: Modeling edge {A, B} with tensor products*

Vertices not connected by this edge (in this example only vertex **C**) are modeled with the identity matrix. Notice that this calculation *increases* the energy of basis states in which vertices **A** and **B** have the same bit value (color), and *decreases* the energy of basis states in which vertices **A** and **B** have different bit values.

A more succinct way to express the preceding calculation is the following. 
$$
\frac{1}{2}\left(w_{ij} Z_i Z_j\right)
$$
The $w_{ij}$ portion of the preceding expression represents the edge weight, which is found in row ${i}$, column ${j}$ of the adjacency matrix. $Z_i Z_j$ means "calculate a tensor product using Pauli $Z$ matrices on qubits ${i}$ and ${j}$, and identity matrices on the rest."

Now we'll model the edge that connects vertices **A** and **C**, scaling the tensor product with the weight of the edge.
$$
C\phantom{........}B\phantom{.........}A\phantom{.........} 
\\
\begin{bmatrix}
  1 & 0 \\
  0 & -1
\end{bmatrix}
\cdot
\begin{bmatrix}
  1 & 0 \\
  0 & 1
\end{bmatrix}
\cdot
\begin{bmatrix}
  1 & 0 \\
  0 & -1
\end{bmatrix}
\cdot
0.5
\cdot
2
=
$$

$$
\begin{bmatrix}
  1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & -1 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & -1 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
 \end{bmatrix}
\begin{matrix}
 CBA \\
 \vert000\rangle \\
 \vert001\rangle \\
 \vert010\rangle \\
 \vert011\rangle \\
 \vert100\rangle \\
 \vert101\rangle \\
 \vert110\rangle \\
 \vert111\rangle \\
 \\
 \end{matrix}
$$

*Fig 11: Modeling edge {A, C} with tensor products*

Again, notice that this calculation *increases* the energy of basis states in which vertices **A** and **C** have the same bit value (color), and *decreases* the energy of basis states in which vertices **A** and **C** have different bit values.

Now that both edges have been modeled, we'll add the matrices together. The resultant matrix shows the combined energy increase/decrease related to each graph coloring.
$$
\begin{bmatrix}
  1.5 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & -1.5 & 0 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0.5 & 0 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & -0.5 & 0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & -0.5 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0.5 & 0 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & -1.5 & 0 \\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 1.5 \\
 \end{bmatrix}
\begin{matrix}
 CBA \\
 \vert000\rangle \\
 \vert001\rangle \\
 \vert010\rangle \\
 \vert011\rangle \\
 \vert100\rangle \\
 \vert101\rangle \\
 \vert110\rangle \\
 \vert111\rangle \\
 \\
 \end{matrix}
$$
*Fig 12: Combined effect of tensor products on energy*

A common and more succinct way of computing the eigenvalues of an Ising Hamiltonian from an adjacency matrix is similar to the following expression. 
$$
\frac{1}{2}\left( \sum_{i<j} w_{ij} Z_i Z_j\right)
$$

In the preceding expression, the $\sum_{i<j}$ portion considers all of the cells in the matrix that are above and to the right of main diagonal, summing the resultant matrices.

#### The end of the beginning

In this article we discussed some of the problem domains in which VQE may be used, and we shed some light on its inner-workings. Some suggested next steps learning more about VQE and applying it to solve problems would be to:

- Read the [VQE documentation](https://qiskit.org/documentation/aqua/algorithms.html#vqe), following links that discuss topics  such as optimizers and variational forms.
- Experiment further with a [Qiskit tutorial that uses VQE for MaxCut problems as well as traveling salesman problems (TSP)](https://nbviewer.jupyter.org/github/Qiskit/qiskit-tutorial/blob/master/qiskit/aqua/optimization/maxcut_and_tsp.ipynb).
- Check out [Qiskit Chemistry](https://qiskit.org/documentation/aqua/chemistry/qiskit_chemistry.html)

 As stated earlier, Qiskit Aqua enables you to use VQE without understanding how it works, but it is our hope that learning more about how it works has been helpful and enlightening!


