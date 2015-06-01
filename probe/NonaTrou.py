#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
from timelog import TimeLog
output_file = open("data_to_injector.txt", 'w')

def pktGenerator(pos, rule_list, rule_dict, types,intersect,log):
    if intersect == None:
        return []

    intersect = copy.deepcopy(intersect)
    log = copy.deepcopy(log)
    ret = []

    if pos >= len(rule_list) :
        #print "log = ",log
        #print "intersect",intersect
        if len(log) <= 0:
            return ret
        header_space = []
        for v in [v for v in rule_list if v not in log]:
            header_space.append(rule_dict[v])
        TimeLog.GetInstance().addTotal()
        pkt = solver.createPacket(intersect,header_space,types)
        TimeLog.GetInstance().addSolver()
        if pkt['SAT'] == 'Yes':
            ret.append((log,pkt))
        return ret
    #for i in range(pos,len(rule_list)):
    i = pos
    cur = pktGenerator(i+1, rule_list, rule_dict, types, intersect, log)
    ret += cur

    intersect = header.intersect_molecule(intersect,rule_dict[rule_list[i]])
    #print intersect
    if intersect != None:
        log.append(rule_list[i])
        cur = pktGenerator(i+1, rule_list, rule_dict, types, intersect, log)
        ret += cur
    return ret
def packetGenerator(edge_dict, rule_dict, types):
    rule_list = rule_dict.keys()

    header_space = []
    for feature in types:
        header_space.append(-1)
    header_space = [[header_space]]
    log = []
    pkts = pktGenerator(0,rule_list,rule_dict,types,header_space,log)
    #print pkts
    return pkts

def dagCompare(edge_dict, rule_list, VV, EE):

    TimeLog.GetInstance().addTotal()
    
    V = rule_list.keys()
    E = []
    for v1 in edge_dict:
        for v2 in edge_dict[v1]:
            E.append([v2,v1])

    #print V
    #print E

    #print VV
    #print EE

    if len(VV) != len(V):
        return False
    if len([val for val in V if val not in VV]) > 0:
        return False

    #equality for two graph.
    h = {}
    for i,k in enumerate(V):
        h[k] = i
    G1 = [[0]*len(V) for i in range(len(V))]
    for edge in E:
        v1 = h[edge[0]]
        v2 = h[edge[1]]
        G1[v1][v2] = 1
    for i in range(len(V)):
        for j in range(len(V)):
            for k in range(len(V)):
                if G1[i][k] == 1 and G1[k][j] == 1:
                    G1[i][j] = 1
    G2 = [[0]*len(V) for i in range(len(V))]
    for edge in EE:
        #print h
        #print edge
        v1 = h[edge[0]]
        v2 = h[edge[1]]
        G2[v1][v2] = 1
    for i in range(len(V)):
        for j in range(len(V)):
            for k in range(len(V)):
                if G2[i][k] == 1 and G2[k][j] == 1:
                    G2[i][j] = 1
    ret = True
    for i in range(len(V)):
        if ret == False:
            break
        for j in range(len(V)):
            if G1[i][j] != G2[i][j]:
                ret = False
                break
    TimeLog.GetInstance().clock()
    return ret


def postProcessor(rule_list, rule_dict, pid2rids):
    pass


def sendToPostcardProcessor(rid,sid, num = 1000):
    pass

def sendToInjector(packet, switch_id = 1, num = 1000):
    pass#output_file.write(str(packet))
#output_file.write('\n')

import sys
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: python algo.py dag_file"
        exit(0)
    dag_file = sys.argv[1]
    print dag_file
    types = parser.type_parse("typename.txt")
    rule_dict,edge_dict = parser.DAGLoader(dag_file);
    #print rule_list
    #print edge_dict
    rule_list = rule_dict.keys()

    header_space = []
    for feature in types:
        header_space.append(-1)
    header_space = [[header_space]]
    log = []
    pkts = pktGenerator(0,rule_list,rule_dict,types,header_space,log)
    print pkts


