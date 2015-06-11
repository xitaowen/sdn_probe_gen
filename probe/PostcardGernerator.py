#!/usr/bin/python
import string
import json
import sys
import os
import logging

import parser

class PostcardGernerator:
    def __init__(self, fname):
        self.name = fname
    def transfer(self, rule):
        ret = "/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  "
        detail = ""
        rid = "0"
        ip = "dl_type=0x0800,"
        tcp = "dl_type=0x0800,nw_proto=6,"
        fg_tcp = False
        fg_ip = False
        for typ in rule:
            #print typ
            cmd = ""
            if typ == "src-ip":
                fg_ip = True
                cmd = "nw_src="+rule[typ]
            elif typ == "dst-ip":
                fg_ip = True
                cmd = "nw_dst="+rule[typ]
            elif typ == "src-port":
                fg_tcp = True
                cmd = "tcp_src="+rule[typ]
            elif typ == "dst-port":
                fg_tcp = True
                cmd = "tcp_dst="+rule[typ]
            elif typ == "priority":
                cmd = "priority="+rule[typ]
            elif typ == "id":
                rid = rule[typ]
            if len(cmd) > 0:
                #print cmd
                detail = detail + cmd + ","
            else:
                logging.debug("20#Unmatch Type"+typ)
        if fg_tcp:
            ret = ret + tcp
        elif fg_ip:
            ret = ret + ip
        ret = ret + detail
        ret = ret + "actions=" + "push_mpls:0x8847,set_mpls_label:" + rid + ",output:" + str(4)
        #print "command:",ret
        return ret



    def start(self):
        # load flow table
        self.types = parser.type_parse("typename.txt")
        #print self.name
        f = parser.LoadFile(self.name)
        #print f
        data = json.loads(f)
        rules = data["table"]

        #parse flow table to cmds
        cmds = ["/ovs/bin/ovs-ofctl -O OpenFlow13 del-flows br0"]
        for rule in rules:
            cmds.append(self.transfer(rule))

        #excute those command on sh
        f = open("postcard.sh","w")
        for cmd in cmds:
            f.write(cmd)  # write the cmd into bash
            f.write("\n")
        f.close()
        #excute those command
        #os.system("scp ./postcard.sh admin@openflow-0.cs.northwestern.edu:~/")
        #os.system("ssh admin@openflow-0.cs.northwestern.edu -t \"sh ./postcard.sh\"")
        os.system("bash postcards.sh")

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
