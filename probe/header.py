#!/usr/bin/python
import json
import re
import copy


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
        #print "moleculeA: "
        #print a
        #print "moleculeB: "
        #print b

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


