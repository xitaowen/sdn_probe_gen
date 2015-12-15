#!/usr/bin/python
import sys
import os
import re
import copy
import sys
sys.path.append("..")
from probe import header

def type_parse(filename):
    fileHandle = open(filename)
    types = []
    lines = fileHandle.readlines()
    for line in lines:
        reg = re.compile(r'"(.+?)"')
        types.append(reg.findall(line)[0])
    fileHandle.close()
    return types

#convert to 0,1,-1
def rule_parse(a):
    rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
    patterns = rule_pattern.findall(a)

    rules = {}
    types = ["tcpSrcPort","tcpDstPort","ipSrc","ipDst"]
    for typ in types:
        #process port
        pattern = typ +'=([0-9]+)'
        reg = re.compile(pattern)
        value = reg.findall(patterns[0])
        if not (len(value)==0):
            #print typ
            rules[typ] = value[0]
        #process ip
        pattern1 = typ +'=((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))(\/{1})(([1-3]\d)|[0-9]))'
        reg1 = re.compile(pattern1)
        value1 = reg1.findall(patterns[0])
        if not (len(value1)==0):
            rules[typ] = value1[0][0]

    #for typ in types:
    #    if (not rules.has_key(typ)):
    #        continue
    #    print typ,":",rules[typ],
    #print ""
    rule = {}
    for typ in types:
        if (not rules.has_key(typ)) or (rule.has_key(typ)):
            continue
        if typ == "tcpSrcPort":
            rule[typ] = rules[typ]
        if typ == "tcpDstPort":
            rule[typ] = rules[typ]
        if typ == "ipSrc":
            dt = rules[typ]
            dt = dt.split('/')
            if len(dt) == 1:
                ln = 32
            else:
                ln = int(dt[1])
            dt = dt[0]
            dt = dt.split('.')
            ip = 0
            for i in dt:
                ip <<=  8
                ip += int(i)
            for i in range(0,ln):
                if (ip&(1<<(31-i))) != 0:
                    rule["ipSrc"+str(i)] = 1
                else:
                    rule["ipSrc"+str(i)] = 0
            rule[typ] = -1

        elif typ == "ipDst":
            dt = rules[typ]
            dt = dt.split('/')
            if len(dt) == 1:
                ln = 32
            else:
                ln = int(dt[1])
            dt = dt[0].split('.')
            ip = 0
            for i in dt:
                ip <<=  8
                ip += int(i)
            for i in range(0,ln):
                if (ip&(1<<(31-i))) != 0:
                    rule["ipDst"+str(i)] = 1
                else:
                    rule["ipDst"+str(i)] = 0
            rule[typ] = -1

    types1 = type_parse("typename.txt")
    rl = []
    for typ in types1:
        if rule.has_key(typ):
            rl.append(rule[typ])
        else:
            rl.append(-1)
    return [[rl]]

#if a include b ,return True
def if_include(a,b):
    rule1 = rule_parse(a)
    rule2 = rule_parse(b)
    #print "rule1:",rule1
    #print "rule2:",rule2
    #for i in range(0,len(rule1)):
    #    if (rule1[i] != rule2[i] and rule1[i] != -1):
    #        return False
    #return True
    #if header.intersect_molecule(rule1,rule2) != None:
    #    if header.subtract_molecule(rule2,rule1) == None:
    if header.intersect_molecule(rule1,rule2) == rule2:
            #print "inter",header.intersect_molecule(a,b)
            #print "sub",header.subtract_molecule(b,a)
        return True
    return False
    

if __name__ == "__main__":
    #a = "{pattern={tcpSrcPort=750 ,tcpDstPort=123 ,ipSrc=149.22.32.112/29,ipDst=198.201.17.168/29,action=OutputPort()}"
    #b = "{pattern={tcpSrcPort=750 ,tcpDstPort=123 ,ipSrc=149.22.32.112/29,ipDst=198.201.17.168/29,action=OutputPort()}"
    #print if_include(a,b)
    if len(sys.argv) != 3:
        print "Usage:"
        sys.exit(1)

    ep = open(sys.argv[1],"r")
    epn = open(sys.argv[2],"w")
    content = ep.readlines()
    n = len(content)
    content[0] = content[0][1:]
    epn.write("[")
    for i in range(0,n-1):
        cnt = i
        #if i >= 4:
        #    print "i = ",i
        #    for j in range(i,n-1):
        #        print j,content[j]
        for j in range(i+1,n-1):
            #print "content[",j,"]",content[j]
            #print "content[",max,"]",content[max]
            result = if_include(content[cnt],content[j])#if cnt include j ,return True
            #print j,result,cnt
            if result:
                cnt = j
        if cnt != i:
            buff = content[i]
            content[i] = content[cnt]
            content[cnt] = buff
        epn.write(str(content[i]))
    epn.write("]")
    ep.close()
    epn.close()

