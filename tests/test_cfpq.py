import pytest

from project.cfpq import *


@pytest.mark.parametrize(
    "cfg_str, graph_edges, expected_cfpq, expected_res_alg, start_nodes, final_nodes, alg_type",
    [
        (
            """
                            S -> A B
                            S -> A C
                            C -> S B
                            A -> a
                            B -> b
                        """,
            [
                (0, 1, {"label": "a"}),
                (1, 2, {"label": "a"}),
                (2, 0, {"label": "a"}),
                (2, 3, {"label": "b"}),
                (3, 2, {"label": "b"}),
            ],
            {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)},
            [
                (Variable("A"), 0, 1),
                (Variable("A"), 1, 2),
                (Variable("A"), 2, 0),
                (Variable("B"), 2, 3),
                (Variable("B"), 3, 2),
                (Variable("S"), 1, 3),
                (Variable("C"), 1, 2),
                (Variable("S"), 0, 2),
                (Variable("C"), 0, 3),
                (Variable("S"), 2, 3),
                (Variable("C"), 2, 2),
                (Variable("S"), 1, 2),
                (Variable("C"), 1, 3),
                (Variable("S"), 0, 3),
                (Variable("C"), 0, 2),
                (Variable("S"), 2, 2),
                (Variable("C"), 2, 3),
            ],
            None,
            None,
            {"hellings", "matrix"},
        ),
        (
            """
                            S -> A B
                            S -> A C
                            C -> S B
                            A -> a
                            B -> b
                        """,
            [
                (0, 1, {"label": "a"}),
                (1, 2, {"label": "a"}),
                (2, 0, {"label": "a"}),
                (2, 3, {"label": "b"}),
                (3, 2, {"label": "b"}),
            ],
            {(0, 3), (2, 3)},
            [
                (Variable("A"), 0, 1),
                (Variable("A"), 1, 2),
                (Variable("A"), 2, 0),
                (Variable("B"), 2, 3),
                (Variable("B"), 3, 2),
                (Variable("S"), 1, 3),
                (Variable("C"), 1, 2),
                (Variable("S"), 0, 2),
                (Variable("C"), 0, 3),
                (Variable("S"), 2, 3),
                (Variable("C"), 2, 2),
                (Variable("S"), 1, 2),
                (Variable("C"), 1, 3),
                (Variable("S"), 0, 3),
                (Variable("C"), 0, 2),
                (Variable("S"), 2, 2),
                (Variable("C"), 2, 3),
            ],
            {0, 2},
            {3},
            {"hellings", "matrix"},
        ),
    ],
)
def test_cfpq(
    cfg_str,
    graph_edges,
    expected_cfpq,
    expected_res_alg,
    start_nodes,
    final_nodes,
    alg_type,
):
    cfg = CFG.from_text(cfg_str)
    graph = MultiDiGraph()
    graph.add_edges_from(graph_edges)
    for alg in alg_type:
        res_cfpq = cfpq(graph, cfg, start_nodes, final_nodes, alg_type=alg)
        if alg == "hellings":
            res_alg = hellings(graph, cfg)
        else:
            res_alg = matrix(graph, cfg)
        assert res_cfpq == expected_cfpq
        assert set(res_alg) == set(expected_res_alg)
