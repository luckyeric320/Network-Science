"""
Networks is a module that implements a network of nodes connected by
edges, and various algorithms and measurements implemented on networks.
(This type of data structure is also known in mathematics as a graph.
What we deal with specifically here are undirected graphs, where there is
no direction or asymmetry between the nodes that delineate an edge.)
This module contains the core code needed to define and manipulate
networks, independently of how they are created or what their context is.
We use the Networks module as part of other problem modules, such as
SmallWorld and Percolation.
"""

# Import the necessary libraries.
import NetGraphics  # a separate module supporting network visualization
import importlib
importlib.reload(NetGraphics)

# -----------------------------------------------------------------------
#
# Defining undirected graph class
#
# -----------------------------------------------------------------------

class UndirectedGraph:
    """An UndirectedGraph g contains a dictionary (g.connections) that
    maps a node identifier (key) to a list of nodes connected to (values).
    g.connections[node] returns a list [node2, node3, node4] of neighbors.
    Node identifiers can be any non-mutable Python type (e.g., integers,
    tuples, strings, but not lists).
    """

    def __init__(self):
        """UndirectedGraph() creates an empty graph g.
	      g.connections starts as an empty dictionary.  When nodes are
	      added, the corresponding values need to be inserted into lists.

        A method/function definition in a class must begin with an instance
        of the class in question; by convention, the name "self" is used for
        this instance."""
        self.connections = {}

    def HasNode(self, node):
        """Returns True if the graph contains the specified node, and
        False otherwise.  Check directly to see if the dictionary of
        connections contains the node, rather than (inefficiently)
        generating a list of all nodes and then searching for the
        specified node."""
        # Hint: use the "in" operator to test if a key is in a dictionary
        return node in self.connections

    def AddNode(self, node):
        """Uses HasNode(node) to determine if node has already been added."""
        if not self.HasNode(node):
            self.connections[node] = []

    def AddEdge(self, node1, node2):
        """Add node1 and node2 to network first
	      Adds new edge
	      (appends node2 to connections[node1] and vice-versa, since it's
	      an undirected graph)
	      Do so only if old edge does not already exist
	      (node2 not in connections[node1])
      	"""
        self.AddNode(node1)
        self.AddNode(node2)
        if node2 not in self.connections[node1]:
            self.connections[node1].append(node2)
            self.connections[node2].append(node1)

    def GetNodes(self):
        """g.GetNodes() returns all nodes (keys) in connections"""
        return list(self.connections.keys())

    def GetNeighbors(self, node):
        """g.GetNeighbors(node) returns a copy of the list of neighbors of
        the specified node.  A copy is returned (using the [:] operator) so
	      that the user does not inadvertently change the neighbor list."""
        return self.connections[node][:]

# Simple test routines

# <codecell>
def pentagraph():
    """pentagraph() creates a simple 5-node UndirectedGraph, and then uses
    the imported NetGraphics module to layout and display the graph.
    The graph is returned from the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,2)
    g.AddEdge(0,3)
    g.AddEdge(1,3)
    g.AddEdge(1,4)
    g.AddEdge(2,4)
    NetGraphics.DisplayCircleGraph(g)
    return g

def circle8():
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,1)
    g.AddEdge(1,2)
    g.AddEdge(2,3)
    g.AddEdge(3,4)
    g.AddEdge(4,5)
    g.AddEdge(5,6)
    g.AddEdge(6,7)
    g.AddEdge(7,0)
    NetGraphics.DisplayCircleGraph(g)
    return g

# Simple test functions

def pentagraph():
    """pentagraph() creates a simple 5-node UndirectedGraph, and then uses
    the imported NetGraphics module to layout and display the graph.
    The graph is returned from the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,2)
    g.AddEdge(0,3)
    g.AddEdge(1,3)
    g.AddEdge(1,4)
    g.AddEdge(2,4)
    NetGraphics.DisplayCircleGraph(g)
    return g

def circle8():
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,1)
    g.AddEdge(1,2)
    g.AddEdge(2,3)
    g.AddEdge(3,4)
    g.AddEdge(4,5)
    g.AddEdge(5,6)
    g.AddEdge(6,7)
    g.AddEdge(7,0)
    NetGraphics.DisplayCircleGraph(g)
    return g

#Functions for calculating path lengths 

def FindPathLengthsFromNode(graph, node):
    """Breadth--first search. Use a dictionary to store the distance to
    each node visited.  Keys in the dictionary thus serve as markers
    of nodes that have already been visited, and should not be considered
    again."""
    distances = {node: 0}
    l = 0
    currentShell = [node]
    while currentShell:
        nextShell = []
        for currentNode in currentShell:
            for neighbor in graph.GetNeighbors(currentNode):
                if neighbor not in distances:
                    distances[neighbor] = l + 1
                    nextShell.append(neighbor)
        l += 1
        currentShell = nextShell
    return distances

def FindAllPathLengths(graph):
    """
    FindAllPathLengths returns a dictionary, indexed by node pairs,
    storing the shortest path length between those nodes, e.g. for
    small-world networks
    """
    allLengths = {}
    for node in graph.GetNodes():
        distances = FindPathLengthsFromNode(graph, node)
        for node2, dist in distances.items():
            if node != node2:
                allLengths[(node, node2)] = dist
    return allLengths

def FindAveragePathLength(graph):
    """Averages path length over all pairs of nodes"""
    allLengths = FindAllPathLengths(graph)
    if len(allLengths) == 0:
        return 0
    return sum(allLengths.values()) / len(allLengths)
