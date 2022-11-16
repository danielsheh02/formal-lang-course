from networkx import MultiDiGraph
from pyformlang.cfg import Variable

from project.cfg_utils import *


def cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_symbol: Variable = Variable("S"),
):
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    return {
        (u, v)
        for (V, u, v) in hellings(graph, cfg)
        if V == start_symbol and u in start_nodes and v in final_nodes
    }


def hellings(graph: MultiDiGraph, cfg: CFG):
    cfg = to_wcnf(cfg)
    term_prod = set()
    var_prod = set()
    eps_prod = set()
    for prod in cfg.productions:
        if len(prod.body) == 1:
            term_prod.add(prod)
        elif len(prod.body) == 2:
            var_prod.add(prod)
        else:
            eps_prod.add(prod)
    r = []
    for (v, u, label) in graph.edges(data="label"):
        for prod in term_prod:
            if label == prod.body[0].value:
                r.append((prod.head, v, u))
    for n in graph.nodes:
        for prod in eps_prod:
            r.append((prod.head, n, n))
    m = r.copy()
    while len(m) > 0:
        (Ni, v, u) = m.pop()
        for (Nj, u1, v1) in r:
            if v == v1:
                for prod in var_prod:
                    closure = (prod.head, u1, u)
                    if prod.body[0] == Nj and prod.body[1] == Ni and closure not in r:
                        r.append(closure)
                        m.append(closure)
        for (Nj, u1, v1) in r:
            if u == u1:
                for prod in var_prod:
                    closure = (prod.head, v, v1)
                    if prod.body[0] == Ni and prod.body[1] == Nj and closure not in r:
                        r.append(closure)
                        m.append(closure)
    return r
