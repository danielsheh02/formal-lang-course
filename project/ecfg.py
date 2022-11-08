from typing import AbstractSet

from pyformlang.cfg import Variable, Terminal, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable],
        start_symbol: Variable,
        productions: dict,
        terminals: AbstractSet[Terminal] = None,
    ):
        self.variables = variables
        self.start_symbol = start_symbol
        self.productions = productions
        self.terminals = terminals

    @classmethod
    def from_cfg(cls, cfg: CFG):
        productions: dict = {}
        for prod in cfg.productions:
            body = Regex(
                " ".join(symb.value for symb in prod.body) if len(prod.body) > 0 else ""
            )
            productions[prod.head] = (
                productions[prod.head].union(body) if prod.head in productions else body
            )
        return cls(
            set(cfg.variables), cfg.start_symbol, productions, set(cfg.terminals)
        )

    @classmethod
    def from_file(cls, path_to_file):
        with open(path_to_file, "r") as file:
            ecfg_string = file.read()
        return cls.from_text(ecfg_string)

    @classmethod
    def from_text(cls, text: str, start_symbol=Variable("S")):
        variables = set()
        productions = dict()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            production = line.split("->")
            if len(production) != 2:
                raise Exception(f"Error in line: {line}")
            head = Variable(production[0].strip())
            body = Regex(production[1].strip())
            if head in variables:
                raise Exception(f"Error in line: {line}")
            variables.add(head)
            productions[head] = body
        return cls(variables, start_symbol, productions)
