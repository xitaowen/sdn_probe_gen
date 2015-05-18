#!/usr/bin/python
import json
import re

def type_parse(filename):
    fileHandle = open(filename)
    types = []
    lines = fileHandle.readlines()
    for line in lines:
        reg = re.compile(r'"(.+?)"')
        types.append(reg.findall(line)[0])
    fileHandle.close()
    return types
def LoadFile(filename):
    fileHandle = open(filename,'r');
    content = fileHandle.read()
    fileHandle.close()
    return content;
import json
def DAGLoader(filename):
    types = type_parse("typename.txt")
    f = LoadFile(filename)
    data = json.loads(f)
    #(0,1): rule 1 depends on rule 0
    dag = data["dependency"]
    ret_dag = {}
    for dep in dag:
        dep = dep.split(",")
        if not ret_dag.has_key(int(dep[0])):
            ret_dag[int(dep[0])] = []
        ret_dag[int(dep[0])].append(int(dep[1]))
    ret_rules = {}
    rules = data["table"]
    #print rules
    for line in rules:
        rule = {}
        for typ in types:
            if (not line.has_key(typ)) or (rule.has_key(typ)):
                continue
            if typ == "src-ip":
                dt = line[typ]
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

            elif typ == "dst-ip":
                dt = line[typ]
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
            else:
                rule[typ] = int(line[typ])
        rl = []
        for typ in types:
            if rule.has_key(typ):
                rl.append(rule[typ])
            else:
                rl.append(-1)
        ids = int(line["id"])
        ret_rules[ids] = [[rl]]

    edges = 0
    for r1 in ret_dag:
        edges += len(ret_dag[r1])
    #print "nodes,edges:",len(ret_dag),edges
    return ret_rules, ret_dag
