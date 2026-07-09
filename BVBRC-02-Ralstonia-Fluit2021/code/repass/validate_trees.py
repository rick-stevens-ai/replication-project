#!/usr/bin/env python3
"""Validate tree topology vs published group assignments.

For each ML tree (16S, OXA22, OXA60):
  - Parse Newick
  - For each group (D1, D2, E1, E2, F, G), test whether tips are monophyletic
  - Report group monophyly summary
"""
from __future__ import annotations
import re, sys, json, pathlib
from collections import defaultdict

ROOT = pathlib.Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021")
OUT = ROOT/"results/repass"

# Minimal Newick parser -> nested list of clades
class Node:
    __slots__ = ("name","children","parent","length","support")
    def __init__(self, name=""):
        self.name=name; self.children=[]; self.parent=None
        self.length=0.0; self.support=None
    def is_leaf(self): return not self.children
    def leaves(self):
        if self.is_leaf(): return [self.name]
        out=[]
        for c in self.children: out.extend(c.leaves())
        return out

def parse_newick(s):
    s = s.strip().rstrip(";")
    pos = [0]
    def parse_node():
        node = Node()
        if s[pos[0]] == "(":
            pos[0] += 1
            while True:
                child = parse_node()
                child.parent = node
                node.children.append(child)
                if s[pos[0]] == ",": pos[0]+=1
                elif s[pos[0]] == ")":
                    pos[0]+=1
                    break
        # name / support / length
        name_buf=[]
        while pos[0] < len(s) and s[pos[0]] not in ",():":
            name_buf.append(s[pos[0]]); pos[0]+=1
        name = "".join(name_buf)
        # internal label may be support value
        if name:
            try:
                node.support = float(name)
            except ValueError:
                node.name = name
        # branch length
        if pos[0] < len(s) and s[pos[0]] == ":":
            pos[0]+=1
            bl=[]
            while pos[0] < len(s) and s[pos[0]] not in ",()":
                bl.append(s[pos[0]]); pos[0]+=1
            node.length = float("".join(bl))
        return node
    return parse_node()

def all_clades(node, out=None):
    if out is None: out=[]
    if not node.is_leaf():
        out.append(set(node.leaves()))
        for c in node.children: all_clades(c, out)
    return out

def group_of(label):
    # label format like 535632_D2
    parts = label.rsplit("_",1)
    return parts[1] if len(parts)==2 else "?"

def analyze(tree_path):
    nwk = open(tree_path).read().strip()
    root = parse_newick(nwk)
    leaves = root.leaves()
    groups = defaultdict(list)
    for l in leaves: groups[group_of(l)].append(l)
    clades = all_clades(root)
    results = {}
    for g, members in groups.items():
        if len(members) == 1:
            results[g] = {"members": members, "monophyletic": "trivial-singleton"}
            continue
        members_set = set(members)
        is_mono = any(c == members_set for c in clades)
        if is_mono:
            results[g] = {"members": members, "monophyletic": True}
        else:
            # Is the group at least clustered with no foreign members?
            # i.e. for each pair of group members find their MRCA's leaves
            # Find smallest clade containing all group members
            covering = [c for c in clades if members_set.issubset(c)]
            if covering:
                smallest = min(covering, key=len)
                extras = sorted(smallest - members_set)
                results[g] = {"members": members, "monophyletic": False,
                              "smallest_containing_clade_size": len(smallest),
                              "extras": extras}
            else:
                results[g] = {"members": members, "monophyletic": False, "extras": "?root?"}
    # Tree summary
    n_internal = sum(1 for c in clades)
    return {"path": str(tree_path), "n_leaves": len(leaves),
            "n_internal": n_internal, "groups": results}

if __name__ == "__main__":
    rep = {}
    for name in ("16S","OXA22","OXA60"):
        rep[name] = analyze(OUT/f"{name}.nwk")
    print(json.dumps(rep, indent=2))
    with open(OUT/"tree_validation.json","w") as fh:
        json.dump(rep, fh, indent=2)
