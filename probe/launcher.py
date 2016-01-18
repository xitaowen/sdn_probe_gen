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
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()

    import parser, FaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = FaulDete.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())
    if pairs == False:
        flag = False
        return flag, TimeLog.GetInstance().getCost()
    #print pairs

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    TimeLog.GetInstance().addCalc()
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['pid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)
    TimeLog.GetInstance().addSend()
    TimeLog.GetInstance().addPackets(len(pairs))


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    while True:
        #print postCardQueue.qsize()
        try:
            TimeLog.GetInstance().addTotal()
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            TimeLog.GetInstance().clock()
            #logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                #logging.info("55#Failed!")
                print "Failed!",TimeLog.GetInstance().getCost()
                flag = False
                return flag, TimeLog.GetInstance().getCost()
            else:
                #logging.info("56#Success!")
                print "Success!",TimeLog.GetInstance().getCost()
                flag = True
                return flag, TimeLog.GetInstance().getCost()
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
                #logging.debug("11# actually, Y pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
            else:
                unmatch += 1
                #logging.info("55#Unfinished!")
                #logging.warn("11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
                #print "11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid)
                pkt = pairs[pid][1]
                warn = ""
                for typ in ['src-ip','dst-ip','src-port','dst-port']:
                    warn += typ+":"+str(pkt[typ])+";"
                #logging.warn("12#"+warn)
                #break
                #print "Failed!",TimeLog.GetInstance().getCost()
                TimeLog.GetInstance().addFirst()
                #return flag, TimeLog.GetInstance().getCost()
                #return flag,time.time()-delta-TIME_WAIT
    #logging.info("56# Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch) )
    #logging.info("57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT))
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
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()

    import parser, FaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = FaulDete.packetGenerator(edge_dict, rule_list, types)
    TimeLog.GetInstance().addCalc()
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['pid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)
    TimeLog.GetInstance().addSend()
    TimeLog.GetInstance().addPackets(len(pairs))


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    while True:
        #print postCardQueue.qsize()
        try:
            TimeLog.GetInstance().addTotal()
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            TimeLog.GetInstance().clock()
            #logging.warn("Post Card Queue is empty.")
            if len(pid2rid) > 0:
                print "Failed!",TimeLog.GetInstance().getCost()
                flag = False
                return flag,TimeLog.GetInstance().getCost()
            else:
                print "Success!",TimeLog.GetInstance().getCost()
                flag = True
                return flag,TimeLog.GetInstance().getCost()
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
                #logging.debug("11# actually, Y pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
            else:
                unmatch += 1
                #logging.info("55#Unfinished!")
                #logging.warn("11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid))
                #print "11# actually, N pid to rid, should match: %d - %d - %d." %(pid,rid,rrid)
                pkt = pairs[pid][1]
                warn = ""
                for typ in ['src-ip','dst-ip','src-port','dst-port']:
                    warn += typ+":"+str(pkt[typ])+";"
                #logging.warn("12#"+warn)
                #break
                #print "Failed!",TimeLog.GetInstance().getCost()
                TimeLog.GetInstance().addFirst()
                #return flag,TimeLog.GetInstance().getCost()
    #logging.info("56# Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch) )
    #logging.info("57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT))
    Flag = False
    return flag,time.time()-delta-TIME_WAIT

def launcherB(dag_file):

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
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()

    import parser, NonaTrou
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = NonaTrou.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    TimeLog.GetInstance().addTotal()
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['pid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)
    TimeLog.GetInstance().addSend()


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    VV = []
    EE = []
    while True:
        #print postCardQueue.qsize()
        try:
            TimeLog.GetInstance().addTotal()
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            TimeLog.GetInstance().clock()
            #logging.warn("Post Card Queue is empty.")
            flag = NonaTrou.dagCompare(edge_dict, rule_list, VV, EE)
            if flag == False:
                #logging.info("55#Failed!")
                print "Failed!",TimeLog.GetInstance().getCost()
                flag = False
                return flag, TimeLog.GetInstance().getCost()
            else:
                #logging.info("56#Success!")
                print "Success!",TimeLog.GetInstance().getCost()
                flag = True
                return flag, TimeLog.GetInstance().getCost()
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            if not rid in VV:
                VV.append(rid)
            rrid = pid2rid[pid]
            for r in rrid:
                if r != rid:
                    EE.append([r,rid])

def launcherBWithWrongTable(dag_file, wrong_dag):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(wrong_dag)
    pcg.start()

    #collect postcard
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(0.1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()

    import parser, NonaTrou
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = NonaTrou.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())

    #send the packets
    #logging.info("3# packets flushed to datapath %.8f" %time.time())
    TimeLog.GetInstance().addCalc()
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['pid'] = i
        pid2rid[i] = rid
        #logging.debug("10# pid to rid: %d - %d." % (i,rid))
        sender.send(pkt)
    TimeLog.GetInstance().addSend()


    #process with the postcard
    matched = 0
    unmatch = 0
    flag = True
    VV = []
    EE = []
    while True:
        #print postCardQueue.qsize()
        try:
            TimeLog.GetInstance().addTotal()
            card = postCardQueue.get(True,TIME_WAIT)
            #print card
        except Exception:
            TimeLog.GetInstance().clock()
            #logging.warn("Post Card Queue is empty.")
            flag = NonaTrou.dagCompare(edge_dict, rule_list, VV, EE)
            if flag == False:
                #logging.info("55#Failed!")
                print "Failed!",TimeLog.GetInstance().getCost()
                flag = False
                return flag, TimeLog.GetInstance().getCost()
            else:
                #logging.info("56#Success!")
                print "Success!",TimeLog.GetInstance().getCost()
                flag = True
                return flag, TimeLog.GetInstance().getCost()
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            if not rid in VV:
                VV.append(rid)
            rrid = pid2rid[pid]
            for r in rrid:
                if r != rid:
                    EE.append([r,rid])

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
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()
    TimeLog.GetInstance().clock()

    import parser, FullAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    flag = FullAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue)
    TimeLog.GetInstance().addTotal()
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()
    #return flag,time.time()-delta-TIME_WAIT

def launcherCWithWrongTable(dag_file, wrong_dag):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    from timelog import TimeLog
    TimeLog.GetInstance().reset()
    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(wrong_dag)
    pcg.start()

    #collect postcard
    #post = PostCardProcessor('s1-eth4')
    PostCardProcessor.Start()
    #post.start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    TimeLog.GetInstance().clock()

    import parser, FullAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    flag = FullAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue)
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()
    #return flag,time.time()-delta-TIME_WAIT

def launcherD(dag_file):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    from timelog import TimeLog
    TimeLog.GetInstance().reset()
    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()

    #collect postcard
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    TimeLog.GetInstance().clock()

    import parser, SemiAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    flag = SemiAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue)
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()
    #return flag,time.time()-delta-TIME_WAIT

