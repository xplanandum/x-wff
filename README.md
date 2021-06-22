# x-wff
Propositional logic game featuring Łukasiewicz notation and many-valued logic

--Under development--

Here is an early draft of x-wff's rules (as a tabletop game):

x-wff rulebook v1.0 by Xavier Peregrino-Lujan

Goal of the game:

Each player takes their/her/his outcome of a dice roll and constructs a 
well-formed formula (wff). Points are earned by forming wffs that are true 
according to a set of agreed-upon propositions.

Needed:

- 6 lowercase dice, faces 'p', 'q', 'r', 's', 'i', 'o'
- 6 uppercase dice, faces 'N', 'K', 'A', 'C', 'E', 'R'
- A place to store the values of 'p', 'q', 'r', 's', and player scores 
  (optionally, use only your brain for Platonic conduct)
- 2 players who are ready to advance/exercise their knowledge of propositional 
  logic

Background:

'p', 'q', 'r', and 's' are variables that range over propositions. As such, 
each letter denotes a well-formed expression in some language. For the game to 
work, each proposition needs to have an agreed upon truth value, T or F. 
Different variables can share the same linguistic value or truth value.

'i' and 'o' are artifacts from a proof-oriented predecessor of this game. x-wff 
implements them like so: if an 'i' is rolled, the die will be rolled again and 
the next roll will be fixed (no re-rolling of subsequent 'i's); if a 'o' is 
rolled, nothing happens. If the only lowercase letters that were rolled are 
'i's or 'o's, one lowercase die will be re-rolled until a 'p', 'q', 'r', or 
's' is obtained. These odd-sounding rules are in place because 'i' and 'o' are 
not usable symbols when forming wffs, and at least one proposition is needed 
to make a wff.

'N', 'K', 'A', 'C', and 'E' are logical constants in the 'Polish' Łukasiewicz 
(woo/cahsh/uh/vits) prefix notation. Here is a table with information about 
each constant:

X | name          | letter origin      | arity  | example
--|---------------|--------------------|--------|-------------------------
N | negation      | from 'Negacja'     | unary  | Np  = not-p
K | conjunction   | from 'Koniunkja'   | binary | Kpq = p and q
A | disjunction   | from 'Alternatywa' | binary | Apq = p or q
C | conditional   | from 'implikaCja'  | binary | Cpq = if p, then q
E | biconditional | from 'Ekiwalencja' | binary | Epq = p if and only if q

The 'R' face of the uppercase dice is a wildcard constant: you get to choose! 
When 'R' is rolled, the player can change the die to 'N', 'K', 'A', or 'C' 
at any point in the round. After this, the side of the die cannot be changed.

The conditionals (C and E) used in this game are material conditionals. 
This means that the 'Cpq' is false only when 'p' is true and 'q' is false. It 
does not matter what 'p' and 'q' stand for. The same linguistic insensitivity 
applies with biconditionals. Truth tables for each logical constant are 
appended to this text. From now on, I assume that you understand the truth 
conditions for all wffs built from these constants.

Rules:

- Before the game

This game does not allow poorly-formed formulas. If you spot one, scoff: "pff!" 
But to know what a pff is, you need to know what a wff is. A wff is a string of 
symbols that satisfies one of the following conditions:

Rule                                       | example
-------------------------------------------|--------
1. it is a single proposition character    | p
2. it is the unary constant before a wff   | NKpq
3. it is a binary constant before two wffs | EAqrs (can also be written EsAqr)

These rules can be applied repeatedly to generate all and only wffs in the dice 
language. That is to say, the grammar of x-wff is generatively sound and 
complete over its logical constants and proposition variables p-s 
[see endnote 1].

So, a pff is a string of symbols that is not a wff, like 'C', 'Npq', 'rs', or 
'Zq'.

- Starting the game

1. Each player takes 3 lowercase and 3 uppercase dice.
2. The players come up with 4 propositions, settle on a truth value for each 
   proposition, and assign each one a unique letter, 'p', 'q', 'r', or 's'. 
   These substeps can be done in any order.

- Playing a round

3. The players roll their dice.
4. Roll any 'i' dice again.
5. If a player's lowercase dice are all 'i's, all 'o's, or some combination of 
   only 'i's and 'o's, then that player rolls one lowercase die until a 'p', 
   'q', 'r', or 's' is obtained.
6. The players each construct the longest true wff possible. Some wff is 
   guaranteed to be constructible with any roll at this point.

- Scoring the results

7. Calculate the truth value of the wffs. Award one point to each player who 
   has constructed a true wff. False wffs get nothing.
8. If a player spots a longer true wff that the opposing player could have 
   made, the player with the needlessly short wff loses 1 point.

- Ending the game

9. Win conditions are flexible, so come up with your own rule or deem the 
   player who reaches 4 points first the winner.
9*.Other win conditions to consider: 1) The first player to utter n falsehoods 
   loses. 2) The first player to reach a chosen number of total wff length (in 
   characters) wins. 3) See how long of a 'truth-streak' you can keep up. 
   4) For quick play: the player with the longest true wff wins.

- Tie breaking

10.To break a tie, both players start a round as usual, but the objective of 
   this round is to be the first to construct a true wff.
11.Both players need wffs by the end of the round. If the first player to make 
   a wff makes a false wff, then the second player's wff is checked. If both 
   are false, the tie breaker round starts over.

Endnotes

1: Generative soundness of grammar system G := if a statement can be 
   constructed after some number n applications of rules in G, then the statement 
   is a wff. Generative completeness of G := if a statement is a wff, then the 
   statement can be constructed with n applications of rules in G.
