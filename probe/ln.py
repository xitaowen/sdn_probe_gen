
import logging
import sys
import time
import json

import PostcardGernerator
from PostCardProcessor import *

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


if __name__ == "__main__":
    #parse the input arguments
    if len(sys.argv) != 2:
        print "Usage: python launcher.py dag_file"
        exit(0)
    dag_file = sys.argv[1]

    #set the log mode
    logging.basicConfig(level=logging.DEBUG)

    #collect postcard
    post = PostCardProcessor('s1-eth4')
    post.start()
    time.sleep(1)
    logging.info("1# start to collect %.8f" %time.time())

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()


    #start to generate packets
    import parser, FaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = FaulDete.packetGenerator(edge_dict, rule_list, types)
    logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    logging.info("3# packets flushed to datapath %.8f" %time.time())
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['rid'] = i
        pid2rid[i] = rid
        logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)


    #process with the postcard
    while True:
        print postCardQueue.qsize()
        try:
            card = postCardQueue.get()
            #card = (1,1)
            print card
        except Exception:
            logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                logging.info("Unfinished!")
            else:
                logging.info("Success!")
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            if rid == pid2rid[pid]:
                pid2rid.pop(pid)
            else:
                logging.info("Unfinished!")
                #break
            logging.debug("11# actually, pid to rid: %d - %d." % (pid,rid))


