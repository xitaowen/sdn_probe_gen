#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
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
        ret.append((log,solver.createPacket(intersect,[],types)))
        return ret
    #for i in range(pos,len(rule_list)):
    i = pos
    cur = pktGenerator(i+1, rule_list, rule_dict, types, intersect, log)
    ret += cur

    intersect = header.intersect_molecule(intersect,rule_dict[rule_list[i]])
    #print intersect
    if intersect != None:
        log.append(i)
        cur = pktGenerator(i+1, rule_list, rule_dict, types, intersect, log)
        ret += cur
    return ret


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



