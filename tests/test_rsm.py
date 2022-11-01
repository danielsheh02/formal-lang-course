import pytest
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.__init__ import *
from project.cfg_utils import read_cfg_from_text
from project.ecfg import ECFG
from project.rsm import RSM


@pytest.mark.parametrize(
    "path_to_file, prod_exp",
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
def test_ecfg_rsm(path_to_file, prod_exp):
    cfg = read_cfg_from_text(path_to_file)
    rsm = RSM.ecfg_to_rsm(ECFG.from_cfg(cfg))
    for key in prod_exp.keys():
        dfa_exp = create_min_dfa_by_regex(prod_exp[key])
        if rsm.boxes[key].is_empty() and dfa_exp.is_empty():
            continue
        assert rsm.boxes[key].is_equivalent_to(dfa_exp)
