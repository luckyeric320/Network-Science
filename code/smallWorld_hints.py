# Import the necessary libraries.
import random, os
import scipy, pylab
import NetGraphics
import numpy as np
# Import your network definitions
import networks
import imp
imp.reload(networks)	# Helps with ipython %run command

# Small world and ring graphs

def MakeRingGraph(num_nodes, Z):
    """
    Makes a ring graph with Z neighboring edges per node.
    Each node i is connected to nodes (i-Z/2) mod L ... (i+Z/2) mod L.
    """
    g = networks.UndirectedGraph()
    for i in range(num_nodes):
        g.AddNode(i)
    for i in range(num_nodes):
        for j in range(1, Z // 2 + 1):
            neighbor = (i + j) % num_nodes
            g.AddEdge(i, neighbor)
    return g

def AddRandomEdges(graph, num_edges_tried):
    """Attempts to add num_edges_tried random bonds to a graph. It may add
    fewer, if the bonds already exist."""
    nodes = graph.GetNodes()
    L = len(nodes)
    for _ in range(num_edges_tried):
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)
        if node1 != node2:
            graph.AddEdge(node1, node2)

def MakeSmallWorldNetwork(L, Z, p):
    """
    Makes a small--world network of size L and Z neighbors,
    with p*Z*L/2 shortcuts added.  This is the Watts-Newman variant
    of the original Watts-Strogatz model.  The original model
    used a rewiring technique, replacing a randomly selected short-range
    bond with a randomly-selected long-range shortcut.  The Watts-Newman
    model keeps all short-range bonds intact, and adds p*Z*L/2 random
    shortcuts.  This revised model is both simpler to treat analytically
    (see the renormalization group analysis by Watts and Newman) and
    avoids the potential for subgraphs to become disconnected from
    one another due to rewiring.
    """
    g = MakeRingGraph(L, Z)
    num_shortcuts = int(p * Z * L / 2)
    AddRandomEdges(g, num_shortcuts)
    return g

def SmallWorldSimple(L, Z, p):
    """
    Generate and display small world network. Creates a graph g using
    MakeSmallWorldNetwork, and uses the NetGraphics command
    DisplayCircleGraph, with only the mandatory argument g. Returns g.
    """
    g = MakeSmallWorldNetwork(L, Z, p)
    NetGraphics.DisplayCircleGraph(g)
    return g

def MakePathLengthHistograms(L=100, Z=4, p=0.1):
    """
    Plots path length histograms for small world networks.
    Find list of all lengths
    Use pylab.hist(lengths, bins=range(max(lengths)), normed=True) """
    g = MakeSmallWorldNetwork(L, Z, p)
    allLengths = networks.FindAllPathLengths(g)
    lengths = list(allLengths.values())
    pylab.figure()
    pylab.hist(lengths, bins=range(max(lengths)+1), density=True)
    pylab.xlabel('Path length')
    pylab.ylabel('Frequency')
    pylab.title('Path length distribution (L=%d, Z=%d, p=%.3f)' % (L, Z, p))
    pylab.show()

def FindAverageAveragePathLength(L, Z, p, numTries):
    """Finds mean and standard deviation for path length between nodes,
    for a small world network of L nodes, Z bonds to neighbors,
    p*Z*L/2 shortcuts, averaging over numTries samples"""
    avgLengths = []
    for _ in range(numTries):
        g = MakeSmallWorldNetwork(L, Z, p)
        avg = networks.FindAveragePathLength(g)
        avgLengths.append(avg)
    mean = np.mean(avgLengths)
    std = np.std(avgLengths)
    return mean, std

def GetPathLength_vs_p(L, Z, numTries, parray):
    """Calculates array of mean pathlengths and sigmas for small
    world networks; returns pathlengths and sigmas"""
    pathlengths = []
    sigmas = []
    for p in parray:
        mean, std = FindAverageAveragePathLength(L, Z, p, numTries)
        pathlengths.append(mean)
        sigmas.append(std)
    return np.array(pathlengths), np.array(sigmas)

def PlotPathLength_vs_p(L, Z, numTries=2,
                        parray=10.**np.arange(-3., 0.001, 0.25)):
    """Plots path length versus p"""
    pathlengths, sigmas = GetPathLength_vs_p(L, Z, numTries, parray)
    # Normalize by l(p=0)
    l0 = pathlengths[0] if parray[0] == 0 else FindAverageAveragePathLength(L, Z, 0, numTries)[0]
    pylab.figure()
    pylab.errorbar(parray, pathlengths / l0, yerr=sigmas / l0, fmt='o-')
    pylab.xscale('log')
    pylab.xlabel('p')
    pylab.ylabel(r'$\ell(p) / \ell(0)$')
    pylab.title('Average path length vs p (L=%d, Z=%d)' % (L, Z))
    pylab.show()


