
import pcap
import sys
import string
import time
import socket
import struct


import threading
import Queue
postCardQueue = Queue.Queue()
Flag = True

class PostCardProcessor(threading.Thread):
    #start from function run.
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name
        self.dev = name
        #make sure thread to exit while its father thread quit.
        self.setDaemon(True)

    def run(self):
        global Flag
        Flag = True
        p = pcap.pcapObject()
        dev = self.dev
        #net, mask = pcap.lookupnet(dev)
        #print net,mask
        p.open_live(dev, 1600, 0, 100)
        p.setfilter('mpls', 0, 0)

        try:
            while Flag:
                p.dispatch(1, self.filter_packet)
                isReady = True
        except KeyboardInterrupt:
            print '%s' % sys.exc_type
            print 'shutting down'
            print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()

    def decode_ip_packet(self,s):
        #decode ip packet
        d={}
        d['version']=(ord(s[0]) & 0xf0) >> 4
        d['header_len']=ord(s[0]) & 0x0f
        d['tos']=ord(s[1])
        d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
        d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
        d['flags']=(ord(s[6]) & 0xe0) >> 5
        d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
        d['ttl']=ord(s[8])
        d['protocol']=ord(s[9])
        d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
        d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
        d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
        if d['header_len']>5:
            d['options']=s[20:4*(d['header_len']-5)]
        else:
            d['options']=None
        d['data']=s[4*d['header_len']:]

        #parse packetid and rule id
        d['ruleid'] = 0

        if d['total_len'] - d['header_len'] < 6:
            d['usertype'] = 0
            d['packetid'] = 0
            return d
        ed = d['total_len']
        #ed = len(s) + 1
        st = ed - 2
        #print d['total_len'],d['header_len'],ed
        d['packetid']=socket.ntohs(struct.unpack('H',s[st:ed])[0])

        ed = st
        st = ed - 4
        d['usertype']=socket.ntohl(struct.unpack('I',s[st:ed])[0])
        return d

    def decode_mpls_packet(self,s):
        #decode mpls packet.
        d = self.decode_ip_packet(s[4:])
        d['ruleid'] = socket.ntohl(struct.unpack('I',s[0:4])[0])>>12
        #d['ruleid'] = struct.unpack('I',s[0:4])[0]>>12
        return d

    def sendToLauncher(self,pid,rid):
        #print "put post card into shared queue:",pid,rid
        postCardQueue.put((pid,rid))

    def filter_packet(self,pktlen, data, timestamp):
        if not data:
            return
        if data[12:14] == '\x88\x47':
            decoded = self.decode_mpls_packet(data[14:])
            #print "usertype:",decoded['usertype']
            #print "ruleid:",decoded['ruleid']
            #if decoded['usertype'] == '\x1f\x1f\x1f\x1f':
            if decoded['usertype'] == 0x1f1f1f1f:
            #if decoded['usertype'] == 3369445979:
                #a test packet found.
                self.sendToLauncher(decoded['packetid'],decoded['ruleid'])
        elif data[12:14] == '\x08\x00':
            decoded = self.decode_ip_packet(data[14:])
            #print "usertype:",decoded['usertype']
            #print "ruleid:",decoded['ruleid']

if __name__ == "__main__":
    post = PostCardProcessor('s1-eth4')
    post.start()
    print postCardQueue.get()
    print postCardQueue.qsize()
    time.sleep(100)
