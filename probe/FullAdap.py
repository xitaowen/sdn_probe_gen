#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
output_file = open("data_to_injector.txt", 'w')

import time,random
def IssueProbe(pkt, rules,v1,v2):
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
    #for v1 in edge_dict:
    #    vset = edge_dict[v1]
    #    for v2 in vset:
    #        S.append([v1,v2])
    rules = rule_list.keys()
    print len(rules)
    for r1 in range(0,len(rules)):
        for r2 in range(r1+1,len(rules)):
            intersection = header.intersect_molecule(rule_list[rules[r1]],rule_list[rules[r2]])
            if intersection != None:
                S.append([rules[r1],rules[r2]])
    while len(S) > 0:
        time.sleep(0.1)
        index = random.randint(0,len(S)-1)
        v1 = S[index][0]
        v2 = S[index][1]
        print len(S),index,v1,v2
        print "S=",S
        print VV,EE
        header_space = []
        for edge in EE:
            if edge[0] == v1 or edge[0] == v2:
                header_space.append(rule_list[edge[1]])
        intersection = header.intersect_molecule(rule_list[v1],rule_list[v2])
        T = (intersection,header_space)
        while True:
            time.sleep(0.1)
            subtraction = header.subtraction_wrapper(intersection, header_space)
            if subtraction == None:
                del S[index]
                break

            pkt = solver.createPacket(intersection,header_space,types)

            vhit = IssueProbe(pkt,rule_list,v1,v2)
            print "packet: ",
            solver.printpkt(pkt,types)
            if not vhit in VV:
                VV.append(vhit)
            if vhit == v1:
                EE.append([v2,v1])
                del S[index]
                break
            if vhit == v2:
                EE.append([v1,v2])
                del S[index]
                break
            EE.append([v2,vhit])
            EE.append([v1,vhit])
            header_space.append(rule_list[vhit])
            S.remove(v1,vhit)
            S.remove(v2.vhit)
    return VV,EE

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



