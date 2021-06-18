#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_battery.py: Tests functions used by x-wff modules."""

__author__ = "Xavier Peregrino-Lujan"
__copyright__ = "Copyright 2021, Xavier Peregrino-Lujan"
__license__ = "GPL"
__version__ = "3.0"
__contact__ = "xaviperluj@gmail.com"
__status__ = "Development"  # or Prototype, Production


def main():
    from random import randint
    from game import logic

    # function from test file format to strings passable to logic.wff_check()
    def wff_tester_parse(s):
        valid_binary = ['C', 'A', 'K', 'E']
        valid_lows = ['p', 'q', 'r', 's', 'o', 'i']
        if s == 'N':
            return 'N'
        elif s == '2':
            return valid_binary[randint(0, 3)]
        elif s == 'a':
            return valid_lows[randint(0, 5)]
        else:
            raise Exception('Invalid character in file.')

    # open wff_test.txt, which contains templates for wff generation;
    # expected output is 20 True
    print('Testing logic.wff_eval()...')
    with open('testing/wff_test.txt', 'r') as file:
        i = 1
        for line in file:
            formula = ''
            for char in line:
                if char == '\n':
                    continue
                else:
                    formula += wff_tester_parse(char)
            print(str(i), formula, logic.wff_eval(formula),
                  sep=', ')
            i += 1
    print('Done')

    print('Testing logic.truth_eval()...')
    # default truth assignment to atomic prop. variables:
    global prop_p
    prop_p = True
    global prop_q
    prop_q = True
    global prop_r
    prop_r = True
    global prop_s
    prop_s = True
    with open('testing/wff_test.txt', 'r') as file:
        i = 1
        for line in file:
            formula = ''
            for char in line:
                if char == '\n':
                    continue
                else:
                    formula += wff_tester_parse(char)
            print(str(i), formula, logic.truth_eval(formula), sep=', ')
            i += 1
    print('Done')


if __name__ == '__main__':
    main()
