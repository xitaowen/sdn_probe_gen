#!/usr/bin/python
import json
import re
import copy

output_file = open("data_to_injector.txt", 'w')

def type_parse(filename):
    fileHandle = open(filename)
    types = []
    lines = fileHandle.readlines()
    for line in lines:
        reg = re.compile(r'"(.+?)"')
        types.append(reg.findall(line)[0])
    fileHandle.close()
    return types

def rule_parse(types, rule_data):
    rule_list = []
    for i in range(len(rule_data)):
        #print rule_data[i]
        rule = []
        for feature in types:
            if feature in rule_data[i]:
                rule.append(rule_data[i][feature])
            else:
                rule.append(-1)
        #print rule
        rule_list.append([[rule]])

    return rule_list

def createPacket(subtraction, types):
    if subtraction == None:
        return {}

    rule = subtraction[0][0]
    packet = {}
    for i in range(len(rule)):
        if rule[i] != -1:
            value = rule[i]
            packet[types[i]] = value
    return packet

# problem
def findRule(sid, rid):
    return rule_list[rid]


# if rule id goes from 0 to N, and rules are sorted according to their id, works
def packetGenerator(edge_dict, rule_list, types):
    # containg all pkt, rule paris
    pairs = []

    header_space = []
    # variable rule1 and rule 2 are int.
    for rule1 in edge_dict:
        #print "rule1 =", rule1
        if edge_dict[rule1]:
            print "rule has other rule to depend on"
            adj_list = edge_dict[rule1]
            #print "adj_list =", adj_list

            for rule2 in adj_list:
                #print data[rule]
                print "rule1 =", rule1
                print "rule2 =", rule2
                intersection = intersect_molecule(rule_list[rule1], rule_list[rule2])
                print "intersection =", intersection
                # perhaps
                subtraction = subtraction_wrapper(intersection, header_space)
                print "subtraction =", subtraction
                packet = createPacket(subtraction, types)
                #print "packet =", packet
                sendToInjector(packet)
                # include the packet and its rule pair
                header_space.append(rule_list[rule2])
                print "header_space:"
                print header_space

                tu = (rule2, packet)
                if tu not in pairs:
                    pairs.append(tu)
                print "pairs =", pairs

                #header_space =
                # update header_space


        else:
            print "rule has no ther rule depend on"
            print "rule1 =", rule1

            subtraction = subtraction_wrapper(rule_list[rule1], header_space)
            print "subtraction =", subtraction

            packet = createPacket(subtraction, types)
            #print "packet =", packet
            sendToInjector(packet)

            tu = (rule1, packet)
            if tu not in pairs:
                pairs.append(tu)
            print "pairs =", pairs

    # should call Qi's module function, comment it for now, print instead
    # sendToInjector(pairs)
    print pairs


def sendToPostcardProcessor(rid,sid, num = 1000):
    pass

def sendToInjector(packet, switch_id = 1, num = 1000):
    output_file.write(str(packet))
    output_file.write('\n')


def include_singu(a,b):
	for i in range(0,len(a)):
		if (a[i] != b[i] and a[i] != -1):
			return False
	return True

#intersection of singu1 and singu2
# -1 means a wildcard
def intersect_singu(a,b):
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

# called by new_dag_generator
def intersect_molecule(a,b):
        print "moleculeA: "
        print a
        print "moleculeB: "
        print b

	ans = []
	for atomA in a:
		for atomB in b:
			newAtom = intersect_atom(atomA, atomB)
			if (newAtom != None):
				ans.append(newAtom)

        #print "ans:"
        #print ans
	if (len(ans) == 0):
		return None
	else:
		return ans


# this is not the most efficient but the correctness can be guarenteed.
# after A - B: all atoms in A don't intersect with any atom in B
# called by new_dag_generator.
def subtract_molecule(a,b):
        if a == None:
            return None

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

def subtraction_wrapper(intersection, header_space):
    subtraction = intersection
    if header_space == []:
        return subtraction

    for i in header_space:
        #print "i:"
        #print i
        subtraction = subtract_molecule(subtraction, i)
    return subtraction

#new dag generator
def new_dag_generator(rules):
	dag = []
	for i in range(len(rules)):
		match_range=copy.deepcopy(rules[i])
		if match_range == None:
			continue
		#print "loop on",i
		#print "---------------------------------"
		for j in range(i+1,len(rules)):
			#print "     and rule",j,":",rules[j]
		  if (rules[j] != None):
                        #print "rules[j]:"
                        #print rules[j]
			if intersect_molecule(match_range, rules[j])!=None:
				dag.append((i,j))
				#match_range = subtract_molecule(match_range,rules[j])
				#print "match changes to   ",match_range
				#print rules[i]
				#print rules[j]
				rules[j] = subtract_molecule(rules[j],rules[i])
				#print "rule",j,"changes to   ",rules[j]
	return dag

# without the trailing [] at the end of my rule
def new_rule_parse(types,filename):
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
		rules.append([[rule]])
	return rules
# algo 2
def pktGenerator_2(pos, rule_list, types,intersect,log):
    if intersect == None:
        return []

    intersect = copy.deepcopy(intersect)
    log = copy.deepcopy(log)
    ret = []

    if pos >= len(rule_list):
        print "log = ",log
        print "intersect",intersect
        ret.append((log,createPacket(intersect,types)))
        return ret
    #for i in range(pos,len(rule_list)):
    i = pos
    cur = pktGenerator_2(i+1, rule_list, types, intersect, log)
    ret += cur

    intersect = intersect_molecule(intersect,rule_list[i])
    #print intersect
    if intersect != None:
        log.append(i)
        cur = pktGenerator_2(i+1, rule_list, types, intersect, log)
        ret += cur
    return ret

if __name__ == "__main__":
    f = open("output")
    types = type_parse("typename.txt")
    #print types

    #print "len of types =", len(types)

    line_count = 1

    rule_list = []
    edge_list = []
    edge_dict = {}

    # data preparation
    while True:
        line = f.readline()
        line = line[:-1]

        if line_count == 1:
            rule_list = line.split(' ')
            rule_list = [int(i) for i in rule_list]

            for i in rule_list:
                edge_dict[i] = []

        if line_count == 2:
            edge_list = line.split(' ')

            for i in edge_list:
                i = i[1:-1]
                i = i.split(',')
                edge_dict[int(i[0])].append(int(i[1]))

        if len(line) == 0:
            break

        line_count += 1

    data_file = open("data.json")
    rule_data = json.load(data_file)

    rule_list = rule_parse(types, rule_data)
    print "rule_list = ",rule_list

    #packetGenerator(edge_dict, rule_list, types)
    header = []
    for feature in types:
        header.append(-1)
    header = [[header]]
    log = []
    pkts = pktGenerator_2(0,rule_list,types,header,log)
    #print "packets = ",pkts

    #print rule_list
    #print edge_list
    #print edge_dict
    f.close()
    data_file.close()


