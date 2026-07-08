"""
Parse IEEE 8500-Node test feeder CSV files and build a topology graph.
Then aggregate buses into ~578 cells (matching paper) by spatial K-means
clustering on bus coordinates. Lines crossing cluster boundaries become
switchable lines; they form the cell-level edge set.

Outputs (saved as np .npz):
    cell_adj      : (n_cells, n_cells)       0/1 cell-level adjacency
    cell_load_kw  : (n_cells,)               total kW load per cell
    cell_xy       : (n_cells, 2)             centroid coords
    bus_to_cell   : (n_buses,)               int cell id per bus
    bus_names     : (n_buses,)               names
    n_buses, n_lines, n_loads as scalars in metadata.json
"""
import os, csv, json, sys, re
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans

DATA_DIR = "/data/stevens/scratch/8500-feeder/csv"
OUT_DIR  = "/gpustor/stevens/projects-active/replicate-1868518/data"
os.makedirs(OUT_DIR, exist_ok=True)

def norm(name): return name.strip().lower()

def read_buscoords():
    coords = {}
    with open(os.path.join(DATA_DIR, "Buscoords.csv")) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("Name"): continue
            parts = re.split(r"[\s,]+", line)
            if len(parts) >= 3:
                try: coords[norm(parts[0])] = (float(parts[1]), float(parts[2]))
                except ValueError: pass
    return coords

def read_lines(fname):
    """Return list of (bus1, bus2, length_units) edges."""
    edges = []
    with open(os.path.join(DATA_DIR, fname)) as f:
        rd = csv.reader(f)
        for row in rd:
            if not row or row[0].strip().startswith("#"): continue
            if row[0].strip().lower() == "name": continue
            if len(row) < 4: continue
            b1 = norm(row[1]); b2 = norm(row[3])
            try: length = float(row[5]) if len(row) > 5 and row[5].strip() else 0.1
            except ValueError: length = 0.1
            edges.append((b1, b2, length))
    return edges

def read_loads():
    # Loads.CSV columns: Name, NumPhases, Bus, phases, Voltage, status, model, connection, kW, PF
    loads = {}
    with open(os.path.join(DATA_DIR, "Loads.CSV")) as f:
        rd = csv.reader(f)
        for row in rd:
            if not row or row[0].strip().startswith("#"): continue
            if row[0].strip().lower() == "name": continue
            try:
                bus = norm(row[2]); kw = float(row[8])
                loads[bus] = loads.get(bus, 0.0) + kw
            except (ValueError, IndexError):
                pass
    return loads

