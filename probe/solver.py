#!/usr/bin/python
import json
import re
import copy

import miniSAT

len_type = {"src-port":16,"dst-port":16,"src-ip":0,"dst-ip":0}
def rule2cnf(rule, op, types):
    cur = 0
    ret = ""
    len_cnf = 0
    cnf = ""
    for ty in range(0,len(types)):
        typ = types[ty]
        #print typ
        if len_type.has_key(typ):
            ln = len_type[typ]
        else:
            ln = 1
        if rule[ty] == -1:
            cur += ln
            continue
        dt = rule[ty]
        for i in range(0,ln):
            if (dt&(1<<(ln-i-1))) > 0:
                if op > 0:
                    cnf += " "+str(cur+i+1)+" 0"
                    len_cnf += 1
                else:
                    ret += " "+"-"+str(cur+i+1)
            else:
                if op < 0:
                    ret += " "+str(cur+i+1)
                else:
                    cnf += " "+"-"+str(cur+i+1)+" 0"
                    len_cnf += 1
        cur += ln
    #print cur
    if op > 0:
        return len_cnf,cnf
    if len(ret) > 0:
        return 1," "+ret+" 0"
    return 0,ret

def ans2packet(ans, types):
    cur = 0
    ret = {'SAT':'Yes'}
    for ty in range(0,len(types)):
        typ = types[ty]
        if len_type.has_key(typ):
            ln = len_type[typ]
        else:
            ln = 1
        ret[typ] = 0
        for i in range(0,ln):
            ret[typ] <<= 1
            #print cur+ln-i
            if cur+ln-i>= len(ans)-1:
                ret[typ] += 0
                continue
            f = int(ans[cur+i+1])
            if f < 0:
                ret[typ] += 0
            else:
                ret[typ] += 1
        cur += ln
    return ret

def printip(ip):
    ret = ""
    for i in range(0,4):
        ret += str((ip>>(24-i*8))&0xFF)
        if i < 3:
            ret += "."
    return ret

def printpkt(pkt, types):
    #pkt = ans2packet(ans, types)
    for i in range(0,32):
        pkt["src-ip"] <<= 1
        pkt["src-ip"] += pkt["ipSrc"+str(i)]
        pkt["dst-ip"] <<= 1
        pkt["dst-ip"] += pkt["ipDst"+str(i)]
    for typ in len_type:
        if typ == "src-ip" or typ == "dst-ip":
            print typ,printip(pkt[typ])," ",
        else:
            print typ,pkt[typ]," ",
    print ""

def createPacket(subtraction, header_space, types):
    if subtraction == None:
        return {'SAT':'No'}
    #transform substraction and header_space to cnf format.
    #First, substraction - header_space
    #Second, Substraction is which packet must match. So every certain bit(0 or 1) should be
    #remains the same. In SAT, each certain bit is new line(for example, 1110** -> x0=1^x1=1^x2=1^x3=0 ).

    #count lines.
    cnf_head = 0
    cnf = ""
    rule = subtraction[0][0]
    # 1 mean this is a positive line.
    tmp_len,tmp = rule2cnf(rule,1,types)
    if tmp_len > 0:
        cnf_head += tmp_len
    cnf += tmp
    #Third, there is an - b4 header_space, so header_space = (r1,r2,r3) => -(r1,r2,r3) = -r1^-r2^-r3.
    #For example rule r1 = 10*, r1 = x0=1^x1=0, so -r1 = (x0=0,x1=1)
    for header in header_space:
        rule = header[0][0]
        # -1 mean this is a negtive line.
        tmp_len,tmp = rule2cnf(rule,-1,types)
        if tmp_len > 0:
            cnf_head += tmp_len
        cnf += tmp
    cnf_head = "p cnf 200 "+str(cnf_head)
    cnf = cnf_head+cnf
    #print len(cnf)
    #
    #solve the sat
    ans = miniSAT.solve(cnf)
    #print "inter:",subtraction
    #print "header_space",header_space
    #print "ans:",ans
    #
    #process the result.
    #if solved, return "SAT 1 2 -3 ..."
    #if unsolvable, return "UNSAT"
    ans = ans.split(' ')
    #printpkt(ans,types)
    if ans[0] == 'SAT':
        return ans2packet(ans,types)
    packet = {'SAT':'No'}
    return packet

