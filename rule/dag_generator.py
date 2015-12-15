#!/usr/bin/python
import sys
import os
import re
import copy
#import networkx as nx
#import matplotlib.pyplot as plt

#atom = value[]



def atom_intersection(atom1,atom2):
	ans = []
	for i in range(len(atom1)):
		if (atom1[i] == atom2[i]):
			ans.append(atom1[i])
		elif (atom1[i] == -1):
			ans.append(atom2[i])
		elif (atom2[i] == -1):
			ans.append(atom1[i])
		else:
			return None
	return ans

#molecule[0] = a list of +atoms
#molecule[1] = a list of -atom
def molecule_intersection(molecule1, molecule2):
	ans=[[],[]]
	if molecule1==None or molecule2==None:
		#print "Molecule1",molecule1,"Molecule2",molecule2
		return None
	for sign1 in range(2):
	  for sign2 in range(2):
		for i in range(len(molecule1[sign1])):
			for j in range(len(molecule2[sign2])):
				ret = atom_intersection(molecule1[sign1][i],molecule2[sign2][j])
				if ret != None:
					ans[sign1 ^ sign2].append(ret)
	return molecule_trim(ans)

#set is a list of atoms

def merge_place(atom1, atom2):
	place = -1
	dif_num = 0
	for i in range(len(atom1)):
		if atom1[i] != atom2[i]:
			dif_num +=1
			if dif_num>1:
				return -1
			if atom1[i]!=-1 and atom2[i]!=-1:
				place=i
	if place>=6 and place<=69:
		return place
	else:
		return -1

#brute force a smarter idea is sort
def set_merge(set):
	find=True
	while find:
		find = False
		for i in range(len(set)):
			for j in range(i):
				place = merge_place(set[i],set[j])
				if place > 0:
					find=True
					set[j][place]=-1
					del set[i]
					break
			if find:
				break
	return set



def molecule_trim(ans):
	find = True
	ans[0]=set_merge(ans[0])
	ans[1]=set_merge(ans[1])
	while find:
		find = False
		for i in range(len(ans[0])):
			for j in range(len(ans[1])):
				if ans[0][i] == ans[1][j]:
					del ans[0][i]
					del ans[1][j]
					find = True
					break
			if find:
				break
	if (len(ans[1]) == 0) and (len(ans[0]) == 0):
		return None
	else:
		return ans

def molecule_minus(molecule1, molecule2):
	ans = molecule1
	intersection = molecule_intersection(molecule1,molecule2)
	if intersection != None:
		for atom in intersection[0]:
			ans[1].append(atom)
		for atom in intersection[1]:
			ans[0].append(atom)
	return molecule_trim(ans)

#rules[index] = molecule

def dag_generator(rules):
	dag = []
	for i in range(len(rules)):
		match_range=copy.deepcopy(rules[i])
		#print "loop on",i
		#print "---------------------------------"
		for j in range(i+1,len(rules)):
			#print "Comparing",match_range,"     and rule",j,":",rules[j]
			if molecule_intersection(match_range, rules[j])!=None:
				dag.append((i,j))
				match_range = molecule_minus(match_range,rules[j])
				#print "match changes to   ",match_range
				rules[j] = molecule_minus(rules[j],rules[i])
				#print "rule",j,"changes to   ",rules[j]
				if match_range == None:
					break
	return dag

def type_parse(fileName):
	fileHandle = open(fileName)
	types=[]
	lines = fileHandle.readlines()
	for line in lines:
		reg = re.compile(r'"(.+?)"')
		types.append(reg.findall(line)[0])
	fileHandle.close()
	return types


def rule_parse(types,filename):
	fileHandle = open(filename)
	rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
	content = fileHandle.read()
	#print content
	patterns = rule_pattern.findall(content)
	#print patterns
	rules=[]
	for line in patterns:
		rule=[]
		for type in types:
			pattern = type +'=(\d+?),'
			reg = re.compile(pattern)
			value = reg.findall(line)
			if len(value)==0:
				rule.append(-1)
			else:
				rule.append(int(value[0]))
		#print rule
		rules.append([[rule],[]])
	fileHandle.close()
	return rules


def draw_dag(rules,dag):
    dg = nx.DiGraph()
    for i in range(len(rules)):
        dg.add_node(i)
    for p in dag:
        dg.add_edge(p[0],p[1])
    nx.draw_circular(dg)
    plt.show()

