"""
Homework 2 - Complete runner script
Generates all required plots and results for Question 2.
Run with: conda activate data_analysis && python hw2_run.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving files
import matplotlib.pyplot as plt

import networks
import smallWorld as sw

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================================================================
# Q2(a): Draw small world network L=20, Z=4, p=0.2 to verify correctness
# ========================================================================
def q2a():
    print("=" * 60)
    print("Q2(a): Small world network visualization (L=20, Z=4, p=0.2)")
    print("=" * 60)
    g = sw.MakeSmallWorldNetwork(20, 4, 0.2)
    # Verify periodic boundary conditions
    for i in range(20):
        neighbors = sorted(g.GetNeighbors(i))
        expected_ring = sorted([(i - 2) % 20, (i - 1) % 20, (i + 1) % 20, (i + 2) % 20])
        for e in expected_ring:
            assert e in neighbors, f"Node {i} missing ring neighbor {e}, has {neighbors}"
    print("Periodic boundary conditions verified correctly!")
    print(f"Node 0 neighbors: {sorted(g.GetNeighbors(0))}")
    print(f"Node 19 neighbors: {sorted(g.GetNeighbors(19))}")

    # Draw circle graph using matplotlib
    draw_circle_graph(g, os.path.join(OUTPUT_DIR, 'q2a_smallworld_L20_Z4_p02.png'),
                      title='Small World Network (L=20, Z=4, p=0.2)')
    print("Graph saved.\n")

# ========================================================================
# Q2(b): Verify p=0 gives constant histogram, then generate p=0.02, p=0.2
# ========================================================================
def q2b_verify_p0():
    print("=" * 60)
    print("Q2(b) Verification: Histogram at p=0 should be constant")
    print("=" * 60)
    L, Z = 100, 2
    g = sw.MakeRingGraph(L, Z)
    allLengths = networks.FindAllPathLengths(g)
    lengths = list(allLengths.values())
    print(f"Ring graph L={L}, Z={Z}: min path={min(lengths)}, max path={max(lengths)}")
    print(f"Expected max path = L/Z = {L//Z}")

    plt.figure(figsize=(8, 5))
    plt.hist(lengths, bins=range(1, max(lengths) + 2), density=True, edgecolor='black')
    plt.xlabel('Path length l')
    plt.ylabel('Frequency (normalized)')
    plt.title(f'Path length distribution (L={L}, Z={Z}, p=0)\nShould be constant for 0 < l < L/Z={L//Z}')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q2b_histogram_p0_verify.png'), dpi=150)
    plt.close()
    print("Histogram at p=0 saved. Distribution should be uniform/constant.\n")


def q2b_generate(L=1000, Z=2):
    print("=" * 60)
    print(f"Q2(b): Generating graphs and histograms (L={L}, Z={Z})")
    print("=" * 60)

    for p in [0.02, 0.2]:
        print(f"\n--- p = {p} ---")
        g = sw.MakeSmallWorldNetwork(L, Z, p)

        # Draw circle graph
        draw_circle_graph(g, os.path.join(OUTPUT_DIR, f'q2b_circle_L{L}_Z{Z}_p{p}.png'),
                          title=f'Small World Network (L={L}, Z={Z}, p={p})')

        # Compute path lengths
        print(f"  Computing all path lengths (this may take a while for L={L})...")
        allLengths = networks.FindAllPathLengths(g)
        lengths = list(allLengths.values())
        avg = np.mean(lengths)
        print(f"  Total pairs: {len(lengths)}")
        print(f"  Average path length: {avg:.2f}")
        print(f"  Max path length: {max(lengths)}")

        # Plot histogram
        plt.figure(figsize=(8, 5))
        plt.hist(lengths, bins=range(1, max(lengths) + 2), density=True, edgecolor='black', alpha=0.7)
        plt.xlabel('Path length l')
        plt.ylabel('Frequency (normalized)')
        plt.title(f'Path length distribution (L={L}, Z={Z}, p={p})\nMean={avg:.2f}')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f'q2b_histogram_L{L}_Z{Z}_p{p}.png'), dpi=150)
        plt.close()
        print(f"  Histogram saved.")

    print()


# ========================================================================
# Q2(b) extra: Find p for "six degrees of separation"
# ========================================================================
def q2b_six_degrees(L=1000, Z=2):
    print("=" * 60)
    print("Q2(b): Finding p for 'six degrees of separation'")
    print("=" * 60)
    for p in [0.5, 1.0, 2.0, 3.0, 5.0]:
        g = sw.MakeSmallWorldNetwork(L, Z, p)
        avg = networks.FindAveragePathLength(g)
        print(f"  p={p:.1f}: average path length = {avg:.2f}")
    print()


# ========================================================================
# Q2(c): Plot l(p)/l(0) vs p, semi-log (Z=2, L=50)
# ========================================================================
def q2c(L=50, Z=2, numTries=3):
    print("=" * 60)
    print(f"Q2(c): Plotting l(p)/l(0) vs p (L={L}, Z={Z}, numTries={numTries})")
    print("=" * 60)

    parray = 10.**np.arange(-3., 0.001, 0.25)
    print(f"  p values: {parray}")

    # Compute l(p=0)
    l0_mean, l0_std = sw.FindAverageAveragePathLength(L, Z, 0, numTries)
    print(f"  l(p=0) = {l0_mean:.2f} +/- {l0_std:.2f}")

    pathlengths = []
    sigmas = []
    for p in parray:
        mean, std = sw.FindAverageAveragePathLength(L, Z, p, numTries)
        pathlengths.append(mean)
        sigmas.append(std)
        print(f"  p={p:.4f}: l(p)={mean:.2f} +/- {std:.2f}, l(p)/l(0)={mean/l0_mean:.4f}")

    pathlengths = np.array(pathlengths)
    sigmas = np.array(sigmas)

    plt.figure(figsize=(8, 5))
    plt.errorbar(parray, pathlengths / l0_mean, yerr=sigmas / l0_mean, fmt='o-', capsize=3)
    plt.xscale('log')
    plt.xlabel('p')
    plt.ylabel(r'$\ell(p) / \ell(0)$')
    plt.title(f'Average path length vs p (L={L}, Z={Z})')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q2c_pathlength_vs_p.png'), dpi=150)
    plt.close()
    print("  Plot saved.\n")


# ========================================================================
# Q2(d): Real network analysis using NetworkX (Karate Club)
# ========================================================================
def q2d():
    print("=" * 60)
    print("Q2(d): Real network analysis - Zachary's Karate Club")
    print("=" * 60)
    try:
        import networkx as nx
    except ImportError:
        print("  NetworkX not installed. Skipping Q2(d).")
        return

    # Use Zachary's Karate Club - a classic real social network
    G = nx.karate_club_graph()
    print(f"  Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

    # Mean distance
    avg_path = nx.average_shortest_path_length(G)
    print(f"  Mean shortest path length: {avg_path:.4f}")

    # All path lengths histogram
    all_lengths = []
    for node in G.nodes():
        lengths = nx.single_source_shortest_path_length(G, node)
        for target, dist in lengths.items():
            if node < target:
                all_lengths.append(dist)

    plt.figure(figsize=(8, 5))
    plt.hist(all_lengths, bins=range(1, max(all_lengths) + 2), density=True,
             edgecolor='black', alpha=0.7)
    plt.xlabel('Path length')
    plt.ylabel('Frequency (normalized)')
    plt.title(f"Zachary's Karate Club - Path Length Distribution\n"
              f"Nodes={G.number_of_nodes()}, Edges={G.number_of_edges()}, "
              f"Mean={avg_path:.2f}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q2d_real_network_histogram.png'), dpi=150)
    plt.close()

    # Betweenness centrality
    bc = nx.betweenness_centrality(G, normalized=True)
    # Pick 3 nodes with highest betweenness
    sorted_bc = sorted(bc.items(), key=lambda x: x[1], reverse=True)
    print(f"\n  Betweenness centrality (top 3 nodes):")
    for node, centrality in sorted_bc[:3]:
        print(f"    Node {node}: betweenness centrality = {centrality:.4f}")

    # Also pick 3 specific nodes to report
    picked_nodes = [sorted_bc[0][0], sorted_bc[1][0], sorted_bc[2][0]]
    print(f"\n  Selected nodes for analysis: {picked_nodes}")

    # Draw the network with betweenness coloring
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    bc_values = [bc[node] for node in G.nodes()]
    nx.draw(G, pos, ax=ax, node_color=bc_values, cmap=plt.cm.Reds, node_size=300,
            with_labels=True, font_size=8, edge_color='gray', alpha=0.9)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Reds,
                                norm=plt.Normalize(vmin=min(bc_values), vmax=max(bc_values)))
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Betweenness Centrality')
    ax.set_title("Zachary's Karate Club - Betweenness Centrality")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'q2d_real_network_betweenness.png'), dpi=150)
    plt.close(fig)
    print("  Plots saved.\n")


# ========================================================================
# Helper: Draw circle graph using matplotlib
# ========================================================================
def draw_circle_graph(graph, filename, title=''):
    nodes = sorted(graph.GetNodes())
    L = len(nodes)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis('off')
    ax.set_title(title)

    positions = {}
    for idx, node in enumerate(nodes):
        theta = 2 * np.pi * idx / L
        x = np.cos(theta)
        y = np.sin(theta)
        positions[node] = (x, y)

    # Draw edges
    for node in nodes:
        x1, y1 = positions[node]
        for neighbor in graph.GetNeighbors(node):
            if neighbor > node:
                x2, y2 = positions[neighbor]
                # Determine if it's a shortcut (non-ring edge)
                dist_on_ring = min(abs(neighbor - node), L - abs(neighbor - node))
                if dist_on_ring <= graph.GetNeighbors(node).__len__() // 2 + 1:
                    # Heuristic: short edge
                    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.3, alpha=0.5)
                else:
                    ax.plot([x1, x2], [y1, y2], 'r-', linewidth=0.5, alpha=0.7)

    # Draw nodes
    for node in nodes:
        x, y = positions[node]
        ax.plot(x, y, 'ko', markersize=max(1, 6 - L // 50))

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


# ========================================================================
# Main
# ========================================================================
if __name__ == '__main__':
    random.seed(42)
    np.random.seed(42)

    q2a()
    q2b_verify_p0()
    q2b_generate(L=1000, Z=2)
    q2b_six_degrees(L=1000, Z=2)
    q2c(L=50, Z=2, numTries=3)
    q2d()

    print("=" * 60)
    print("All outputs saved to:", OUTPUT_DIR)
    print("=" * 60)
