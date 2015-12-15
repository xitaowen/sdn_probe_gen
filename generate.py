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
        #os.system(cmd)

if __name__ == "__main__":
    #level = 2
    #step = 10
    from settings import level
    from settings import step
    inputs = {}
    #for l in range(level):
    #    for i in range(l*step,(l+1)*step):
    #        inputs[i] = [10**(l+1),str(i)]
    inputs[0] = [10,"fig1"+str(0)]
    inputs[1] = [20,"fig1"+str(1)]
    inputs[2] = [40,"fig1"+str(2)]
    inputs[3] = [80,"fig1"+str(3)]
    inputs[4] = [160,"fig1"+str(4)]
    inputs[5] = [320,"fig1"+str(5)]
    inputs[6] = [640,"fig1"+str(6)]
    inputs[7] = [1280,"fig1"+str(7)]
    inputs[8] = [2560,"fig1"+str(8)]
    #for i in range(3*step,4*step):
    #    inputs[i] = [10000,str(i)]

    generate(inputs)
    

