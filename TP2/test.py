from helper import levenshtein_distance, PCFG
from unittest import TestCase


class TestLevenshtein:
    """
    Test the Levenshtein distance function
    """

    def test_simple_case(self):
        """
        Simple case
        """
        assert levenshtein_distance('chat', 'chqt') == 1

    def test_same_string(self):
        """
        Same string
        """
        assert levenshtein_distance('pomme', 'pomme') == 0

    def test_different_lenght(self):
        """
        Different lenght
        """
        assert levenshtein_distance('pistou', 'pistouche') == 3

    def test_symmetry(self):
        """
        Test function symmetry
        """
        s1, s2 = 'peluche', 'trois'
        assert levenshtein_distance(s1, s2) == levenshtein_distance(s2, s1)


class TestPCFG(TestCase):
    def setUp(self):
        self.pcfg = PCFG()

    def test_clean_sentence(self):
        """
        Test the clean_sentence method
        """
        with_functionnals = "( (SENT (PP-MOD (P En) (NP (NC 1996))) (PONCT ,) (NP-SUJ (DET la) (NC municipalité)) (VN (V étudie)) (NP-OBJ (DET la) (NC possibilité) (PP (P d') (NP (DET une) (NC construction) (AP (ADJ neuve))))) (PONCT .)))"

        without_functionnals = "( (SENT (PP (P En) (NP (NC 1996))) (PONCT ,) (NP (DET la) (NC municipalité)) (VN (V étudie)) (NP (DET la) (NC possibilité) (PP (P d') (NP (DET une) (NC construction) (AP (ADJ neuve))))) (PONCT .)))"

        assert PCFG.clean_sentence(with_functionnals) == without_functionnals

        already_clean = "( (SENT (PP (P En) (NP (NC 1996))) (PONCT ,)"
        assert PCFG.clean_sentence(already_clean) == already_clean

    # def test_fill_PCFG(self):
    #     sent = "(SENT (PP (P En) (NP (NC 1996))) (PONCT ,))"
    #     # rules = [['SENT', ]]
    #     rules = [['NC', '1996'], ['P', 'En'], ['PONCT', ','], ['NP', 'NC'],
    #              ['PP', 'P', 'NP'], ['SENT', 'PP', 'PONCT']]
    #     self.assertCountEqual(rules, self.pcfg.fill_PCFG(sent))

    def test_add_rule(self):
        """
        Test the _add_rule method
        """
        rules = [['NC', '1996'], ['P', 'En'], ['PONCT', ','], ['NP', 'NC'],
                 ['PP', 'P', 'NP'], ['SENT', 'PP', 'PONCT']]

        for rule in rules:
            self.pcfg._add_rule(rule)

        for rule in rules:
            assert self.pcfg.rule_counter[rule[0]]['_'.join(rule[1:])] == 1
