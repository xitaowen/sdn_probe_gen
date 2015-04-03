#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
output_file = open("data_to_injector.txt", 'w')

import time,random
def IssueProbe(pkt, rules,v1,v2):
    print pkt
    if random.randint(0,1) == 0:
        return v1
    else:
        return v2
    for rule in rules:
        return rule
def packetGenerator(edge_dict, rule_list, types):
    S = []
    VV = []
    EE = []
    for v1 in edge_dict:
        vset = edge_dict[v1]
        for v2 in vset:
            S.append([v1,v2])
    while len(S) > 0:
        pset = []
        #print len(S),index
        print VV,EE
        for s in S:
            v1 = s[0]
            v2 = s[1]
            header_space = []
            for edge in EE:
                if edge[0] == v1 or edge[0] == v2:
                    header_space.append(rule_list[edge[1]])
            intersection = header.intersect_molecule(rule_list[v1],rule_list[v2])

            T = [intersection,header_space]
            subtraction = header.subtraction_wrapper(intersection, header_space)
            if subtraction == None:
                continue
            pkt = solver.createPacket(intersection,header_space,types)
            pset.append([v1,v2,pkt])

        #IssueProbeSet
        for p in pset:
            v1 = p[0]
            v2 = p[1]
            pkt = p[2]

            vhit = IssueProbe(pkt,rule_list,v1,v2)
            if not vhit in VV:
                VV.append(vhit)
            if vhit == v1 or vhit == v2:
                EE.append([v1,v2])
                S.remove([v1,v2])
                break
            EE.append([v2,vhit])

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



