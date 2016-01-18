#!/usr/bin/python
import json
import re
import copy
import time

import header
import solver,parser
from timelog import TimeLog
output_file = open("data_to_injector.txt", 'w')

# if rule id goes from 0 to N, and rules are sorted according to their id, works
def packetGenerator(edge_dict, rule_list, types):
    # containg all pkt, rule paris
    pairs = []
    dag = {}
    for rule in rule_list:
        dag[rule] = []
    for rule1 in edge_dict:
        if not dag.has_key(rule1):
            dag[rule1] = []
        for rule2 in edge_dict[rule1]:
            if not dag.has_key(rule2):
                dag[rule2] = []
            dag[rule2].append(rule1)

    dep = copy.deepcopy(dag)
    #print dag

    header_space = []
    T = {}
    for rule1 in rule_list.keys():
        T[rule1] = []
    # variable rule1 and rule 2 are int.
    while True:
        rule1 = -1
        for rule in dag:
            if len(dag[rule]) == 0:
                rule1 = rule
                break
        if rule1 == -1:
            break
        for rule in dep[rule1]:
            if len(T[rule]) > 0:
                T[rule1] += T[rule]

        T[rule1].sort()
        T[rule1] = [x for i, x in enumerate(T[rule1]) if not i or T[rule1][i] != T[rule1][i-1]]

        if edge_dict.has_key(rule1):
            #print "rule has other rule to depend on"
            adj_list = edge_dict[rule1]

            for rule2 in adj_list:
                #intersection = header.intersect_molecule((rule_list[rule1], rule_list[rule2]))
                intersection = header.intersect_molecule(rule_list[rule1], rule_list[rule2])
                #print rule1,rule_list[rule1]
                #print rule2,rule_list[rule2]
                #print intersection
                if intersection == None:
                    #print rule1,rule_list[rule1]
                    #print rule2,rule_list[rule2]
                    continue
                #print rule1,rule2
                TimeLog.GetInstance().addCalc()
                packet = solver.createPacket(intersection,T[rule1],types)
                TimeLog.GetInstance().addSolver()
                #print packet
                if packet['SAT'] == 'No':
                    print "1. Dependency Error"
                    print rule2
                    return False
                # include the packet and its rule pair
                T[rule2].append(intersection)
                #T[rule2].append(rule_list[rule1])

                tu = (rule1, packet)
                if tu not in pairs:
                    pairs.append(tu)

        elif len(dep[rule1]) > 0:
            #print "rule has no ther rule depend on"
            TimeLog.GetInstance().addCalc()
            packet = solver.createPacket(rule_list[rule1],T[rule1],types)
            TimeLog.GetInstance().addSolver()
            if packet['SAT'] == 'No':
                print "2. (leaf) Dependency Error"
                #print rule1
                return False

            tu = (rule1, packet)
            if tu not in pairs:
                pairs.append(tu)

        elif len(dep[rule1]) == 0:
            #print "rule has no ther rule depend on"
            TimeLog.GetInstance().addCalc()
            packet = solver.createPacket(rule_list[rule1],T[rule1],types)
            TimeLog.GetInstance().addSolver()
            if packet['SAT'] == 'No':
                print "3. (dependent) Dependency Error"
                #print rule1
                return False

            tu = (rule1, packet)
            if tu not in pairs:
                pairs.append(tu)

        #remove visited rules in dag
        del dag[rule1]
        for rule in dag:
            if rule1 in dag[rule]:
                dag[rule].remove(rule1)
    #print pairs
    TimeLog.GetInstance().addCalc()
    return pairs


import sys
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: python algo.py dag_file"
        exit(0)
    dag_file = sys.argv[1]
    print dag_file
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    #print rule_list
    #print edge_dict

    pairs = packetGenerator(edge_dict, rule_list, types)
    for pair in pairs:
        #print pair
        rid = pair[0]
        pkt = pair[1]
        print rid
        for typ in ['src-ip','dst-ip','src-port','dst-port']:
            print typ,pkt[typ]



