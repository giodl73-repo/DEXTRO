# Recursive Bisection Algorithm

This document provides a detailed explanation of the recursive bisection algorithm used for congressional redistricting.

## Core Concept

**Problem**: Partition N tracts into K districts with equal population.

**Solution**: Divide and conquer
1. Split all tracts into 2 groups (using METIS)
2. Recursively split each group until you have K districts

## Visual Walkthrough

The following diagram shows how recursive bisection works step-by-step, from geographic input through graph representation, the cut operation, and resulting partitions:

```mermaid
graph TB
    subgraph "Step 1: Geographic Input"
        A1["<b>State with Census Tracts</b><br/>────────────────────<br/>┌───┬───┬───┐<br/>│ A │ B │ C │ Pop: 120K<br/>├───┼───┼───┤<br/>│ D │ E │ F │ Pop: 130K<br/>├───┼───┼───┤<br/>│ G │ H │ I │ Pop: 125K<br/>└───┴───┴───┘<br/>Total: 375K → 2 Districts<br/>Target: ~187.5K per district"]
    end

    subgraph "Step 2: Graph Representation"
        B1["<b>Adjacency Graph</b><br/>────────────────────<br/>Vertices (Census Tracts):<br/>• A (pop: 40K)<br/>• B (pop: 45K)<br/>• C (pop: 35K)<br/>• D (pop: 42K)<br/>• E (pop: 48K)<br/>• F (pop: 40K)<br/>• G (pop: 38K)<br/>• H (pop: 47K)<br/>• I (pop: 40K)<br/><br/>Edges (Adjacencies):<br/>A↔B, B↔C, D↔E, E↔F<br/>G↔H, H↔I, A↔D, B↔E<br/>C↔F, D↔G, E↔H, F↔I"]
    end

    subgraph "Step 3: METIS Partitioning"
        C1["<b>Graph with Edge Weights</b><br/>────────────────────<br/>      A(40)───B(45)───C(35)<br/>       │       │       │<br/>      D(42)───E(48)───F(40)<br/>       │       │       │<br/>      G(38)───H(47)───I(40)<br/><br/>Find minimum edge cut that:<br/>✓ Balances population (~50%/50%)<br/>✓ Minimizes edges crossed<br/>✓ Keeps regions contiguous"]
    end

    subgraph "Step 4: The Cut"
        D1["<b>Partition Cut Found</b><br/>────────────────────<br/>      A(40)───B(45) ║ C(35)<br/>       │       │     ║  │<br/>      D(42)───E(48) ║ F(40)<br/>       │       │     ║  │<br/>      G(38)───H(47) ║ I(40)<br/>━━━━━━━━━━━━━━━━━━━<br/>Cut edges: B↔C, E↔F, H↔I<br/>Edge cut weight: 3"]
    end

    subgraph "Step 5: Two Balanced Partitions"
        E1["<b>Region 0 (Left)</b><br/>────────────────────<br/>┌───┬───┐<br/>│ A │ B │<br/>├───┼───┤<br/>│ D │ E │<br/>├───┼───┤<br/>│ G │ H │<br/>└───┴───┘<br/>Population: 187K<br/>Target: 1 district<br/>✓ Balanced!"]
        E2["<b>Region 1 (Right)</b><br/>────────────────────<br/>┌───┐<br/>│ C │<br/>├───┤<br/>│ F │<br/>├───┤<br/>│ I │<br/>└───┘<br/>Population: 188K<br/>Target: 1 district<br/>✓ Balanced!"]
    end

    subgraph "Step 6: Recurse if Needed"
        F1["<b>Check Each Region</b><br/>────────────────────<br/>Region 0: 1 district → DONE ✓<br/>Region 1: 1 district → DONE ✓<br/><br/>If target_districts > 1:<br/>  Split again recursively<br/><br/>Round 1: 1 → 2 regions<br/>Round 2: 2 → 4 regions<br/>Round 3: 4 → 8 regions<br/>Continue until each region<br/>has target_districts = 1"]
    end

    A1 ==> B1
    B1 ==> C1
    C1 ==> D1
    D1 ==> E1
    D1 ==> E2
    E1 ==> F1
    E2 ==> F1

    style A1 fill:#E8F5E9
    style B1 fill:#FFF3E0
    style C1 fill:#E3F2FD
    style D1 fill:#FFEBEE
    style E1 fill:#F3E5F5
    style E2 fill:#F3E5F5
    style F1 fill:#E0F2F1
```

