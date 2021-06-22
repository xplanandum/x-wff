#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""logic.py: Houses wff-analyzing functions.
truth_eval(str) -> bool: determines whether a wff is true.
wff_eval(str) -> bool: determines whether a string is a wff.
"""

__author__ = "Xavier Peregrino-Lujan"
__copyright__ = "Copyright 2021, Xavier Peregrino-Lujan"
__license__ = "GPL"
__version__ = "3.0"
__contact__ = "xaviperluj@gmail.com"
__status__ = "Development"  # or Prototype, Production


if __name__ != '__main__':
    prop_p = True
    prop_q = True
    prop_r = True
    prop_s = True
    path_start = 'game/'


class Pff(Exception):
    """raise when not a wff, but a pff.
    meta-exception occurs when argument is passed.
    """
    def __init__(self):
        default = 'Poorly-formed formula.'
        super().__init__(default)
    pass


def wff_eval(f):
    """ input: Formula, Formula.read is the string that can encode a wff.
           Formula.gamemode is int -> {0: exclude o and i, 1: exclude i,
           2: exclude o, 3: include all variables}
    output: bool, whether input is a wff or not in x-wff language.

      misc: accepts combinations of 'NCAKEpqrsio' characters up to 6 long.
    """

    s = f.read
    mode = f.gamemode
    # Phase 1 - exclude obvious non-wffs
    valid_caps = ['N', 'C', 'A', 'K', 'E']
    valid_lows = ['p', 'q', 'r', 's', 'o', 'i']
    # check that s contains all and only valid letters:
    for char in list(s):
        if char not in valid_caps and char not in valid_lows:
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


def t_table(conn, v1, v2):
    """ input: (connective, first truth value, second truth value)
    output: truth value; T, F, o, i, -i, To, -To, Fo, -Fo
    """
    table_file = path_start + 'A_table.txt'
    with open(table_file, 'r') as file:
        # mappings between truth values and A table file code.
        # int numerals represent both a truth value and column/row index in
        #   the truth table file.
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
            return decode[negate[encode[v1]]]
        elif conn == 'A':
            lines = file.readlines()
            A_code = lines[int(encode[v1])][int(encode[v2])]
            A_val = decode[A_code]
            return A_val
        elif conn == 'K':
            lines = file.readlines()
            # Kxy <=> NANxNy
            nv1 = negate[encode[v1]]
            nv2 = negate[encode[v2]]
            K_code = negate[lines[int(nv1)][int(nv2)]]
            K_val = decode[K_code]
            return K_val
        elif conn == 'C':
            lines = file.readlines()
            # Cxy <=> ANxy
            nv1 = negate[encode[v1]]
            C_code = lines[int(nv1)][int(encode[v2])]
            C_val = decode[C_code]
            return C_val
        elif conn == 'E':
            lines = file.readlines()
            # Exy <=> NANANxyNANyx
            cv1 = encode[v1]
            cv2 = encode[v2]
            nv1 = negate[cv1]
            nv2 = negate[cv2]
            # get sub-disjunts ANxy and ANyx
            s_dis1 = lines[int(nv1)][int(cv2)]
            s_dis2 = lines[int(nv2)][int(cv1)]
            # get NAN(s_sdis1)N(s_dis2)
            E_code = negate[lines[int(negate[s_dis1])][int(negate[s_dis2])]]
            E_val = decode[E_code]
            return E_val


def truth_parse(f):
    """ input: Formula, Formula.read is a string known to be a wff in the
           current gamemode.
    output: truth value of that wff.
    """
    # interpret the characters in wff from last to first
    t_stack = []
    for char in reversed(f.read):
        if char == 'p':
            if prop_p:
                temp = 'T'
            else:
                temp = 'F'
            t_stack.append(temp)
            continue
        elif char == 'q':
            if prop_q:
                temp = 'T'
            else:
                temp = 'F'
            t_stack.append(temp)
            continue
        elif char == 'r':
            if prop_r:
                temp = 'T'
            else:
                temp = 'F'
            t_stack.append(temp)
            continue
        elif char == 's':
            if prop_s:
                temp = 'T'
            else:
                temp = 'F'
            t_stack.append(temp)
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


def truth_eval(f):
    """ input: Formula, Formula.read is a string attempting to encode a wff
           in prefix form.
    output: string, truth value given the predetermined truth values
            of atomic sentences p, q, r, and s.
    """
    # first pass to wff_eval() to test if f.read is a wff:
    if wff_eval(f):
        return truth_parse(f)
    else:
        raise Pff


class Formula:
    """
    """
    def __init__(self, letters, gamemode):

        self.read = letters
        self.gamemode = gamemode
        self.validity = None
        self.truth = None

    def get_validity(self):
        """stores and returns bool, whether Formula.read is a wff."""
        self.validity = wff_eval(self)
        return self.validity

    def get_truth(self):
        """stores and returns string, truth value of Formula.read."""
        self.truth = truth_eval(self)
        return self.truth


def main():
    default_mode = 3
    temp = input('pass a formula to wff_eval(): ')
    f1 = Formula(temp, default_mode)
    f1.get_validity()
    print(f1.validity)
    # debug truth assignment to atomic prop. variables:
    #TODO: pull default props from text file, write new ones to same text file
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
    f2 = Formula(temp, default_mode)
    f2.get_truth()
    print(f2.truth)


if __name__ == '__main__':
    main()
