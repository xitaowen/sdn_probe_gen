import logging
import sys
import time
import json

import PostcardGernerator
from PostCardProcessor import *
TIME_WAIT = 1

class Sender:
    def __init__(self):
        self.name = "packets"

    def send(self,pkt):
        import socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.name)
        sock.send(json.dumps(pkt))
        #print sock.recv(1024)
        sock.close()

def launcherA(dag_file):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()

    #collect postcard
    post = PostCardProcessor('s1-eth4')
    post.start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    delta = time.time()

    import parser, FaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = FaulDete.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['rid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    while True:
        #print postCardQueue.qsize()
        try:
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            #logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                logging.info("55#Failed!")
                print "Failed!"
                flag = False
                return flag,time.time()-delta-TIME_WAIT
            else:
                logging.info("56#Success!")
                print "Success!"
                flag = True
                return flag,time.time()-delta-TIME_WAIT
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
                logging.debug("11# actually, Y pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
            else:
                unmatch += 1
                #logging.info("55#Unfinished!")
                logging.warn("11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
                pkt = pairs[pid][1]
                warn = ""
                for typ in ['src-ip','dst-ip','src-port','dst-port']:
                    warn += typ+":"+str(pkt[typ])+";"
                logging.warn("12#"+warn)
                #break
    logging.info("56# Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch) )
    logging.info("57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT))
    print "Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch) 
    print "57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT)
    Flag = False
    return flag,time.time()-delta-TIME_WAIT

def launcherAWithWrongTable(dag_file, wrong_dag):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.WARNING)

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(wrong_dag)
    pcg.start()

    #collect postcard
    post = PostCardProcessor('s1-eth4')
    post.start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    delta = time.time()

    import parser, FaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = FaulDete.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['rid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    while True:
        #print postCardQueue.qsize()
        try:
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            #logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                print "Failed!"
                flag = False
                return flag,time.time()-delta-TIME_WAIT
            else:
                logging.info("56#Success!")
                print "Success!"
                flag = True
                return flag,time.time()-delta-TIME_WAIT
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
                logging.debug("11# actually, Y pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
            else:
                unmatch += 1
                #logging.info("55#Unfinished!")
                logging.warn("11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
                pkt = pairs[pid][1]
                warn = ""
                for typ in ['src-ip','dst-ip','src-port','dst-port']:
                    warn += typ+":"+str(pkt[typ])+";"
                logging.warn("12#"+warn)
                #break
    logging.info("56# Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch) )
    logging.info("57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT))
    Flag = False
    return flag,time.time()-delta-TIME_WAIT

def launcherC(dag_file):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()

    #collect postcard
    post = PostCardProcessor('s1-eth4')
    post.start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    delta = time.time()

    import parser, FullAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    flag = FullAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue)
    if flag == False:
        print "Failed!"
    elif flag == True:
        print "Success!"
    else:
        print "Unexpected!"
    Flag = False
    return flag,time.time()-delta-TIME_WAIT
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['rid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    while True:
        #print postCardQueue.qsize()
        try:
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            #logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                logging.info("55#Failed!")
                print "Failed!"
                flag = False
                return flag,time.time()-delta-TIME_WAIT
            else:
                logging.info("56#Success!")
                print "Success!"
                flag = True
                return flag,time.time()-delta-TIME_WAIT
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
                logging.debug("11# actually, Y pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
            else:
                unmatch += 1
                #logging.info("55#Unfinished!")
                logging.warn("11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
                pkt = pairs[pid][1]
if __name__ == "__main__":
    #parse the input arguments
    if len(sys.argv) != 2:
        print "Usage: python launcher.py dag_file"
        exit(0)
    dag_file = sys.argv[1]
    #launcherA(dag_file)
    launcherC(dag_file)

