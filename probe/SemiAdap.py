#!/usr/bin/python
import json
import re
import copy

import header,solver,parser
from timelog import TimeLog
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
TIME_WAIT = 1

postCardQueue = []
Pid = 0
def IssueProbe(pkt, rules,v1,v2):
    global postCardQueue
    global Pid
    while not postCardQueue.empty():
        postCardQueue.get()
    #pkt['pid'] = Pid
    #Pid += 1
    sender.send(pkt)
    TimeLog.GetInstance().addPacket()
    try:
        card = postCardQueue.get(True,TIME_WAIT)
    except Exception:
        TimeLog.GetInstance().clock()
        return -1
    pid = card[0]
    rid = card[1]
    #print "Pid,pid,rid",pkt['pid'],pid,rid,"v1,v2",v1,v2
    return int(rid)
    if random.randint(0,1) == 0:
        return v1
    else:
        return v2
    for rule in rules:
        return rule
def IssueProbeSet(pkts):
    #print "#",len(pkts)
    global postCardQueue
    while not postCardQueue.empty():
        postCardQueue.get()
    hits = {}
    for pkt in pkts:
        sender.send(pkts[pkt])
        hits[pkt] = -1
    TimeLog.GetInstance().addPackets(len(pkts))
    if len(pkts) == 0:
        return hits
    while True:
        try:
            TimeLog.GetInstance().addSend()
            card = postCardQueue.get(True,TIME_WAIT)
        except Exception:
            TimeLog.GetInstance().clock()
            #pid = card[0]
            #rid = card[1]
            #hits[pid] = rid
            return hits
        pid = card[0]
        rid = card[1]
        hits[pid] = rid
    #print "pid,rid",pid,rid,"v1,v2",v1,v2

def packetGenerator(edge_dict, rule_list, types, q):
    global postCardQueue
    postCardQueue = q
    global Pid
    Pid = 0

    TimeLog.GetInstance().addTotal()

    V = rule_list.keys()
    E = []
    for v1 in edge_dict:
        for v2 in edge_dict[v1]:
            E.append([v2,v1])

    S = []
    VV = []
    EE = []
    rules = rule_list.keys()
    for r1 in range(0,len(rules)):
        for r2 in range(r1+1,len(rules)):
            intersection = header.intersect_molecule(rule_list[rules[r1]],rule_list[rules[r2]])
            if intersection != None:
                S.append([rules[r1],rules[r2]])
    while len(S) > 0:
        #print "#",len(S),S
        pset = {}
        pindex = {}
        #print len(S)
        #print VV,EE
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
                S.remove(s)
                continue
            TimeLog.GetInstance().addTotal()
            pkt = solver.createPacket(intersection,header_space,types)
            TimeLog.GetInstance().addSolver()
            if pkt['SAT'] == 'No':
                S.remove(s)
                break
            pindex[Pid] = [v1,v2]
            pset[Pid] = pkt
            pkt['pid'] = Pid
            Pid += 1

        #print len(pset)
        #IssueProbeSet
        TimeLog.GetInstance().addTotal()
        pHits = IssueProbeSet(pset)
        TimeLog.GetInstance().addSend()

        for p in pHits:
            vhit = pHits[p]
            v1 = pindex[p][0]
            v2 = pindex[p][1]
        #for p in pset:
            #print len(pset)
            #pkt = pset[p]
            #v1 = pindex[p][0]
            #v2 = pindex[p][1]
            #TimeLog.GetInstance().addTotal()
            #vhit = IssueProbe(pkt,rule_list,v1,v2)
            #TimeLog.GetInstance().addSend()

            if vhit >= 0 and not vhit in VV:
                VV.append(vhit)
            if vhit == v1:
                EE.append([v2,v1])
                if [v1,v2] in S:
                    S.remove([v1,v2])
                continue
            if vhit == v2:
                EE.append([v1,v2])
                if [v1,v2] in S:
                    S.remove([v1,v2])
                continue
            if vhit >= 0:
                EE.append([v2,vhit])
                EE.append([v1,vhit])
                if [v1,vhit] in S:
                    S.remove([v1,vhit])
                if [v2,vhit] in S:
                    S.remove([v2,vhit])
            if vhit == -1:
                if [v1,v2] in S:
                    S.remove([v1,v2])
    #print "VV:",VV
    #print "EE:",EE
    #print "stage 2:"
    VVV = [val for val in V if val not in VV]
    while len(VVV) > 0:
        #print "#",len(VVV)
        index = random.randint(0,len(VVV)-1)
        v = VVV[index]
        T = rule_list[v]
        TT = []
        header_space = []
        #for vv in VV:
            #intersection = header.intersect_molecule(rule_list[vv],rule_list[vv])
            #if intersection != None:
                #header_space.append(intersection)
                #TT.append(vv)
        while True:
            #len(T) > 0 and len(header_space) > 0:
            TimeLog.GetInstance().addCalc()
            #print "solver: ",len(header_space)
            pkt = solver.createPacket(T,header_space,types)
            TimeLog.GetInstance().addSolver()
            if pkt['SAT'] == 'No':
                break
            TimeLog.GetInstance().addCalc()
            Pid += 1
            pkt['pid'] = Pid
            vhit = IssueProbe(pkt, rule_list, v, v)
            TimeLog.GetInstance().addSend()
            if vhit == -1:
                break
            if (not vhit in VV) and (vhit in V):
                VV.append(vhit)
            if vhit in VVV:
                VVV.remove(vhit)
            if vhit == v:
                break
            if vhit in TT:
                break
            TT.append(vhit)
            header_space.append(rule_list[vhit])
        if v in VVV:
            VVV.remove(v)
    #print "After leafs' detection:"
    #print "Original Graph"
    #print "V:",V
    #print "E:",E
    #print "Actual Graph"
    #print "VV:",VV
    #print "EE:",EE
    TimeLog.GetInstance().addCalc()
    #for i in [val for val in V if val not in VV]:
    #    print "missing:",i
    if len(VV) != len(V):
        return False
    if len([val for val in V if val not in VV]) > 0:
        return False
    #ret = True
    #TimeLog.GetInstance().clock()
    #return ret

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
    #print "Original DAG:",G1
    #print "Actual DAG:",G2
    TimeLog.GetInstance().clock()
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