def transitive_reduction(dag, maxi):
	connected =[]
	for i in range(maxi):
		connected.append([0 for i in range(maxi)])
	for i in range(len(dag)):
		connected[dag[i][1]][dag[i][0]] = 1
	tr_dag = []
	for i in range(maxi):
		for j in range(i):
			if (connected[i][j] == 1):
				for k in range(j+1,i):
					if (connected[i][k] ==1 and connected[k][j] ==1):
						connected[i][j] =0
						break
			if (connected[i][j] == 1):
				tr_dag.append((j,i))
	return tr_dag
#   Structure
#   singularity = [value1,value2,....., ,]  value -1 means a wildcard
#   atom = main singularity - {singularity i}
#   atom = [main singularity, singularity 1, singularity 2, ....]
#   molecule = [atom1, atom2, atom......]


#singu a include singu b
def include_singu(a,b):
	for i in range(0,len(a)):
		if (a[i] != b[i] and a[i] != -1):
			return False
	return True

#intersection of singu1 and singu2
# -1 means a wildcard
def intersect_singu(a,b):
#	print "a ",a
#	print "b ",b
	ans = []
	for i in range(0,len(a)):
		if (a[i] == b[i]):
			ans.append(a[i])
		elif (a[i] == -1):
			ans.append(b[i])
		elif (b[i] == -1):
			ans.append(a[i])
		else:             # a and b differing on any value domain indicates that they don't intersect
			return None
	return ans


# intersection of atom1 and atom2 : a new atom whose main area is the intersection of the two main areas
#                                   and whose holes are old holes of atom1 and atom2 that remain in the new main area
# Potential optimization: check repetition
def intersect_atom(a,b):
	ans=[]
	domain = intersect_singu(a[0],b[0])
	if (domain == None):
		return None
	ans.append(domain)
	for i in range(1,len(a)):
		temp = intersect_singu(domain, a[i])
		if (temp != None):
			ans.append(temp)
	for i in range(1,len(b)):
		temp = intersect_singu(domain, b[i])
		if (temp != None):
			ans.append(temp)
	for i in range(1,len(ans)):
		if (ans[i] == ans[0]):
			return None
	return ans
# using '^' to represent intersect
# atomA ([mainA, singuA1, singuA2....])  - atomB ([mainB, singuB1, singuB2, ...] =
#  [mainA, mainA ^ mainB, singuA1, singuA2.., singuAn] +
#  [singuBi ^ mainA ^ main B, singuA1, singuA2...., singuAn]
# Reason: any hole in A will still be a hole
#         intersection of mainA and mainB will be a new hole
#         the part of a hole in B that falls into (mainA^mainB) and doesn't intersect with any hole in A results in a concrete piece after A-B
#  always return a molecule
def subtract_atom(a,b):
	newAtom1 = []
	newDomain = intersect_singu(a[0],b[0])
	if (newDomain == None):
		return None
	for i in range(1,len(a)):
		if include_singu(a[i],newDomain):
			return None
	ans = []
	if (include_singu(newDomain,a[0]) == False):
		newAtom1.append(a[0])
		newAtom1.append(newDomain)
		for i in range(1,len(a)):
			if (include_singu(newDomain,a[i]) == False):
			#only subtract holes of A that don't fall into the new hole mainA^mainB
				newAtom1.append(a[i])
		ans.append(newAtom1)
	for i in range(1,len(b)):
		atomMain = intersect_singu(b[i],a[0]) #b[i] is already in mainB
		if (atomMain == None):
			continue
		newAtom = [];
		newAtom.append(atomMain)
		valid = True
		for j in range(1,len(a)):
			singu = intersect_singu(atomMain,a[j])
			if (singu != None):
				if (singu == atomMain):
					valid = False
					break
				else:
					newAtom.append(singu)
		if (valid):
			ans.append(newAtom)
	return ans
#moleculeA @ moleculeB = atoms in A @ atoms in B
# atoms in the same molecule don't intersect
def intersect_molecule(a,b):
	ans = []
	for atomA in a:
		for atomB in b:
			newAtom = intersect_atom(atomA, atomB)
			if (newAtom != None):
				ans.append(newAtom)
	if (len(ans) == 0):
		return None
	else:
		return ans


# this is not the most efficient but the correctness can be guarenteed.
# after A - B: all atoms in A don't intersect with any atom in B
def subtract_molecule(a,b):
	ans = [copy.deepcopy(atom) for atom in a]
	cursor =0
	while (cursor < len(ans)):
		deleted = False
		for atom in b:
			temp = subtract_atom(ans[cursor],atom)
			if (temp != None):
				del ans[cursor]
				if (len(temp) == 0):  # A[cursor] is subtracted to empty
					deleted= True
					break
				ans.insert(cursor,temp[0]) # replace A[cursor] with a subtracted atom
				for i in range(1,len(temp)):
					ans.append(temp[i]) #append the rest subtracted atoms
		if (not deleted):
			cursor+=1
	if (len(ans) == 0):
		return None
	else:
		return ans

