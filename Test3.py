from probe import launcher 

import random
import os

def generate(inputs):
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        cmd = "cd rule;sh generator.sh "+name+" "+str(size)
        print cmd
        os.system(cmd)

if __name__ == "__main__":
    step = 10;
    inputs = {}
    for i in range(0,step):
        inputs[i] = [10,str(i)]
    for i in range(step,2*step):
        inputs[i] = [100,str(i)]
    #for i in range(2*step,3*step):
    #    inputs[i] = [1000,str(i)]
    #for i in range(3*step,4*step):
    #    inputs[i] = [10000,str(i)]

    #generate(inputs)
    
    total = 0
    right = 0
    time = {}
    time[0] = 0
    time[1] = 0
    time[2] = 0
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        #ret = launcher.launcherA("./data/"+name)
        ret = launcher.launcherAWithWrongTable("./data/"+name,"./data/"+name+".order")
        if ret[0] == True:
            right += 1
        total += 1
        time[key/step] += ret[1]
    print right,"/",total
    for i in range(0,3):
        print i,time[i],
        if step > 0:
            print time[i]/step