def main():
    print("Reading buscoords...")
    coords = read_buscoords()
    print(f"  {len(coords)} buses with coords")

    print("Reading lines...")
    pri_edges = read_lines("Lines.csv")
    tri_edges = read_lines("Triplex_Lines.csv")
    print(f"  {len(pri_edges)} primary lines, {len(tri_edges)} triplex lines")

    print("Reading transformers...")
    xfm_edges = []
    try:
        with open(os.path.join(DATA_DIR, "Transformers.csv")) as f:
            rd = csv.reader(f)
            for row in rd:
                if not row or row[0].strip().startswith("#") or row[0].strip().lower() == "name":
                    continue
                if len(row) >= 4:
                    xfm_edges.append((norm(row[1]), norm(row[3]), 0.0))
    except FileNotFoundError: pass

    # LoadXfmrs.csv: center-tapped distribution xfmrs. Connect Wdg1Bus(2)-Wdg2Bus(6)-Wdg3Bus(10)
    try:
        with open(os.path.join(DATA_DIR, "LoadXfmrs.csv")) as f:
            rd = csv.reader(f)
            for row in rd:
                if not row or row[0].strip().startswith("#") or row[0].strip().lower() == "name": continue
                if len(row) >= 7:
                    b1 = norm(row[2]); b2 = norm(row[6])
                    xfm_edges.append((b1, b2, 0.0))
                if len(row) >= 11:
                    b3 = norm(row[10])
                    if b3 and b3 != norm(row[6]):
                        xfm_edges.append((norm(row[6]), b3, 0.0))
    except FileNotFoundError: pass
    print(f"  {len(xfm_edges)} transformer connections")

    all_edges = pri_edges + tri_edges + xfm_edges
    G = nx.Graph()
    for b1,b2,l in all_edges:
        if b1 and b2:
            G.add_edge(b1, b2, length=l)
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Restrict to largest connected component
    cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(cc).copy()
    print(f"Largest CC: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Coords for nodes (fallback to (0,0) for nodes without coords)
    nodes = list(G.nodes())
    bus_idx = {n:i for i,n in enumerate(nodes)}
    xy = np.array([coords.get(n, (0.0,0.0)) for n in nodes], dtype=np.float32)

    # Loads
    loads_kw = read_loads()
    bus_load = np.zeros(len(nodes), dtype=np.float32)
    for n,kw in loads_kw.items():
        if n in bus_idx:
            bus_load[bus_idx[n]] = kw
    print(f"Total load: {bus_load.sum():.1f} kW across {(bus_load>0).sum()} buses")

    # K-means on coords to get ~578 cells (paper's target).
    # Some buses lack coords — assign them to the nearest neighbor cell post-hoc via BFS.
    have_coords = np.array([coords.__contains__(n) for n in nodes])
    n_cells_target = 578
    print(f"Running K-means to {n_cells_target} clusters on {have_coords.sum()} buses w/ coords...")
    km = KMeans(n_clusters=n_cells_target, n_init=10, random_state=42)
    cell_ids = -1 * np.ones(len(nodes), dtype=np.int32)
    cell_ids[have_coords] = km.fit_predict(xy[have_coords])

    # Propagate cell labels to coord-less buses via BFS
    try:
        A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csr")
    except AttributeError:
        A = nx.to_scipy_sparse_matrix(G, nodelist=nodes, format="csr")
    # iterative propagation
    changed = True
    while changed:
        changed = False
        unassigned = np.where(cell_ids < 0)[0]
        if len(unassigned) == 0: break
        for u in unassigned:
            nbrs = A.indices[A.indptr[u]:A.indptr[u+1]]
            nbr_cells = cell_ids[nbrs]
            nbr_cells = nbr_cells[nbr_cells >= 0]
            if len(nbr_cells) > 0:
                vals, counts = np.unique(nbr_cells, return_counts=True)
                cell_ids[u] = int(vals[np.argmax(counts)])
                changed = True
        if not changed: break

    # Any still-unassigned: shove into cell 0
    cell_ids[cell_ids < 0] = 0

    # Build cell-level adjacency
    n_cells = int(cell_ids.max()) + 1
    cell_adj = np.zeros((n_cells, n_cells), dtype=np.float32)
    cell_load = np.zeros(n_cells, dtype=np.float32)
    cell_xy = np.zeros((n_cells, 2), dtype=np.float32)
    cell_size = np.zeros(n_cells, dtype=np.int32)
    for u, v in G.edges():
        cu, cv = cell_ids[bus_idx[u]], cell_ids[bus_idx[v]]
        if cu != cv:
            cell_adj[cu, cv] = 1.0
            cell_adj[cv, cu] = 1.0
    for i, n in enumerate(nodes):
        c = cell_ids[i]
        cell_load[c] += bus_load[i]
        cell_xy[c]   += xy[i]
        cell_size[c] += 1
    cell_xy /= np.maximum(cell_size[:, None], 1)

    n_switchable = int((cell_adj.sum() / 2))
    print(f"Cells: {n_cells}, inter-cell switchable lines: {n_switchable}, total cell load: {cell_load.sum():.1f} kW")

    # Save
    np.savez(os.path.join(OUT_DIR, "cell_graph.npz"),
             cell_adj=cell_adj, cell_load_kw=cell_load, cell_xy=cell_xy,
             bus_to_cell=cell_ids, cell_size=cell_size)
    meta = {
        "n_buses": int(G.number_of_nodes()),
        "n_lines": int(G.number_of_edges()),
        "n_cells": int(n_cells),
        "n_switchable_lines": int(n_switchable),
        "total_load_kw": float(cell_load.sum()),
        "n_load_buses": int((bus_load>0).sum()),
    }
    with open(os.path.join(OUT_DIR, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Saved:", os.path.join(OUT_DIR, "cell_graph.npz"))
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
