from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA, State

from project.ecfg import ECFG


class RSM:
    def __init__(
        self,
        start_symbol: Variable,
        boxes: dict,
    ):
        self.start_symbol = start_symbol
        self.boxes = boxes

    @classmethod
    def ecfg_to_rsm(cls, ecfg: ECFG):
        boxes: dict = {}
        for key, value in ecfg.productions.items():
            boxes[key] = value.to_epsilon_nfa().to_deterministic()
        return cls(ecfg.start_symbol, boxes)

    def minimize(self):
        for key, value in self.boxes.items():
            self.boxes[key] = value.minimize()
        return self

    def merge_boxes_to_single_nfa(self):
        result = EpsilonNFA()
        for var, fa in self.boxes.items():
            for state in fa.start_states:
                result.add_start_state(State((var, state)))
            for state in fa.final_states:
                result.add_final_state(State((var, state)))
            for (start, symbol, finish) in fa:
                result.add_transition(
                    State((var, start)),
                    symbol,
                    State((var, finish)),
                )
        return result
