"""Lexical Analyzer + Recognizer"""
"""Zachary Inserra"""
"""CSC - 434"""

import logging
logging.basicConfig(filename = "output.log", level = logging.DEBUG)

letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
operator = ["*", "/", "+", "-"]
assignment = "="
space = " "
rules = []
chList = []
token = ""
workingString = ""

"""
GRAMMER RULES:
statement -> assign_stmt | expression
assign_stmt -> identifier assignment expression
expression -> (identifier | number) operator expression | (identifier | number)

put into dictionary?
compare RHS of working string removing first LHS until match is found
"""

"""terminal in list term corresponds to its nonterminal in list nonTerm, both have same index"""
term = ["identifier operator expression", "number operator expression", "identifier ", "number ", "identifier assignment expression", "assign_stmt", "expression"]
nonTerm = ["expression", "expression", "expression", "expression", "assign_stmt", "statement", "statement"]

""" Takes in line of code
    Iterates through line
    As it iterates through a string it goes through various state changes
    adding tokens to a string that will the be output"""

class tokenize(object):
    def __init__(self, inp, state = 0):
        self.inp = inp
        self.workingString = ""
        self.token = ""
        self.nwsList = []

        for i in inp:
            stateCheck = state
            state = self.classify(i, state)
            """ If state is the same as previous state, the token 
                will not be added until the state changes and is not a space"""
            if state != stateCheck and state != 0:
                self.workingString += self.token
            if state == 0:
                colState = self.classify(i, state)
                state = rules[state][colState]
            elif state == 1:
                colState = self.classify(i, state)
                state = rules[state][colState]
            elif state == 2:
                colState = self.classify(i, state)
                state = rules[state][colState]
            elif state == 3:
                colState = self.classify(i, state)
                state = rules[state][colState]
            elif state == 4:
                colState = self.classify(i, state)
                state = rules[state][colState]
            elif state == 5:
                colState = self.classify(i, state)
                state = rules[state][colState]
                break

        print(inp+ " tokenizes as " +self.workingString)
        logging.info(inp+ " tokenizes as " +self.workingString)

        """call recognize function on workingString to evaluate validity"""
        self.recognize(self.workingString)

    """ Takes a character and the current state of the FSM, 
        returns a number corresponding to a column in the rule list,
        and sets the token name"""
    def classify(self, input, state):
        if input in letter:
            self.token = "identifier "
            return 1
        elif input in number:
            if state == 1:
                self.token = "identifier "
                return 1
            else:
                self.token = "number "
                return 2
        elif input in operator:
            if state == 3:
                self.token = "error "
                return 6
            else:
                self.token = "operator "
                return 3
        elif input in assignment:
            self.token = "assignment "
            return 4
        elif input in space:
            return 0
        else:
            self.token = "error "
            return 5

    """check if working string is in list of terminals
        if not drop LHS and check until success
            replace with corresponding nonterminal(same list index)
        if, replace..."""
    def recognize(self, ws):
        # BASE CASE
        # If the string translates to 'statement'
        # it prints as 'Valid'
        if ws == "statement":
            print("         " +self.inp+ " is a Valid Statement")
            logging.info("         " +self.inp+ " is a Valid Statement")
        # If there is an error in the original string, nothing will be printed
        elif "error " in ws:
            None
        else:
            # If the string is in a list of terminals
            # it is replaced with a corresponding nonterminal
            # Then it is rejoined with the LHS words that were dropped
            # and goes through the recognize function again
            if ws in term:
                nt = nonTerm[term.index(ws)]
                self.nwsList.append(nt)
                nws = " ".join(self.nwsList)
                self.nwsList = []
                self.recognize(nws)
            # If the string can not be found in the list of terminals
            # then the LHS is dropped and recognize is called again
            # on the RHS
            # If the RHS never translates to a nonterminal,
            # 'Invalid' is printed
            else:
                wsList = ws.split(" ")
                for i in range(len(wsList)):
                    self.nwsList.append(wsList.pop(0))
                    nws = " ".join(wsList)
                    if nws in term:
                        nt = nonTerm[term.index(nws)]
                        self.nwsList.append(nt)
                        nws = " ".join(self.nwsList)
                        self.nwsList = []
                        self.recognize(nws)
                print("         " +self.inp+ " is an Invalid Statement")
                logging.info("         " +self.inp+ " is an Invalid Statement")
                

""" Reads rule file and creates a list of rules for the FSM to follow """
with open('LexTable.txt', 'r') as table:
    for line in table:
        rule = [int(num) for num in line.split()]
        rules.append(rule)

""" Reads test file and passes each line to the tokenizer """
test = open("Test.txt", "r")
for i in test:
    i = i.rstrip("\n")
    tokenize(i)
test.close()
