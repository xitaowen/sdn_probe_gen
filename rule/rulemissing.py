#!/usr/bin/python
import re
import json
import random

def type_parse(fileName):
    fileHandle = open(fileName)
    types=[]
    lines = fileHandle.readlines()
    for line in lines:
        reg = re.compile(r'"(.+?)"')
        types.append(reg.findall(line)[0])
    fileHandle.close()
    return types

import sys
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: 4"
        sys.exit(1)

    dp = open(sys.argv[2],"r")
    ft = open(sys.argv[1],"r")
    test = open(sys.argv[3],"w")
    types = type_parse("typename.txt")
    data = {}

    #write the dependency
    depen = []
    dpcontent = dp.read()
    dpct = dpcontent.split(")")
    temp = []
    for pair in dpct:
        tmp = pair.split("(")
        if len(tmp) >= 2:
            temp.append(tmp[1])
    dpct = temp
    temp = []
    for pair in dpct:
        temp.append(pair.split(","))
    dpct = temp
    #print dpct
    for i in range(0,len(dpct)):
        depen.append(dpct[i][0]+"," + dpct[i][1])
    data["dependency"] = depen

    #write the table
    tab = []
    rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
    ftcontent = ft.read()
    patterns = rule_pattern.findall(ftcontent)
    total = len(patterns)
    for i,line in enumerate(patterns):
        rule={}
        at = {}
        r = random.randint(0,2)
        if not r == 0:
            at["output"] = str(r)
        rule["actions"] = at
        rule["id"] = str(i)
        rule["priority"] = str(total-i)
        for typ in types:
            pattern = typ +'=((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))(\/{1})(([1-3]\d)|[0-9]))'
            reg = re.compile(pattern)
            value = reg.findall(line)
            if not (len(value)==0):
                if typ == "ipSrc":
                    rule["src-ip"] = value[0][0]
                if typ == "ipDst":
                    rule["dst-ip"] = value[0][0]
            pattern = typ +'=(?:([0-9]+)[\ ])'
            reg = re.compile(pattern)
            value = reg.findall(line)
            if not (len(value)==0):
                if typ == "tcpSrcPort":
                    rule["src-port"] = value[0]
                if typ == "tcpDstPort":
                    rule["dst-port"] = value[0]
        tab.append(rule)
    tab = tab[0:-1]
    data["table"] = tab

    #convert to json
    encode = json.dumps(data,indent=4)
    test.write(encode)

    test.close()
    dp.close()
    ft.close()
