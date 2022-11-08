from pyformlang.cfg import Variable
from pyformlang.regular_expression import PythonRegex, Regex

from project.__init__ import *
import pytest
from project.ecfg import ECFG
from project.cfg_utils import read_cfg_from_text


@pytest.mark.parametrize(
    "path_to_file, ecfg_prod_exp",
    [
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg1",
            {
                Variable("S"): Regex("A B | D | T"),
                Variable("D"): Regex("Y"),
                Variable("Y"): Regex("z"),
                Variable("A"): Regex("a b"),
                Variable("B"): Regex(""),
            },
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg2",
            {
                Variable("S"): Regex("C D E"),
                Variable("D"): Regex("i"),
                Variable("C"): Regex("f G"),
                Variable("E"): Regex("j"),
                Variable("G"): Regex("h"),
            },
        ),
        (
            f"{str(shared.ROOT) + os.sep}cfg_files{os.sep}cfg3",
            {
                Variable("S"): Regex("A S B | c"),
                Variable("B"): Regex("b"),
                Variable("A"): Regex("a"),
            },
        ),
    ],
)
def test_cfg_to_ecfg(path_to_file, ecfg_prod_exp):
    cfg = read_cfg_from_text(path_to_file)
    ecfg = ECFG.from_cfg(cfg)
    for key in ecfg_prod_exp.keys():
        min_dfa = create_min_dfa_by_regex(ecfg.productions[key])
        min_dfa_exp = create_min_dfa_by_regex(ecfg_prod_exp[key])
        if min_dfa.is_empty() and min_dfa_exp.is_empty():
            continue
        assert min_dfa_exp.is_equivalent_to(min_dfa)


@pytest.mark.parametrize(
    "ecfg_str, ecfg_exp",
    [
        (
            """
                S -> a S | A c*
                A -> b
                """,
            {
                Variable("S"): Regex("a S | A c*"),
                Variable("A"): Regex("b"),
            },
        ),
        (
            """
                S -> A B C* | a b
                A -> e*
                B -> h
                C -> g
                """,
            {
                Variable("S"): Regex("A B C* | a b"),
                Variable("A"): Regex("e*"),
                Variable("B"): Regex("h"),
                Variable("C"): Regex("g"),
            },
        ),
    ],
)
def test_ecfg_from_text(ecfg_str, ecfg_exp):
    ecfg = ECFG.from_text(ecfg_str)
    for key in ecfg_exp.keys():
        min_dfa = create_min_dfa_by_regex(ecfg.productions[key])
        min_dfa_exp = create_min_dfa_by_regex(ecfg_exp[key])
        if min_dfa.is_empty() and min_dfa_exp.is_empty():
            continue
        assert min_dfa_exp.is_equivalent_to(min_dfa)