def launcherDWithWrongTable(dag_file, wrong_dag):

    #set the log mode
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
    #logging.basicConfig(level=logging.ERROR)

    from timelog import TimeLog
    TimeLog.GetInstance().reset()
    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(wrong_dag)
    pcg.start()

    #collect postcard
    #post = PostCardProcessor('s1-eth4')
    PostCardProcessor.Start()
    #post.start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    TimeLog.GetInstance().clock()

    import parser, SemiAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    flag = SemiAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue)
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()
    #return flag,time.time()-delta-TIME_WAIT

def preTest(dag_file):

    import parser, PreTest
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    pairs = PreTest.packetGenerator(edge_dict, rule_list, types)
    #logging.info("2# packets generated %.8f" %time.time())
    if pairs[0] == False:
        flag = False
        return pairs
    return True,0

def launcherE(dag_file, pre_file):
    #set the log mode
    logging.basicConfig(level=logging.WARNING)

    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()

    PostCardProcessor.Start()
    time.sleep(0.1)

    from timelog import TimeLog

    import parser, IncrFaulDete
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file)
    rule_lists,edge_dicts = parser.DAGLoader(pre_file)

    table = []
    for i in rule_list.keys():
        for j in rule_lists.keys():
            ret = cmp(rule_list[i], rule_lists[j])
            if ret == 0:
                #print rule_list[i]
                #print rule_lists[j]
                table.append(i)
    #print table

    TimeLog.GetInstance().reset()
    pairs = IncrFaulDete.packetGenerator(edge_dict, rule_list, types, table)
    if pairs == False:
        flag = False
        return flag, TimeLog.GetInstance().getCost()

    TimeLog.GetInstance().addCalc()
    sender = Sender()
    pid2rid = {}
    for i,pair in enumerate(pairs):
        rid = pair[0]
        pkt = pair[1]
        pkt['pid'] = i
        pid2rid[i] = rid
        sender.send(pkt)
    TimeLog.GetInstance().addSend()
    TimeLog.GetInstance().addPackets(len(pairs))

    matched = 0
    unmatch = 0
    flag = True
    while True:
        try:
            TimeLog.GetInstance().addTotal()
            card = postCardQueue.get(True,TIME_WAIT)
        except Exception:
            TimeLog.GetInstance().clock()
            if len(pid2rid) > 0:
                print "Failed!",TimeLog.GetInstance().getCost()
                flag = False
                return flag, TimeLog.GetInstance().getCost()
            else:
                print "Success!",TimeLog.GetInstance().getCost()
                flag = True
                return flag, TimeLog.GetInstance().getCost()
            break
        pid = card[0]
        rid = card[1]
        if pid in pid2rid:
            rrid = pid2rid[pid]
            if rid == pid2rid[pid]:
                matched += 1
                pid2rid.pop(pid)
            else:
                unmatch += 1
                pkt = pairs[pid][1]
                warn = ""
                for typ in ['src-ip','dst-ip','src-port','dst-port']:
                    warn += typ+":"+str(pkt[typ])+";"
                TimeLog.GetInstance().addFirst()
    print "Finally, %d packets matched right, %d packets mismatched." %(matched,unmatch)
    print "57#time count: %.6f seconds" % (time.time() - delta - TIME_WAIT)
    Flag = False
    return flag,time.time()-delta-TIME_WAIT

