#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
output_file = open("data_to_injector.txt", 'w')

class Sender:
    def __init__(self):
        self.name = "packets"
    def send(self,pkt):
        import socket
        sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        sock.connect(self.name)
        sock.send(json.dumps(pkt))
        #print sock.recv(1024)
        sock.close()

import time,random
sender = Sender()
TIME_WAIT = 4

postCardQueue = []

def IssueProbe(pkt, rules,v1,v2):
    global postCardQueue
    sender.send(pkt)
    try:
        card = postCardQueue.get(True,TIME_WAIT)
    except Exception:
        return -1
    pid = card[0]
    rid = card[1]
    print "pid,rid",pid,rid,"v1,v2",v1,v2
    return int(rid)
    if random.randint(0,1) == 0:
        return v1
    else:
        return v2
    for rule in rules:
        return rule

def packetGenerator(edge_dict, rule_list, types, q):
    global postCardQueue
    postCardQueue = q
    
    V = rule_list.keys()
    E = []
    for v1 in edge_dict:
        for v2 in edge_dict[v1]:
            E.append([v2,v1])

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
            #time.sleep(0.1)
            subtraction = header.subtraction_wrapper(intersection, header_space)
            if subtraction == None:
                del S[index]
                break

            pkt = solver.createPacket(intersection,header_space,types)
            if pkt['SAT'] == 'No':
                del S[index]
                break

            print "packet: ",
            types_tmp = {"src-port":16,"dst-port":16,"src-ip":0,"dst-ip":0}
            for typ in types_tmp:
                if pkt.has_key(typ):
                    print typ,pkt[typ],
            print ""

            vhit = IssueProbe(pkt,rule_list,v1,v2)
            if vhit == -1:
                return False
            
            #solver.printpkt(pkt,types)
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
            if [v1,vhit] in S:
                S.remove([v1,vhit])
            if [v2,vhit] in S:
                S.remove([v2,vhit])
    print "VV:",VV
    print "EE:",EE
    VVV = [val for val in V if val not in VV]
    while len(VVV) > 0:
        v = VVV[0]
        T = rule_list[v]
        header_space = []
        for vv in VV:
            header_space.append(rule_list[vv])
        while len(T) > 0 and len(header_space) > 0:
            pkt = solver.createPacket(T,header_space,types)
            if pkt['SAT'] == 'No':
                if v in VVV:
                    VVV.remove(v)
                break
            vhit = IssueProbe(pkt, rule_list, vhit, vhit)
            if not vhit in VV:
                VV.append(vhit)
            if vhit in VVV:
                VVV.remove(vhit)
            if vhit == v:
                if vhit in VVV:
                    VVV.remove(vhit)
                break
            header_space.append(rule_list[vhit])
    print "After leafs' detection:"
    print "VV:",VV
    print "EE:",EE
    print "V:",V
    print "E:",E
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
    for edge in E:
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
    return ret
    import networkx as nx
    G = nx.DiGraph()
    for v in V:
        G.add_node(v)
    for edge in E:
        G.add_edge(edge[1],edge[0])
    GG = nx.DiGraph()
    for v in VV:
        GG.add_node(v)
    for edge in EE:
        GG.add_edge(edge[1],edge[0])
    ret = nx.is_isomorphic(G, GG)

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
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    #print rule_list
    #print edge_dict

    packetGenerator(edge_dict, rule_list, types)



