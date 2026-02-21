# Homework 2 - Answers

## Question 1: Gephi Visualization
*(Requires manual operation in Gephi software - download dataset, import, visualize)*

---

## Question 2: Small World Networks

### 2(a) Constructing a Small World Network

**Code completed** in `networks.py` and `smallWorld.py`.

- `UndirectedGraph` class: implemented `HasNode`, `AddNode`, `AddEdge`, `GetNodes`, `GetNeighbors`
- `MakeRingGraph(L, Z)`: creates ring with periodic boundary conditions
- `MakeSmallWorldNetwork(L, Z, p)`: ring + p*Z*L/2 random shortcuts

**Verification of periodic boundary conditions:**
- Node 0 connects to: [1, 2, 18, 19] (for L=20, Z=4), correctly wrapping around
- Node 19 connects to: [0, 1, 17, 18], correctly wrapping around

See: `q2a_smallworld_L20_Z4_p02.png`

---

### 2(b) Path Length Distribution

**Verification at p=0:**
- Ring graph L=100, Z=2: path lengths range from 1 to 50 = L/Z
- Histogram is constant (uniform) for 0 < l < L/Z, as expected

See: `q2b_histogram_p0_verify.png`

**Results for L=1000, Z=2:**

| p    | Average path length | Max path length |
|------|-------------------|-----------------|
| 0.02 | 50.87             | 120             |
| 0.2  | 11.69             | 26              |

**Analysis:**
- At p=0, the average path length would be L/4 = 250 (for L=1000, Z=2)
- At p=0.02, the average drops significantly to ~50.87, showing that even a small number of shortcuts (0.02 * 2 * 1000 / 2 = 20 shortcuts) dramatically reduces path lengths
- At p=0.2, the average drops further to ~11.69 with 200 shortcuts
- The distribution shifts from uniform to approximately bell-shaped, concentrated at shorter lengths

**Six degrees of separation:**
- p=0.5: avg = 7.41
- p=1.0: avg = 5.35

For L=1000, Z=2, approximately **p ~ 1.0** gives six degrees of separation (average path length around 5-6).

See: `q2b_circle_L1000_Z2_p0.02.png`, `q2b_histogram_L1000_Z2_p0.02.png`, `q2b_circle_L1000_Z2_p0.2.png`, `q2b_histogram_L1000_Z2_p0.2.png`

---

### 2(c) Average Path Length vs p

Plot of l(p)/l(0) for Z=2, L=50 on semi-log scale:

- l(p=0) = 12.76 (= L/4 = 50/4 = 12.5, close to theoretical)
- The curve shows the characteristic Watts-Strogatz transition:
  - For small p (< 0.01), l(p)/l(0) ~ 1 (no change)
  - Around p ~ 0.03-0.1, a sharp drop occurs
  - For large p (> 0.3), l(p)/l(0) approaches a small value

This is consistent with Fig. 2 of Watts and Strogatz (1998), with p values shifted by a factor of ~100 (since our model adds shortcuts instead of rewiring, and L=50 is smaller).

See: `q2c_pathlength_vs_p.png`

---

### 2(d) Real Network Analysis

**Network:** Zachary's Karate Club (a classic social network)
- 34 nodes, 78 edges
- Mean shortest path length: **2.408**

**Path length distribution:** Most pairs of nodes are separated by 2-3 hops.

**Betweenness Centrality (top 3 nodes):**

| Node | Betweenness Centrality | Role |
|------|----------------------|------|
| 0    | 0.4376               | Club instructor (Mr. Hi) |
| 33   | 0.3041               | Club president (John A) |
| 32   | 0.1452               | Key connector |

These three nodes are the most crucial bridges in the network. Nodes 0 and 33 represent the two faction leaders in the famous club split, and their high betweenness centrality reflects their roles as central connectors through which many shortest paths pass.

See: `q2d_real_network_histogram.png`, `q2d_real_network_betweenness.png`

---

## Question 3: Hospital Assignment (Network Flow)

**Problem:** Assign n injured people to k hospitals such that:
- Each person goes to a hospital within half-hour driving distance
- Each hospital receives at most ceil(n/k) people

**Network Flow Construction:**

