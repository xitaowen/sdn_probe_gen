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
    inputs[0] = [320,"fig15"]
    #inputs[6] = [640,"fig1"+str(6)]
    #inputs[7] = [1280,"fig1"+str(7)]
    
    total = 0
    right = 0
    times = ["calc","solver","send","total"]
    for option in ["fault","full-adapt","semi-adapt"]:
    #for option in ["semi-adapt"]:
        case = [320,"fig15"]
        #case = [80,"fig13"]
        size= case[0]
        name = case[1]
        for error in [1,2,4,8,16,32]:
            faultName = name + "_" +str(error)
            if option == "fault":
            	print option,"detection both missing and out of order. case with[size,inputFile]:",case,". fault rules:",error
                ret = launcher.launcherAWithWrongTable("./data/"+name,"./data/"+faultName+".mix")
            elif option == "full-adapt":
            	print option,"full-adapt both missing and out of order. case with[size,inputFile]:",case,". fault rules:",error
                ret = launcher.launcherCWithWrongTable("./data/"+name,"./data/"+faultName+".mix")
            elif option == "semi-adapt":
            	print option,"semi-adapt both missing and out of order. case with[size,inputFile]:",case,". fault rules:",error
                #ret = launcher.launcherD("./data/"+name)
                ret = launcher.launcherDWithWrongTable("./data/"+name,"./data/"+faultName+".mix")
            pass
        if ret[0] == True:
            right += 1
        total += 1
    print right,"/",total


