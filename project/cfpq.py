from networkx import MultiDiGraph
from pyformlang.cfg import Variable
from scipy.sparse import dok_array, eye

from project.cfg_utils import *


def cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_symbol: Variable = Variable("S"),
    alg_type: str = "hellings",
):
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    if alg_type == "hellings":
        return {
            (u, v)
            for (V, u, v) in hellings(graph, cfg)
            if V == start_symbol and u in start_nodes and v in final_nodes
        }
    elif alg_type == "matrix":
        return {
            (u, v)
            for (V, u, v) in matrix(graph, cfg)
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


def matrix(graph: MultiDiGraph, cfg: CFG):
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
    adjs: dict[Variable, dok_array] = {
        v: dok_array((len(graph.nodes), len(graph.nodes)), dtype=bool)
        for v in cfg.variables
    }
    nodes = {n: i for i, n in enumerate(graph.nodes)}
    for (v, u, label) in graph.edges(data="label"):
        for prod in term_prod:
            if label == prod.body[0].value:
                adjs[prod.head][nodes[v], nodes[u]] = True

    for adj in adjs.values():
        adj.tocsr()
    diag = eye(len(nodes), dtype=bool, format="csr")

    for v in eps_prod:
        adjs[v.head] += diag
    changing = True
    while changing:
        changing = False
        for prod in var_prod:
            nnz_old = adjs[prod.head].nnz
            adjs[prod.head] += adjs[prod.body[0]] @ adjs[prod.body[1]]
            changing |= adjs[prod.head].nnz != nnz_old

    nodes = {i: n for n, i in nodes.items()}
    result = []
    for N, adj in adjs.items():
        for i, j in zip(*adj.nonzero()):
            result.append((N, nodes[i], nodes[j]))
    return result
