import pytest

from project.cfpq import *


@pytest.mark.parametrize(
    "cfg_str, graph_edges, expected_cfpq, start_nodes, final_nodes, alg_type",
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
            None,
            None,
            {"hellings", "matrix", "tensor"},
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
            {0, 2},
            {3},
            {"hellings", "matrix", "tensor"},
        ),
    ],
)
def test_cfpq(
    cfg_str,
    graph_edges,
    expected_cfpq,
    start_nodes,
    final_nodes,
    alg_type,
):
    cfg = CFG.from_text(cfg_str)
    graph = MultiDiGraph()
    graph.add_edges_from(graph_edges)
    for alg in alg_type:
        res_cfpq = cfpq(graph, cfg, start_nodes, final_nodes, alg_type=alg)
        assert res_cfpq == expected_cfpq
