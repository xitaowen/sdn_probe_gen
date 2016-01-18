from probe import launcher 

import random
import os

def generate(inputs):
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        #print case
        cmd = "cd rule;sh generator.sh "+name+" "+str(size)
        print cmd
        os.system(cmd)
def rgenerate(inputs):
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        cmd = "cd rule;sh rgenerator.sh "+name+" "+str(size)
        print cmd
        os.system(cmd)

if __name__ == "__main__":
    #level = 2
    #step = 10
    from settings import level
    from settings import step
    inputs = {}
    #for l in range(level):
    #    for i in range(l*step,(l+1)*step):
    #        inputs[i] = [10**(l+1),str(i)]
    #inputs[0] = [10,"fig1"+str(0)]
    #inputs[1] = [20,"fig1"+str(1)]
    #inputs[2] = [40,"fig1"+str(2)]
    #inputs[3] = [80,"fig1"+str(3)]
    #inputs[4] = [160,"fig1"+str(4)]
    #inputs[4] = [15,"fig1"+str(4)]
    #inputs[5] = [320,"fig1"+str(5)]
    #inputs[6] = [640,"fig1"+str(6)]
    #inputs[7] = [1280,"fig1"+str(7)]
    #for i in range(3*step,4*step):
    #    inputs[i] = [10000,str(i)]
    nums = [10,20,40,80,160,320]
    nums = [320]
    for num in range(0,len(nums)):
        for case in range(0,5):
            inputs[case] = [nums[num],"fig"+str(nums[num])+"_"+str(case)]
    print inputs
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        print "case: ",case
        ins ={}
        ins[0] = case
        generate(ins)
        while True:
            error = -1
            ret = launcher.preTest("./data/"+name)
            if ret[0] == True:
                print "OK:case: ",case
                break
            else:
                error = ret[1]
            print "Fail, retry,",error
            filename = "./rule/data/"+name+"_2"
            handler = open(filename)
            rules = handler.readlines()
            handler.close()
            
            handler = open(filename,'w')
            for i in range(0,len(rules)):
                if i != error:
                    handler.writeline(rules[i])
            handler.close()
            rgenerate(ins)
