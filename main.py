#!/usr/bin/env python

# core

import json
import logging
import sys

logging.basicConfig(level=logging.WARN)

mother_of = dict()

def trivial(p1, p2, t):
    "If p1 is the trivial antecedant of p2, return p1 as a truthy value."
    if p1 == p2:
        return p1

def upline(p1, p2, t, include_root=False):
    """Return all members of family tree upline of p1, stopping at p2.
    Include p1 in the return list, if include_root is True."""
    if include_root:
        upline = [ p1 ]
    else:
        upline = []

    logging.debug("Finding all members from %s up to %s", p1, p2)
    new_mother = p1

    while True:
        current = new_mother
        logging.debug("Current = %s", current)
        try:
            new_mother = mother_of[current]
        except KeyError:
            break
        logging.debug("New mother = %s", new_mother)
        upline.append(new_mother)
        if new_mother == p2:
            break

    logging.debug("Upline of %s is %s", p1, upline)
    return upline

def lineal_up(p1, p2, t):
    "Return True if p2 is a strict antecedent of p1."
    return p2 in upline(p1, p2, t)

def lineal_down(p1, p2, t):
    "Return True if p1 is a strict antecedent of p2."
    return p2 in upline(p2, p1, t)

def common_ancestor(p1, p2, t):
    "Return nearest common_ancestor of p1 and p2."
    line_1 = upline(p1, None, t, include_root=True) # get entire upline
    logging.debug("Line 1: %s", line_1)
    line_2 = upline(p2, None, t, include_root=True) # get entire upline
    logging.debug("Line 2: %s", line_2)
    for ancestor in line_1:
        if ancestor in line_2:
            return ancestor

def antecedent(p1, p2, t):
    """This function takes three parameters:

   1. A string representing the family tree
   2. The name of the first person
   3. The name of another person

   And returns the closest antecedent of two two given names."""
    if trivial(p1, p2, t):
        return trivial(p1, p2, t)
    if lineal_up(p1, p2, t):
        logging.debug("Relationship is lineal_up")
        return p2
    if lineal_down(p1, p2, t):
        logging.debug("Relationship is lineal_down")
        return p1
    if common_ancestor(p1, p2, t):
        logging.debug("Relationship is based on common_ancestor")
        return common_ancestor(p1, p2, t)
    raise Exception("No antecedent found.")

def deserialize(tree_as_string):
    """Presumption: the offspring are ALWAYS represented as a list, even when
    there is only 1."""
    return json.loads(tree_as_string)

def calculate_mothers(family_tree):
    for mother, children in family_tree.iteritems():
        for child in children:
            mother_of[child] = mother

def main(tree_as_string, person_1, person_2):
    family_tree = deserialize(tree_as_string)
    calculate_mothers(family_tree)
    logging.debug("Returning antecedent of %s and %s", person_1, person_2)
    return antecedent(person_1, person_2, family_tree)

import unittest
class TestTreeWalking(unittest.TestCase):

    def setUp(self):
        self.tree_as_string = """
{"Ann": ["Betty", "Clare"], "Betty": ["Donna", "Elizabeth", "Flora"], "Clare": ["Gloria", "Hazel"]}
        """
        self.family_tree = deserialize(self.tree_as_string)
        calculate_mothers(self.family_tree)

    def atest_upline_1(self):
        self.assertEqual(
            upline("Hazel", "Gloria", self.family_tree),
            ["Clare", "Ann"])

    def atest_common_1(self):
        self.assertEqual(
            common_ancestor("Hazel", "Flora", self.family_tree),
            "Ann")

    def atest_common_2(self):
        self.assertEqual(
            common_ancestor("Hazel", "Betty", self.family_tree),
            "Ann")

    def atest_common_3(self):
        self.assertEqual(
            common_ancestor("Hazel", "Ann", self.family_tree),
            "Ann")

    def atest_common_4(self):
        self.assertEqual(
            common_ancestor("Hazel", "Gloria", self.family_tree),
            "Clare")

    # 2 and 5 fail

    def atest_main_1(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Gloria"),
            "Clare")

    def atest_main_2(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Clare"),
            "Clare")

    def test_main_3(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Flora"),
            "Ann")

    def atest_main_4(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Betty"),
            "Ann")

    def atest_main_5(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Ann"),
            "Ann")

    def atest_main_6(self):
        self.assertEqual(
            main(self.tree_as_string, "Hazel", "Hazel"),
            "Hazel")




if __name__ == '__main__':
    """unittest.main()"""
    antecedent = main(*sys.argv[1:4])
    print antecedent
