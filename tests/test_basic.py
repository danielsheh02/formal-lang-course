import filecmp
from project.__init__ import *
import networkx as nx


def test_create_two_cycles_graph():
    graph_expected = cfpq_data.labeled_two_cycles_graph(40, 40, labels=("a", "b"))
    graph = create_two_cycles_graph(40, 40, ("a", "b"))
    em = nx.algorithms.isomorphism.categorical_multiedge_match("label", None)
    assert nx.is_isomorphic(graph, graph_expected, edge_match=em)


def test_save_graph_in_dot():
    graph_expected = cfpq_data.labeled_two_cycles_graph(40, 40, labels=("a", "b"))
    save_in_dot(graph_expected)
    assert filecmp.cmp(
        str(shared.ROOT) + os.sep + "output" + os.sep + "graph.dot",
        str(shared.ROOT) + os.sep + "output" + os.sep + "expected_graph.dot",
    )


def test_get_graph_info_by_graph():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    info_by_graph = get_info_by_graph(graph)
    assert info_by_graph.number_of_nodes == 7
    assert info_by_graph.number_of_edges == 8
    assert info_by_graph.labels == ["a", "a", "a", "a", "b", "b", "b", "b"]


def test_get_graph_info_by_name():
    info_by_name = get_info_by_name("univ")
    assert info_by_name.number_of_nodes == 179
    assert info_by_name.number_of_edges == 293
    assert info_by_name.labels == [
        "someValuesFrom",
        "type",
        "onProperty",
        "type",
        "subClassOf",
        "label",
        "range",
        "type",
        "label",
        "domain",
        "label",
        "type",
        "label",
        "subClassOf",
        "type",
        "subClassOf",
        "label",
        "type",
        "first",
        "rest",
        "someValuesFrom",
        "type",
        "onProperty",
        "subClassOf",
        "type",
        "label",
        "subPropertyOf",
        "type",
        "label",
        "label",
        "subClassOf",
        "type",
        "type",
        "subClassOf",
        "label",
        "rest",
        "first",
        "rest",
        "first",
        "type",
        "label",
        "type",
        "onProperty",
        "someValuesFrom",
        "domain",
        "label",
        "type",
        "range",
        "label",
        "type",
        "label",
        "subPropertyOf",
        "type",
        "type",
        "inverseOf",
        "label",
        "label",
        "intersectionOf",
        "type",
        "rest",
        "first",
        "versionInfo",
        "comment",
        "label",
        "type",
        "subPropertyOf",
        "label",
        "range",
        "type",
        "domain",
        "range",
        "inverseOf",
        "type",
        "domain",
        "label",
        "type",
        "subClassOf",
        "label",
        "domain",
        "label",
        "range",
        "type",
        "inverseOf",
        "label",
        "subClassOf",
        "type",
        "type",
        "subClassOf",
        "label",
        "intersectionOf",
        "first",
        "rest",
        "type",
        "label",
        "range",
        "domain",
        "label",
        "type",
        "type",
        "label",
        "first",
        "rest",
        "label",
        "intersectionOf",
        "type",
        "rest",
        "first",
        "domain",
        "type",
        "range",
        "label",
        "first",
        "rest",
        "type",
        "label",
        "range",
        "label",
        "type",
        "domain",
        "label",
        "type",
        "intersectionOf",
        "type",
        "subClassOf",
        "label",
        "label",
        "type",
        "subClassOf",
        "subClassOf",
        "type",
        "label",
        "range",
        "type",
        "label",
        "domain",
        "type",
        "subClassOf",
        "label",
        "subClassOf",
        "type",
        "label",
        "domain",
        "subPropertyOf",
        "type",
        "range",
        "label",
        "label",
        "type",
        "domain",
        "range",
        "label",
        "range",
        "type",
        "domain",
        "label",
        "subClassOf",
        "type",
        "type",
        "subClassOf",
        "subClassOf",
        "label",
        "someValuesFrom",
        "type",
        "onProperty",
        "rest",
        "first",
        "type",
        "onProperty",
        "someValuesFrom",
        "type",
        "label",
        "subClassOf",
        "type",
        "label",
        "range",
        "domain",
        "label",
        "type",
        "subClassOf",
        "label",
        "subClassOf",
        "type",
        "someValuesFrom",
        "type",
        "onProperty",
        "label",
        "subClassOf",
        "type",
        "type",
        "subClassOf",
        "label",
        "type",
        "label",
        "subClassOf",
        "domain",
        "type",
        "label",
        "range",
        "someValuesFrom",
        "type",
        "onProperty",
        "subClassOf",
        "label",
        "type",
        "domain",
        "range",
        "type",
        "label",
        "first",
        "rest",
        "type",
        "subClassOf",
        "label",
        "domain",
        "label",
        "type",
        "intersectionOf",
        "label",
        "type",
        "type",
        "label",
        "range",
        "domain",
        "domain",
        "label",
        "type",
        "type",
        "label",
        "label",
        "subClassOf",
        "type",
        "type",
        "subClassOf",
        "subClassOf",
        "label",
        "subClassOf",
        "type",
        "label",
        "type",
        "label",
        "subClassOf",
        "intersectionOf",
        "subClassOf",
        "label",
        "type",
        "someValuesFrom",
        "type",
        "onProperty",
        "label",
        "type",
        "domain",
        "domain",
        "label",
        "type",
        "subClassOf",
        "type",
        "label",
        "type",
        "domain",
        "label",
        "label",
        "subClassOf",
        "type",
        "subClassOf",
        "label",
        "type",
        "subClassOf",
        "label",
        "type",
        "type",
        "domain",
        "label",
        "label",
        "type",
        "domain",
        "type",
        "range",
        "label",
        "domain",
        "label",
        "type",
        "subClassOf",
        "label",
        "subPropertyOf",
        "range",
        "type",
        "domain",
        "label",
        "type",
        "first",
        "rest",
        "label",
        "type",
    ]
