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
    #level = 2
    #step = 10
    from settings import level
    from settings import step
    inputs = {}
    for l in range(level):
        for i in range(l*step,(l+1)*step):
            inputs[i] = [10**(l+1),str(i)]
    #for i in range(3*step,4*step):
    #    inputs[i] = [10000,str(i)]

    generate(inputs)
    

