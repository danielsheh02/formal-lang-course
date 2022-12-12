from pyformlang.cfg import CFG


def to_wcnf(cfg: CFG) -> CFG:
    cfg_new = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = cfg_new._get_productions_with_only_single_terminals()
    new_productions = cfg_new._decompose_productions(new_productions)
    return CFG(start_symbol=cfg_new.start_symbol, productions=set(new_productions))


def read_cfg_from_text(path_to_file) -> CFG:
    with open(path_to_file, "r") as file:
        cfg_string = file.read()
    return CFG.from_text(cfg_string)


def cyk(cfg: CFG, word: str):
    cnf = cfg.to_normal_form()
    len_word = len(word)
    if len_word == 0:
        return cfg.generate_epsilon()
    term_prod = [t for t in cnf.productions if len(t.body) == 1]
    var_prod = [v for v in cnf.productions if len(v.body) == 2]
    M = [[(set("")) for _ in range(len_word)] for _ in range(len_word)]
    for i in range(len_word):
        M[i][i].update(
            prod.head.value for prod in term_prod if word[i] == prod.body[0].value
        )
    for i in range(1, len_word):
        for j in range(len_word - i):
            k = j + i
            for z in range(j, k):
                for prod in var_prod:
                    if (
                        prod.body[0].value in M[j][z]
                        and prod.body[1].value in M[z + 1][k]
                    ):
                        M[j][k].update({prod.head.value})
    return cnf.start_symbol.value in M[0][len_word - 1]