#new dag generator
def new_dag_generator(rules):
	dag = []
#	print "len",len(rules)
	for i in range(len(rules)):
		if rules[i] == None:
			continue
		match_range=copy.deepcopy(rules[i])
		if match_range == None:
			continue
		#print "loop on",i
		#print "loop on",i
		#print "---------------------------------"
		for j in range(i+1,len(rules)):
 			if i == 56 and j == 71:
 				pass#print intersect_molecule(match_range, rules[j])#pass#print rules[i],rules[j]
			if rules[j] == None:
				print j
				continue
			#print "     and rule",j,":",rules[j]
			if intersect_molecule(match_range, rules[j])!=None:
 				if i == 56 and j == 71:
 					pass#print i,j
				dag.append((i,j))
				#match_range = subtract_molecule(match_range,rules[j])
				#print "match changes to   ",match_range
				#print rules[i]
				#print rules[j]
				rules[j] = subtract_molecule(rules[j],rules[i])
				#print "rule",j,"changes to   ",rules[j]
	return dag

def new_rule_parse(types,filename):
	fileHandle = open(filename)
	rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
	content = fileHandle.read()
	#print filename
	#print content
	patterns = rule_pattern.findall(content)
	#print patterns
	rules=[]
	for line in patterns:
		rule=[]
		for type in types:
			pattern = type +'=([0-9]+)'
			reg = re.compile(pattern)
			value = reg.findall(line)
			if len(value)==0:
				rule.append(-1)
			else:
				#print type," ",int(value[0])
				rule.append(int(value[0]))
		#print rule
		rules.append([[rule]])
	fileHandle.close()
	return rules
def new_new_rule_parse(types,filename):
    fileHandle = open(filename)
    content = fileHandle.read()
    rule_pattern = re.compile(r'pattern=([\s\S]*?)action=')
    patterns = rule_pattern.findall(content)
    #print patterns[56]
    #print patterns[71]

    types1 = type_parse("typename.txt")
    ret = []
    for pattern in patterns:
        rules = {}
        types = ["tcpSrcPort","tcpDstPort","ipSrc","ipDst"]
        for typ in types:
            #process port
            patt = typ +'=([0-9]+)'
            reg = re.compile(patt)
            #print "patterns[0]",patterns[0]
            #print patterns
            #print patterns[0]
            #print reg.findall(patterns[0])
            value = reg.findall(pattern)
            if not (len(value)==0):
                rules[typ] = value[0]
            #process ip
            pattern1 = typ +'=((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))(\/{1})(([1-3]\d)|[0-9]))'
            reg1 = re.compile(pattern1)
            value1 = reg1.findall(pattern)
            if not (len(value1)==0):
                rules[typ] = value1[0][0]

        #print rules
        rule = {}
        for typ in types:
            if (not rules.has_key(typ)) or (rule.has_key(typ)):
                continue
            if typ == "tcpSrcPort":
                rule[typ] = int(rules[typ])
            if typ == "tcpDstPort":
                rule[typ] = int(rules[typ])
            if typ == "ipSrc":
                dt = rules[typ]
                dt = dt.split('/')
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
        rl = []
        for typ in types1:
            if rule.has_key(typ):
                rl.append(rule[typ])
            else:
                rl.append(-1)
        ret.append([[rl]])
    for i in range(0,len(types1)):
        typ = types1[i]
        #print typ,ret[56][0][0][i]
    for i in range(0,len(types1)):
        typ = types1[i]
        #print typ,ret[71][0][0][i]
    return ret



if __name__=="__main__":
#parse all the types
    types = type_parse("typename.txt")
    if len(sys.argv) != 2:
        print "Usage: python dag_generator.py rule_file_path"
        print "One pattern on each line in rule_file."
        sys.exit(0)
#	rules = rule_parse(types,sys.argv[1])
#	print len(rules)
#	print (rules)
#	dag=dag_generator(rules)
#	print "-----original dag-------"
#	print dag
#	print "-----after reduction----"
#	tr_dag = transitive_reduction(dag, len(rules))
#	print tr_dag
    rules = new_new_rule_parse(types,sys.argv[1])
    #print rules
    dag=new_dag_generator(rules)
#	print "-----new dag-------"
#	print dag
#	print "-----after reduction----"
    #dag = transitive_reduction(dag, len(rules))
    print dag
	#draw_dag(rules,dag)

