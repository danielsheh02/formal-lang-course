# from typing import AbstractSet
#
# from pyformlang.cfg import Variable, Terminal, CFG
# from pyformlang.regular_expression import PythonRegex
#
#
# class ECFG:
#     def __init__(
#         self,
#         variables: AbstractSet[Variable],
#         terminals: AbstractSet[Terminal],
#         start_symbol: Variable,
#         productions: dict,
#     ):
#         self.variables = variables
#         self.terminals = terminals
#         self.start_symbol = start_symbol
#         self.productions = productions
#
#     @classmethod
#     def cfg_to_ecfg(cls, cfg: CFG):
#         productions: dict = {}
#         for prod in cfg.productions:
#             body = PythonRegex(
#                 " ".join(symb.value for symb in prod.body) if len(prod.body) > 0 else ""
#             )
#             productions[prod.head] = (
#                 productions[prod.head].union(body) if prod.head in productions else body
#             )
#         return cls(
#             set(cfg.variables), set(cfg.terminals), cfg.start_symbol, productions
#         )