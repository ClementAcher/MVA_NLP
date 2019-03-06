import numpy as np
import re
from collections import defaultdict


class PCFG:
    def __init__(self):
        self.rule_counter = defaultdict(lambda: defaultdict(float))

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
        self.rule_counter[rule[0]]['_'.join(rule[1:])] += 1

    def fill_PCFG(self, lines):
        for line in lines:
            line = self.clean_sentence(line)
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


def parse(filename='sequoia-corpus+fct.mrg_strict'):
    pcfg = PCFG()
    with open(filename, 'r', encoding='utf-8') as f:
        pcfg.fill_PCFG(f.readlines())
    return pcfg
