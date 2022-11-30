from networkx import MultiDiGraph
from pyformlang.cfg import Variable
from scipy.sparse import dok_array, eye, lil_matrix

from project import create_nfa_by_graph, BoolAutomaton
from project.cfg_utils import *
from project.ecfg import ECFG
from project.rsm import RSM


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
    elif alg_type == "tensor":
        return {
            (u, v)
            for (V, u, v) in tensor(graph, cfg)
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


def tensor(graph: MultiDiGraph, cfg: CFG):
    bool_mtx_rsm = BoolAutomaton(
        RSM.ecfg_to_rsm(ECFG.from_cfg(cfg)).minimize().merge_boxes_to_single_nfa()
    )
    bool_mtx_graph = BoolAutomaton(create_nfa_by_graph(graph))
    identity_matrix = eye(bool_mtx_graph.number_of_states, format="dok", dtype=bool)
    for nonterm in cfg.get_nullable_symbols():
        if nonterm.value in bool_mtx_graph.edges.keys():
            bool_mtx_graph.edges[nonterm.value] += identity_matrix
        else:
            bool_mtx_graph.edges[nonterm.value] = identity_matrix

    last_transitive_closure_idxs_len = 0

    while True:
        transitive_closure_idxs = list(
            zip(*bool_mtx_rsm.intersect(bool_mtx_graph).transitive_closure().nonzero())
        )
        if len(transitive_closure_idxs) == last_transitive_closure_idxs_len:
            break
        last_transitive_closure_idxs_len = len(transitive_closure_idxs)
        for (i, j) in transitive_closure_idxs:
            r_i, r_j = (
                i // bool_mtx_graph.number_of_states,
                j // bool_mtx_graph.number_of_states,
            )
            g_i, g_j = (
                i % bool_mtx_graph.number_of_states,
                j % bool_mtx_graph.number_of_states,
            )
            state_from = bool_mtx_rsm.number_state[r_i]
            state_to = bool_mtx_rsm.number_state[r_j]
            nonterm, _ = state_from.value
            if (
                state_from in bool_mtx_rsm.start_states
                and state_to in bool_mtx_rsm.final_states
            ):
                if nonterm.value in bool_mtx_graph.edges.keys():
                    bool_mtx_graph.edges[nonterm][g_i, g_j] = True
                else:
                    bool_mtx_graph.edges[nonterm] = lil_matrix(
                        (
                            bool_mtx_graph.number_of_states,
                            bool_mtx_graph.number_of_states,
                        ),
                        dtype=bool,
                    )
                    bool_mtx_graph.edges[nonterm][g_i, g_j] = True
    return {
        (
            nonterm,
            bool_mtx_graph.number_state[graph_i],
            bool_mtx_graph.number_state[graph_j],
        )
        for nonterm, mtx in bool_mtx_graph.edges.items()
        for graph_i, graph_j in zip(*mtx.nonzero())
    }
