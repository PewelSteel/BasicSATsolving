import sys
from idlelib.rpc import RPCHandler, SocketIO
from operator import index
from itertools import combinations
import copy
import csv
import time
import tracemalloc

empty = []

def resolve(clause1, clause2):
    for literal in clause1:
        if -1*literal in clause2:
            new_clause = clause1.copy()
            for literal1 in clause2:
                if literal1 not in new_clause:
                    new_clause.append(literal1)
            new_clause.remove(literal)
            new_clause.remove(-1*literal)
            return new_clause
    return None

def resolution(clause_set):
    for clause1, clause2 in combinations(clause_set, 2):
        resolvent = resolve(clause1, clause2)
        if resolvent is not None and resolvent not in clause_set:
            clause_set.append(resolvent)
            print(f"New clause: {resolvent} (from {clause1} and {clause2})")
            break

def resolutionONLY(clause_set):
    resolvent = [1]
    while resolvent != None and resolvent != []:
        for clause1,clause2 in combinations(clause_set, 2):
            resolvent = resolve(clause1, clause2)
            if resolvent is not None and resolvent not in clause_set:
                clause_set.append(resolvent)
                print(f"New clause: {resolvent} (from {clause1} and {clause2})")
                if resolvent == []:
                    print("Generated empty clause => UNSATISFIABLE")
                    return
                break
    print("Full set of clauses => SATISFIABLE")

def onelitverif(clause_set):
    for clause in clause_set:
        if len(clause) == 1:
            return 1
    return 0

def purelitverif(clause_set):
    literals = []
    for clause in clause_set:
        for literal in clause:
            if literal not in literals:
                literals.append(literal)
    for literal in literals:
        if literal in literals and -1*literal not in literals:
            return 1
    return 0

def onelit(clause_set):
    for index,clause in enumerate(clause_set):
        if len(clause) == 1:
            print(f"Apply 1-literal rule on {clause}")
            literal = clause[0]
            break
    cl = -1*literal
    i = 0
    while i < len(clause_set):
        clause = clause_set[i]
        if literal in clause:
            print(f"Removed {clause} because of {literal}")
            clause_set.pop(i)
            i -= 1
        elif cl in clause:
            print(f"Removed {cl} from {clause}")
            clause.remove(cl)
        i = i + 1
    print("New set of clauses:")
    for clause in clause_set:
        print(clause)
    return clause_set

def purelit(clause_set):
    literals = []
    for clause in clause_set:
        for literal in clause:
            if literal not in literals:
                literals.append(literal)
    for literal in literals:
        if literal in literals and -1*literal not in literals:
            sliteral = literal
            break
    print(f"Apply pure-literal rule on {sliteral}")
    i=0
    while i < len(clause_set):
        if sliteral in clause_set[i]:
            print(f"Removed {clause_set[i]}")
            clause_set.pop(i)
            i -= 1
        i = i + 1
    print("New set of clauses:")
    for clause in clause_set:
        print(clause)
    return clause_set

def DP(clause_set):
    while empty not in clause_set and clause_set != empty:
        while onelitverif(clause_set):
            onelit(clause_set)
        while purelitverif(clause_set):
            purelit(clause_set)
        resolution(clause_set)
    if empty in clause_set:
        print("UNSATISFIABLE")
    else:
        print("SATISIFIABLE")

def DPLL(clause_set,splitcount):
    splitcount = splitcount+1
    while empty not in clause_set and clause_set != empty:
        while onelitverif(clause_set):
            onelit(clause_set)
        while purelitverif(clause_set):
            purelit(clause_set)
        if empty in clause_set:
            print("Generated empty clause => UNSATISFIABLE")
            return 0
        elif clause_set == empty:
            print("Full set of clauses => SATISIFIABLE")
            return 1
        while True:
            print(clause_set)
            firstlit = clause_set[0][0]
            print(f"Split number {splitcount} on {firstlit}")
            DPLL1 = copy.deepcopy(clause_set)
            DPLL2 = clause_set.copy()
            fl = []
            ofl = []
            fl.append(firstlit)
            ofl.append(-1*firstlit)
            DPLL1.append(fl)
            DPLL2.append(ofl)
            print(f"I.{splitcount} {DPLL1}")
            if DPLL(DPLL1,splitcount) == 1:
                print("One of the branches is satisfiable => SATISFIABLE")
                return 1
            print(f"II {DPLL2}")
            if DPLL(DPLL2,splitcount) == 1:
                print("One of the branches is satisfiable => SATISFIABLE")
                return 1
            splitcount = splitcount - 1
            print("UNSATISIFABLE")
            return 0


clauseset = []
splitcount = 0
max_size = 0

with open("clauses.csv" , "r", encoding="UTF-8") as file:
    for line in file:
        clause = line.strip().split()
        elements = []
        for element in clause:
            element = int(element)
            if element != 0:
                elements.append(element)
        clauseset.append(elements)
print("Set of clauses:")
for clause in clauseset:
    print(clause)

print("Choose a method of solving (1, 2 or 3):");
print("1.Resolution")
print("2.DP")
print("3.DPLL")
method = 3
if method == 1:
    tracemalloc.start()
    start = time.time()
    resolutionONLY(clauseset)
    current, peak = tracemalloc.get_traced_memory()
    end = time.time()
elif method == 2:
    tracemalloc.start()
    start = time.time()
    DP(clauseset)
    current, peak = tracemalloc.get_traced_memory()
    end = time.time()
elif method == 3:
    tracemalloc.start()
    start = time.time()
    DPLL(clauseset,splitcount)
    current, peak = tracemalloc.get_traced_memory()
    end = time.time()
else:
    print("Wrong input!")
    exit()
print(f"Execution time: {end - start}")
print(f"Peak memory usage: {peak / 1024:.2f} KB")
