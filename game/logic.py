#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""logic.py: Houses wff-analyzing functions.
Formula -> stores string data with evaluative data about that string
  (validity and truth value).
truth_eval(str, int) -> bool: determines whether a wff is true.
wff_eval(str, int) -> bool: determines whether a string is a wff.
in above funcs, int is gamemode variable.
"""

__author__ = "Xavier Peregrino-Lujan"
__copyright__ = "Copyright 2021, Xavier Peregrino-Lujan"
__license__ = "GPL"
__version__ = "3.0"
__contact__ = "xaviperluj@gmail.com"
__status__ = "Development"  # or Prototype, Production


# debug block for testing in other modules
if __name__ != '__main__':
    prop_p = True
    prop_q = True
    prop_r = True
    prop_s = True
    # TODO: use os module to get absolute path to root folder, maybe
    path_start = 'game/'


class Pff(Exception):
    """raise when not a wff, but a pff.
    do not pass with an argument.
    """
    def __init__(self):
        default = 'Poorly-formed formula.'
        super().__init__(default)
    pass


def wff_eval(s, mode):
    """input: s is string that can encode a wff,
    mode is int -> {0: exclude o and i, 1: exclude i, 2: exclude o,
      3: include all variables}
    output: bool, whether input is a wff or not in x-wff language.
    """
    # Phase 1 - exclude obvious non-wffs
    valid_caps = ['N', 'C', 'A', 'K', 'E']
    valid_lows = ['p', 'q', 'r', 's', 'o', 'i']
    # check that s contains at least one propositional variable:
    if len([x for x in valid_lows if x in s]) == 0:
        return False
    # check that s contains all and only valid letters:
    if len([x for x in s if x in valid_caps or x in valid_lows]) == 0:
        return False
    # check that s is not longer than max possible wff size:
    if len(s) > 6:
        return False
    # check that s is legal in the current gamemode:
    if mode == 0:
        if 'o' in s or 'i' in s:
            return False
    elif mode == 1:
        if 'i' in s:
            return False
    elif mode == 2:
        if 'o' in s:
            return False
    # check that s is atomic if it is one character:
    if len(s) == 1 and s not in valid_lows:
        return False

    # Phase 2 - parse s as a stack of characters, read in left to right
    binary_caps = [x for x in valid_caps if x != 'N']
    stack = list(s)
    wffList = []  # bool values will be appended here
    while len(stack) > 0:
        # atomic wffs (lowercase) count as one wff and can appear
        # anywhere so long as the total num of wffs is
        # not greater than 1 by end:
        if stack[-1] in valid_lows:
            wffList.append(True)
            stack.pop()
            continue
        # unary connectives (N) can appear after at least 1 wff has
        # appeared:
        elif stack[-1] == 'N' and len(wffList) >= 1:
            stack.pop()
            continue
        # binary connectives (C, A, K, E) can appear after at least 2
        # wffs have appeared:
        elif stack[-1] in binary_caps and len(wffList) >= 2:
            wffList.pop()
            stack.pop()
            continue
        else:
            return False
    # string is a wff iff it is exactly 1 wff after evaluating
    # connectives
    if len(wffList) == 1:
        return True
    else:
        return False


def t_table(conn, val1, val2):
    """input: (connective, first truth value, second truth value)
    output: truth value; T, F, o, i, -i, To, -To, Fo, -Fo
    """
    # mappings between truth values and A table file code.
    # int numerals represent both a truth value and column/row index in
    #   the truth table file.
    # Ex. ('T', 'F') is encoded ('1', '0'), which is found at lines[1][0].
    encode = {'F': '0', 'T': '1', 'o': '2', 'i': '3', '-i': '4', 'To': '5',
              '-To': '6', 'Fo': '7', '-Fo': '8'
              }
    decode = {'0': 'F', '1': 'T', '2': 'o', '3': 'i', '4': '-i', '5': 'To',
              '6': '-To', '7': 'Fo', '8': '-Fo'
              }
    # N truth table
    negate = {'0': '1', '1': '0', '2': '2', '3': '4', '4': '3', '5': '8',
              '6': '7', '7': '6', '8': '5'
              }

    if conn == 'N':
        # int conversion only needed for subscripting the file
        return decode[negate[encode[val1]]]

    table_file = path_start + 'A_table.txt'
    if conn == 'A':
        with open(table_file, 'r') as file:
            lines = file.readlines()
            a_code = lines[int(encode[val1])][int(encode[val2])]
            a_val = decode[a_code]
            return a_val

    elif conn == 'K':
        with open(table_file, 'r') as file:
            lines = file.readlines()
            # Kxy <=> NANxNy
            neg_val1 = negate[encode[val1]]
            neg_val2 = negate[encode[val2]]
            k_code = negate[lines[int(neg_val1)][int(neg_val2)]]
            k_val = decode[k_code]
            return k_val

    elif conn == 'C':
        with open(table_file, 'r') as file:
            lines = file.readlines()
            # Cxy <=> ANxy
            neg_val1 = negate[encode[val1]]
            c_code = lines[int(neg_val1)][int(encode[val2])]
            c_val = decode[c_code]
            return c_val

    elif conn == 'E':
        with open(table_file, 'r') as file:
            lines = file.readlines()
            # Exy <=> NANANxyNANyx
            code_val1 = encode[val1]
            code_val2 = encode[val2]
            neg_val1 = negate[code_val1]
            neg_val2 = negate[code_val2]
            # get sub-disjunts ANxy and ANyx
            s_dis1 = lines[int(neg_val1)][int(code_val2)]
            s_dis2 = lines[int(neg_val2)][int(code_val1)]
            # get NAN(s_sdis1)N(s_dis2)
            e_code = negate[lines[int(negate[s_dis1])][int(negate[s_dis2])]]
            e_val = decode[e_code]
            return e_val


def truth_parse(s):
    """input: Formula, Formula.read is a string known to be a wff in the
      current gamemode.
    output: truth value of that wff.
    """
    # interpret the characters in wff from last to first
    t_stack = []
    for char in reversed(s):
        if char == 'p':
            if prop_p:
                prop_val = 'T'
            else:
                prop_val = 'F'
            t_stack.append(prop_val)
            continue
        elif char == 'q':
            if prop_q:
                prop_val = 'T'
            else:
                prop_val = 'F'
            t_stack.append(prop_val)
            continue
        elif char == 'r':
            if prop_r:
                prop_val = 'T'
            else:
                prop_val = 'F'
            t_stack.append(prop_val)
            continue
        elif char == 's':
            if prop_s:
                prop_val = 'T'
            else:
                prop_val = 'F'
            t_stack.append(prop_val)
            continue
        elif char == 'i':
            t_stack.append('i')
            continue
        elif char == 'o':
            t_stack.append('o')
            continue
        elif char == 'N':
            t_stack.append(t_table(char, t_stack.pop(), None))
        else:
            t_stack.append(t_table(char, t_stack.pop(), t_stack.pop()))
            continue
    return t_stack[0]


def truth_eval(s, mode):
    """input: s is string attempting to encode a wff in prefix form.
    mode is int -> {0: exclude o and i, 1: exclude i, 2: exclude o,
      3: include all variables}
    output: string, truth value given the predetermined truth values
      of atomic sentences p, q, r, and s.
    """
    # first pass to wff_eval() to test if f.read is a wff:
    if wff_eval(s, mode):
        return truth_parse(s)
    else:
        raise Pff


class Formula:
    """Formula(str, int) str is potential wff, int is gamemode.
    get_validity() returns and stores bool, whether string is a wff.
    get_truth() returns and stores str, truth value of that wff.
    """
    def __init__(self, letters, gamemode):
        self.read = letters
        self.gamemode = gamemode
        self.validity = None
        self.truth = None

    def get_validity(self):
        """stores and returns bool, whether Formula.read is a wff."""
        self.validity = wff_eval(self.read, self.gamemode)
        return self.validity

    def get_truth(self):
        """stores and returns string, truth value of Formula.read."""
        try:
            self.truth = truth_eval(self.read, self.gamemode)
            return self.truth
        except Pff:
            self.validity = False
            self.truth = 'pff'
            return self.truth


def main():
    debug_mode = 3
    temp = input('pass a formula to wff_eval(): ')
    f1 = Formula(temp, debug_mode)
    f1.get_validity()
    print(f1.validity)
    # debug truth assignment to atomic prop. variables:
    global path_start
    path_start = ''
    global prop_p
    prop_p = True
    global prop_q
    prop_q = True
    global prop_r
    prop_r = True
    global prop_s
    prop_s = True
    temp = input('pass a formula to truth_eval(): ')
    f2 = Formula(temp, debug_mode)
    f2.get_truth()
    print(f2.truth)


if __name__ == '__main__':
    print('testing logic.py...')
    main()