```
        cap=1       cap=1 (if reachable)     cap=ceil(n/k)
  [s] -------> [p_i] -----------------> [h_j] ------------> [t]
  source      people                   hospitals           sink
```

**Nodes:**
1. **Source s**: a super-source node
2. **Person nodes** p_1, p_2, ..., p_n: one for each injured person
3. **Hospital nodes** h_1, h_2, ..., h_k: one for each hospital
4. **Sink t**: a super-sink node

**Edges:**
1. **s -> p_i**: capacity = 1 for each person i (each person must be assigned to exactly one hospital)
2. **p_i -> h_j**: capacity = 1 if hospital h_j is within half-hour driving distance of person p_i (represents a feasible assignment)
3. **h_j -> t**: capacity = ceil(n/k) for each hospital j (enforces the load balancing constraint)

**Algorithm:**
Run a max-flow algorithm (e.g., Ford-Fulkerson, Edmonds-Karp) on this network.

**Decision:**
- If **max flow = n**, then a feasible balanced assignment exists. The flow on each edge p_i -> h_j indicates the assignment.
- If **max flow < n**, then it is impossible to assign all people while respecting distance and capacity constraints.

**Correctness argument:**
- The capacity 1 on s -> p_i edges ensures each person is assigned to exactly one hospital
- The edges p_i -> h_j only exist for feasible (reachable) hospitals, ensuring distance constraints
- The capacity ceil(n/k) on h_j -> t edges ensures no hospital is overloaded
- Max flow = n means all n units of flow reach the sink, so every person is assigned

**Time complexity:** O(V * E^2) with Edmonds-Karp, where V = n + k + 2, E = n + (sum of feasible assignments) + k.

---

## Question 4: Balloon Measurement (Network Flow)

**Problem:** Assign m balloons to measure n conditions such that:
- Each balloon measures at most 2 conditions
- Each condition is measured by at least k different balloons
- A balloon can only measure conditions in its capability set S_i

**Network Flow Construction:**

```
        cap=2       cap=1 (if c_j in S_i)    cap=k
  [s] -------> [b_i] -----------------> [c_j] ---------> [t]
  source      balloons                conditions         sink
```

**Nodes:**
1. **Source s**: a super-source node
2. **Balloon nodes** b_1, b_2, ..., b_m: one for each balloon
3. **Condition nodes** c_1, c_2, ..., c_n: one for each atmospheric condition
4. **Sink t**: a super-sink node

**Edges:**
1. **s -> b_i**: capacity = 2 for each balloon i (each balloon can make at most 2 measurements)
2. **b_i -> c_j**: capacity = 1 if condition c_j is in S_i (balloon i is capable of measuring condition j). The capacity of 1 prevents the same balloon from measuring the same condition twice.
3. **c_j -> t**: capacity = k for each condition j (each condition needs to be measured by at least k different balloons)

**Algorithm:**
Run a max-flow algorithm (e.g., Ford-Fulkerson, Edmonds-Karp) on this network.

**Decision:**
- If **max flow = n * k**, then a feasible measurement plan exists. Each unit of flow through b_i -> c_j means balloon i measures condition c_j.
- If **max flow < n * k**, then it is impossible to measure every condition k times with the given constraints.

**Correctness argument:**
- The capacity 2 on s -> b_i edges ensures each balloon measures at most 2 conditions
- The capacity 1 on b_i -> c_j edges ensures a balloon doesn't measure the same condition twice
- The edges b_i -> c_j only exist when c_j in S_i, respecting capability constraints
- The capacity k on c_j -> t edges ensures each condition receives exactly k measurements when saturated
- Total required flow is n * k (n conditions, each needing k measurements)

**Verification with the example (k=2, n=4, m=4):**
- s -> b1, b2, b3, b4 all have capacity 2
- b1 -> c1, c2, c3 (S1 = {c1, c2, c3})
- b2 -> c1, c2, c3 (S2 = {c1, c2, c3})
- b3 -> c1, c3, c4 (S3 = {c1, c3, c4})
- b4 -> c1, c3, c4 (S4 = {c1, c3, c4})
- c1, c2, c3, c4 -> t all have capacity 2
- Max flow = 8 = 4 * 2, so a solution exists.

**Time complexity:** O(V * E^2) with Edmonds-Karp, where V = m + n + 2, E = m + (sum of |S_i|) + n.