**Key Steps Explained**:
1. **Geographic Input**: Start with census tracts and their populations
2. **Graph Representation**: Convert spatial data into a graph where vertices are tracts and edges connect adjacent tracts
3. **METIS Partitioning**: Use METIS to find the optimal cut that balances population while minimizing edge cuts
4. **The Cut**: Partition the graph by removing edges (shown with ║ symbols)
5. **Balanced Partitions**: Result is two contiguous regions with nearly equal population
6. **Recurse**: If a region needs more than 1 district, split it again recursively

## Why Recursive Bisection?

**Alternative**: Direct K-way partitioning
- **Problem**: METIS struggles with large K, slow, poor balance
- **Our Solution**: Binary splits are fast and well-balanced

**Advantages**:
- Hierarchical (creates natural nested structure)
- Fast (log₂K levels of recursion)
- Good population balance at each level
- Easy to visualize (binary tree)

## Pseudocode

```python
def recursive_bisection(tracts, adjacency_graph, target_districts):
    """
    Recursively partition tracts into districts.

    Args:
        tracts: List of tract data (with population)
        adjacency_graph: NetworkX graph of tract connectivity
        target_districts: Number of districts to create

    Returns:
        assignments: dict mapping tract_idx -> district_id
    """
    if target_districts == 1:
        # Base case: assign all tracts to district 1
        return {idx: 1 for idx in range(len(tracts))}

    # Split into two groups
    split_point = target_districts // 2

    # Use METIS to partition graph into 2 balanced parts
    partition = metis_bisect(adjacency_graph, tracts_population)

    # Separate into two subgraphs
    group_0_tracts = [i for i in range(len(tracts)) if partition[i] == 0]
    group_1_tracts = [i for i in range(len(tracts)) if partition[i] == 1]

    group_0_graph = adjacency_graph.subgraph(group_0_tracts)
    group_1_graph = adjacency_graph.subgraph(group_1_tracts)

    # Recursively partition each group
    group_0_assignments = recursive_bisection(
        group_0_tracts, group_0_graph, split_point
    )

    group_1_assignments = recursive_bisection(
        group_1_tracts, group_1_graph, target_districts - split_point
    )

    # Offset group_1 district IDs
    for tract_idx, district_id in group_1_assignments.items():
        group_1_assignments[tract_idx] = district_id + split_point

    # Combine assignments
    return {**group_0_assignments, **group_1_assignments}
```

## METIS Integration

**METIS** (Multi-constraint Graph Partitioning): Fast graph partitioning library
- Input: Weighted graph + target partition sizes
- Output: Partition assignment for each node
- Objective: Minimize edge cuts (keeps geographically compact)

**Our Usage**:
```python
import pymetis

# Convert NetworkX graph to METIS format
adjacency_list = [list(adj_graph.neighbors(i)) for i in nodes]

# Partition with population weights
parts = pymetis.part_graph(
    nparts=2,                    # Binary split
    adjacency=adjacency_list,
    vweights=population_weights, # Balance population
    niter=100                    # Quality (more iterations = better)
)
```

**Why niter=100?**: Trade-off between speed and quality
- niter=10: Fast, lower quality
- niter=100: Good balance (our default)
- niter=1000: Slow, diminishing returns

## Handling Odd Numbers of Districts

**Problem**: 52 districts → 26, 26 ✓
**Problem**: 53 districts → 26, 27? or 27, 26?

**Solution**: Split as evenly as possible
```python
split_point = target_districts // 2
group_0_size = split_point
group_1_size = target_districts - split_point

# Example: 53 districts
# split_point = 53 // 2 = 26
# group_0 = 26, group_1 = 27
```

## Bisection Tree Example

**California: 52 districts**

```
                    52 districts
                   /            \
              26                 26
             /  \               /  \
           13   13            13    13
          / \   / \          / \   / \
         7  6  7  6         7  6  7  6
        ...
```

- Level 0: 1 region (all tracts)
- Level 1: 2 regions
- Level 2: 4 regions
- Level 3: 8 regions
- Level 4: 16 regions
- Level 5: 32 regions
- Level 6: 52 districts ✓

Total rounds: ⌈log₂(52)⌉ = 6 levels

## Implementation

The algorithm is implemented in `src/apportionment/partition/recursive_bisection.py`. See [ARCHITECTURE.md](ARCHITECTURE.md) for how this fits into the overall system architecture.
