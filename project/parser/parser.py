from pathlib import Path
from typing import Union

from antlr4 import InputStream, CommonTokenStream, ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl, ParseTreeWalker
from pydot import Dot, Edge, Node

from project.parser.GQLParser import GQLParser
from project.parser.GQLLexer import GQLLexer
from project.parser.GQLListener import GQLListener


def get_parser(inp: str) -> GQLParser:
    input_stream = InputStream(inp)
    lexer = GQLLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    return GQLParser(tokens)


def accept(inp: str) -> bool:
    parser = get_parser(inp)
    parser.removeErrorListeners()
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def save_in_dot(inp: str, file: Union[Path, str]):
    if not accept(inp):
        raise ValueError("The input does not belong to the language.")
    parser = get_parser(inp)
    listener = DotTree()
    ParseTreeWalker().walk(listener, parser.prog())
    listener.dot.write(str(file))


class DotTree(GQLListener):
    def __init__(self):
        self.dot = Dot("tree", graph_type="digraph")
        self.num_nodes = 0
        self.nodes = {}
        self.rules = GQLParser.ruleNames
        super(DotTree, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.dot.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.dot.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.dot.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.dot.add_node(Node(self.num_nodes, label=f"{node.getText()}"))
