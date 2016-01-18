from probe import launcher 

import random
import os

#level = 2
#step = 10
from settings import level
from settings import step

def generate(inputs):
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        cmd = "cd rule;sh generator.sh "+name+" "+str(size)
        print cmd
        os.system(cmd)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 1:
        print "Usage: python Test.py Mode [fault|non-adapt|full-adapt|semi-adapt]"
        print "mode 0: correct table"
        print "mode 1: missing rule"
        print "mode 2: priority fault"
        exit(1)
    #generate(inputs)
    inputs = {}
    inputs[0] = [10,"fig1"+str(0)]
    inputs[1] = [20,"fig1"+str(1)]
    inputs[2] = [40,"fig1"+str(2)]
    inputs[3] = [80,"fig1"+str(3)]
    inputs[4] = [160,"fig1"+str(4)]
    inputs[5] = [320,"fig1"+str(5)]
    #inputs[6] = [640,"fig1"+str(6)]
    #inputs[7] = [1280,"fig1"+str(7)]
    
    total = 0
    right = 0
    times = ["calc","solver","send","total"]
    for option in ["fault","full-adapt","semi-adapt"]:
        for key in inputs:
            case = inputs[key]
            size= case[0]
            name = case[1]
            print option,"detection. case with[size,inputFile]: ",case
            if option == "fault":
                ret = launcher.launcherA("./data/"+name)
            elif option == "none-adapt":
                ret = launcher.launcherB("./data/"+name)
            elif option == "full-adapt":
                ret = launcher.launcherC("./data/"+name)
            elif option == "semi-adapt":
                ret = launcher.launcherD("./data/"+name)
        if ret[0] == True:
            right += 1
        total += 1
    print right,"/",total


