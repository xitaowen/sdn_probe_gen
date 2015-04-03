#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
output_file = open("data_to_injector.txt", 'w')

# if rule id goes from 0 to N, and rules are sorted according to their id, works
def packetGenerator(edge_dict, rule_list, types):
    # containg all pkt, rule paris
    pairs = []
    dag = {}
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
    for rule1 in edge_dict:
        T[rule1] = []
        for rule2 in edge_dict[rule1]:
            T[rule2] = []
    # variable rule1 and rule 2 are int.
    while True:
        rule1 = -1
        for rule in dag:
            if len(dag[rule]) == 0:
                rule1 = rule
                break;
        if rule1 == -1:
            break
        for rule in dep[rule1]:
            T[rule1] += T[rule]

        T[rule1].sort()
        T[rule1] = [x for i, x in enumerate(T[rule1]) if not i or T[rule1][i] != T[rule1][i-1]]

        if edge_dict.has_key(rule1):
            #print "rule has other rule to depend on"
            adj_list = edge_dict[rule1]

            for rule2 in adj_list:
                intersection = header.intersect_molecule(rule_list[rule1], rule_list[rule2])
                packet = solver.createPacket(intersection,T[rule1],types)
                sendToInjector(packet)
                # include the packet and its rule pair
                T[rule2].append(intersection)

                tu = (rule2, packet)
                if tu not in pairs:
                    pairs.append(tu)


        elif len(dep[rule1]) >= 0:
            #print "rule has no ther rule depend on"
            packet = solver.createPacket(rule_list[rule1],T[rule1],types)
            sendToInjector(packet)

            tu = (rule1, packet)
            if tu not in pairs:
                pairs.append(tu)

        #remove visited rules in dag
        del dag[rule1]
        for rule in dag:
            if rule1 in dag[rule]:
                dag[rule].remove(rule1)

    #print pairs


def sendToPostcardProcessor(rid,sid, num = 1000):
    pass

def sendToInjector(packet, switch_id = 1, num = 1000):
    output_file.write(str(packet))
    output_file.write('\n')

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

    packetGenerator(edge_dict, rule_list, types)



