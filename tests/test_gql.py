import filecmp
import os

import pytest

from project.parser.parser import *


@pytest.mark.parametrize(
    "prog, result",
    [
        (""" graph = load_graph("some_path"); """, True),
        (""" graph = add_start({node1, node2}, graph); """, True),
        (""" graph = add_final({node1, node2}, graph); """, True),
        (""" graph = set_start({node1, node2}, graph); """, True),
        (""" graph = set_final({node1, node2}, graph); """, True),
    ],
)
def test_graph_funs(prog, result):
    assert accept(prog) == result


@pytest.mark.parametrize(
    "prog, result",
    [
        (""" vertices = get_start(graph); """, True),
        (""" vertices = get_final(graph); """, True),
        (""" vertices = get_vertices(graph); """, True),
        (""" vertices = get_reachable(graph); """, True),
        (""" vertices = {v1, v2, 1, true, "string"}; """, True),
    ],
)
def test_vertices_funs(prog, result):
    assert accept(prog) == result


@pytest.mark.parametrize(
    "prog, result",
    [
        (""" edges = get_edges(graph); """, True),
        (""" edges = {e1, e2, (1, l1, 2), (1, true, 2), (1, "string", 2)}; """, True),
    ],
)
def test_edges_funs(prog, result):
    assert accept(prog) == result


@pytest.mark.parametrize(
    "prog, result",
    [
        (""" labels = get_labels(graph); """, True),
        (""" labels = {l1, l2, 1, false, "string"}; """, True),
    ],
)
def test_labels_funs(prog, result):
    assert accept(prog) == result


@pytest.mark.parametrize(
    "prog, result",
    [
        (""" set_of_labels = map(lambda label: label, get_labels(graph)); """, True),
        (""" set_of_vert = filter(lambda v: (v IN {1, 5} ), {1, 2, 3, 5}); """, True),
        (""" intersection = intersect("string", expr2); """, True),
        (""" concatenation = concat("string", expr2); """, True),
        (""" unification = union("string", expr2); """, True),
        (""" klini = star(expr1); """, True),
        (""" klini = star("string"); """, True),
    ],
)
def test_expr_funs(prog, result):
    assert accept(prog) == result


@pytest.mark.parametrize(
    "prog, result",
    [
        (
            """
        graph = load_graph ("some_path");
        graph1 = set_start (get_vertices (graph), graph);
        graph2 = set_final (get_start (graph1), graph1);

        query = star (union ("a", star ("b")));

        intersection = intersect (graph2, query);

        print (intersection);
        """,
            True,
        )
    ],
)
def test_mini_prog(prog, result):
    assert accept(prog) == result


def test_write_in_dot():
    text = """
        graph = load_graph ("some_path");
        graph1 = set_start (get_vertices (graph), graph);
        graph2 = set_final (get_start (graph1), graph1);

        query = star (union ("a", star ("b")));

        intersection = intersect (graph2, query);

        print (intersection);
    """
    save_in_dot(text, "tests/dot/output_tree.dot")
    assert filecmp.cmp(
        "tests/dot/output_tree.dot", "tests/dot/expected_tree.dot", shallow=False
    )
    os.remove("tests/dot/output_tree.dot")
