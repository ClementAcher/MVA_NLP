import re
from collections import defaultdict

import numpy as np

INNER_PARENTHESIS = re.compile('\(([^()]+)\)')


class PCFG:

    HASHABLE_CHAR = '_'  # char used to join NT symbols in the dict
    TRANS_CHAR = '+'  # char used to join NT symbols to create transition rules

    def __init__(self):
        self.rule_counter = defaultdict(lambda: defaultdict(float))
        self.lexicon = defaultdict(lambda: defaultdict(float))
        self.reversed_lexicon = defaultdict(lambda: defaultdict(float))

    @staticmethod
    def clean_sentence(sentence):
        """
        Remove functional labels from tree bank sample

        Args:
        - sentence (str) : single sample from tree bank

        Returns:
        - cleaned_sentence (str) : sentence without any functional labels
        """
        return re.sub(r'(-)\w+', '', sentence)

    def _add_rule(self, rule):
        """
        Add/increment by one the counter corresponding to the rule

        Args:
        - rule (list) : the rule is rule[0] -> rule[1]rule[2]...rule[-1]
        """
        # Don't add a rule that is already in the lexicon
        if (len(rule) != 2) or (rule[1] not in self.reversed_lexicon.keys()):
            # Remove functional labels
            cleaned_rule = [self.clean_sentence(tag) for tag in rule]

            self.rule_counter[cleaned_rule[0]][self.HASHABLE_CHAR.join(
                cleaned_rule[1:])] += 1

    def fill_lexicon(self, lines):
        for line in lines:
            matchs = INNER_PARENTHESIS.findall(line)
            for match in matchs:
                non_term, term = match.split()
                non_term = self.clean_sentence(non_term)
                self.lexicon[non_term][term] += 1
                self.reversed_lexicon[term][non_term] += 1

    def fill_PCFG(self, lines):
        """
        Fill rule_counter in a linear time by line
        """
        for line in lines:
            # line = self.clean_sentence(line)
            # Get the sentence as a list of tags
            list_tags = line.replace('(', '( ').replace(')', ' )').split()
            stack = []
            for tag in list_tags:
                if tag != ')':
                    stack.append(tag)
                else:
                    current_rule = []
                    while stack[-1] != '(':
                        current_rule.insert(0, stack.pop())
                    # Remove the ')'
                    stack.pop()
                    # And replace it with the tag
                    stack.append(current_rule[0])
                    self._add_rule(current_rule)

    def normalize_rules(self):
        pass

    def train(self, lines):
        self.fill_lexicon(lines)
        self.fill_PCFG(lines)


def levenshtein_distance(s1, s2):
    """
    Compute the Levenshtein distance between two strings

    Args:
    - s1, s2 (str)

    Returns:
    - distance (int)
    """

    d = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)
    cost = 0

    for i in range(len(s1) + 1):
        d[i, 0] = i
    for j in range(len(s2) + 1):
        d[0, j] = j

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1,
                          d[i - 1, j - 1] + cost)

    return d[-1, -1]


def tree_to_sentence(line):
    """Get the sequence of token from a treebank sample"""
    matchs = INNER_PARENTHESIS.findall(line)
    for match in matchs:
        non_term, term = match.split()
        print(non_term, term)


def parse(filename='./data/sequoia-corpus+fct.mrg_strict'):
    pcfg = PCFG()
    with open(filename, 'r', encoding='utf-8') as f:
        pcfg.train(f.readlines())
    return pcfg
