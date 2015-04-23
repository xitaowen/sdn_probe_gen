#!/usr/bin/python
import string
import json
import sys
import os

import parser

class PostcardGernerator:
    def __init__(self, fname):
        self.name = fname
    def transfer(self, rule):
        ret = "ovs-ofctl -O OpenFlow13 add-flow s1  "
        rid = "0"
        for typ in rule:
            #print typ
            cmd = ""
            if typ == "src-ip":
                cmd = "nw_src="+rule[typ]
            elif typ == "dst-ip":
                cmd = "nw_dst="+rule[typ]
            elif typ == "src-port":
                cmd = "tp-src="+rule[typ]
            elif typ == "dst-port":
                cmd = "tp-dst="+rule[typ]
            elif typ == "priority":
                cmd = "priority="+rule[typ]
            elif typ == "id":
                rid = rule[typ]
            if len(cmd) > 0:
                #print cmd
                ret = ret + cmd + ","
            else:
                print "Unmatch Type",typ
        ret = ret + "actions=" + "push_mpls:0x8847,set_mpls_label:" + rid + ",output:" + str(4)
        print "command:",ret
        return ret



    def start(self):
        # load flow table
        self.types = parser.type_parse("typename.txt")
        f = parser.LoadFile(self.name)
        data = json.loads(f)
        rules = data["table"]

        #parse flow table to cmds
        cmds = []
        for rule in rules:
            cmds.append(self.transfer(rule))

        #excute those command on sh
        f = open("postcard.sh","w")
        for cmd in cmds:
            f.write(cmd)  # write the cmd into bash
            f.write("\n")
        f.close()
        #excute those command
        os.system("sh postcard.sh")

if __name__ == "__main__":
    name = sys.argv[1]
    print name

    pcg = PostcardGernerator(name)
    pcg.start()
    '''
    data_file = open(name)#open flowtable
    flowtable = json.load(data_file)#decode it
    global relation  #a dictionary the relationship with rid and postcardid
    global pcnumber  #postcardid
    relation = {}
    pcnumber = 0
    #sendtoSend_pkt(flowtable)
    sendtoPostcardGeneration(flowtable)
    #receivefromPostCardProcessor()
    data_file.close()
    '''