def launcherF(dag_file, pre_file):

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
    #post = PostCardProcessor('s1-eth4')
    #post.start()
    PostCardProcessor.Start()
    time.sleep(1)
    #logging.info("1# start to collect %.8f" %time.time())

    #start to generate packets
    from timelog import TimeLog
    TimeLog.GetInstance().reset()

    import parser, IncrFullAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    rule_lists,edge_dicts = parser.DAGLoader(pre_file)

    table = []
    for i in rule_list.keys():
        for j in rule_lists.keys():
            ret = cmp(rule_list[i], rule_lists[j])
            if ret == 0:
                #print rule_list[i]
                #print rule_lists[j]
                table.append(i)
    #print len(table),table

    TimeLog.GetInstance().clock()
    flag = IncrFullAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue, table)
    TimeLog.GetInstance().addTotal()
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()

def launcherG(dag_file, pre_file):
    logging.basicConfig(level=logging.WARNING)

    from timelog import TimeLog
    TimeLog.GetInstance().reset()
    #generate rules and install them on switch 1
    pcg = PostcardGernerator.PostcardGernerator(dag_file)
    pcg.start()

    PostCardProcessor.Start()
    time.sleep(1)

    #start to generate packets

    import parser, IncrSemiAdap
    types = parser.type_parse("typename.txt")
    rule_list,edge_dict = parser.DAGLoader(dag_file);
    rule_lists,edge_dicts = parser.DAGLoader(pre_file)

    table = []
    tbN = []
    hs = {}
    for i in rule_list.keys():
        for j in rule_lists.keys():
            ret = cmp(rule_list[i], rule_lists[j])
            if ret == 0:
                #print rule_list[i]
                #print rule_lists[j]
                table.append(i)
                if not j in tbN:
                    tbN.append(j)
                    hs[j] = i
    #print table
    edges_pre = []
    for i in edge_dicts.keys():
        if not i in tbN:
            continue
        for j in edge_dicts[i]:
            if not j in tbN:
                continue
            edges_pre.append([hs[i], hs[j]])

    TimeLog.GetInstance().clock()
    flag = IncrSemiAdap.packetGenerator(edge_dict, rule_list, types, postCardQueue, table, edges_pre)
    if flag == False:
        print "Failed!",TimeLog.GetInstance().getCost()
    elif flag == True:
        print "Success!",TimeLog.GetInstance().getCost()
    else:
        print "Unexpected!",TimeLog.GetInstance().getCost()
    Flag = False
    time.sleep(0.1)
    return flag,TimeLog.GetInstance().getCost()

if __name__ == "__main__":
    #parse the input arguments
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print "Or Usage: python launcher.py dag_file"
        print "Or Usage: python launcher.py dag_file pre_file"
        exit(0)
    dag_file = sys.argv[1]
    pre_file = ""
    if len(sys.argv) == 3:
        pre_file = sys.argv[2]
    #launcherA(dag_file)
    #launcherAWithWrongTable(dag_file,dag_file+".miss")
    #launcherAWithWrongTable(dag_file,dag_file+".order")
    #launcherB(dag_file)
    #launcherBWithWrongTable(dag_file,dag_file+".miss")
    #launcherBWithWrongTable(dag_file,dag_file+".order")
    #launcherC(dag_file)
    #launcherCWithWrongTable(dag_file,dag_file+".miss")
    #launcherCWithWrongTable(dag_file,dag_file+".order")
    #launcherD(dag_file)
    #launcherDWithWrongTable(dag_file,dag_file+".miss")
    #launcherDWithWrongTable(dag_file,dag_file+".order")
    #launcherDWithWrongTable(dag_file,dag_file+"_8.mix")
    launcherE(dag_file, pre_file)
    #launcherF(dag_file, pre_file)
    #launcherG(dag_file, pre_file)
