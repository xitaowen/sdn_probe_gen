from ryu.base import app_manager
from ryu.topology import event
from ryu.controller.controller import Datapath
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import ofctl_v1_3
from ryu.ofproto import ofproto_v1_3
from ryu.lib import ofctl_v1_0
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.mac import haddr_to_bin
from ryu.lib.ip import ipv4_to_str
from ryu.lib.ip import ipv4_to_bin
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.topology.switches import Switch
from ryu.topology.api import get_switch
#import re
import json
import array

import threading
import os
import time
import socket
import struct
switchid = 1
class PacketProcessor(threading.Thread):
    def __init__(self,app):
        threading.Thread.__init__(self)
        self.sockname = 'packets'
        self.app = app
    def run(self):	
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        global switchid 
        if os.path.exists(self.sockname):
            os.unlink(self.sockname)
        sock.bind(self.sockname)
        sock.listen(1)
        while True:
            conn,addr = sock.accept()
            data = conn.recv(102400)
            try:
                #print "data:",data
                rule = json.loads(data)
                #print "rule:",rule
                pkt = {}
                for key in rule:
                    pkt[key] = rule[key]
                self.app.sendpkt(switchid, pkt)
            except Exception as e:
                print "Exception!"
                print e
            finally:
                print "%.16f" %time.time()
                print "###############"
            #print data
                conn.close()

class SendPkt(app_manager.RyuApp):
    OFP_VERSIONS = {ofproto_v1_3.OFP_VERSION}

    def __init__(self, *args, **kwargs):
        super(SendPkt, self).__init__(*args, **kwargs)
        self.count = 0
        self.pktReciever = PacketProcessor(self)
        self.pktReciever.start()

    def pkt_out(self, datapath, pkt, port=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt.serialize()
        
        import socket 
         
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
        s.bind(("em2", 0))
        s.send(pkt.data)
        s.close()
        return
        #data = pkt.data
        #data = pkt.data + bytearray(array.array('c', ['5']))
        if self.count < 256:
            data = pkt.data + bytearray([self.count])
        else:
            self.count = 0
            data = pkt.data + bytearray([self.count])
        self.count += 1
        if port != None:
            out_port = port
        else:
            out_port = ofproto.OFPP_FLOOD
        out_port = 1
        actions = [parser.OFPActionOutput(out_port)]
        #print "pkt-out!"
        #print "port:", out_port
        #print "pkt:", data
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions, data=data)
        datapath.send_msg(out)
        print "packet_sent"
        print "%.16f" %time.time()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        global switchid 
        print 'switch entrying'
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        switchid = datapath.id
        print "switch id: ", switchid
        #actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        actions = []
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        # print 'add flow!!!!!!!!!!!!!!!'
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        idle_timeout = 600
        hard_timeout = 10
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    def sendpkt(self, dpid, pkt, port=None):
        print "inside sendpkt"
        tcp_field = ["src-port", "dst-port"]
        ip_field = ["src-ip", "dst-ip"]
        id_field = ["pid"]

        # default value set inside the library file
        srcip = "10.0.0.1"
        dstip = "10.0.0.2"
        srcport = 1
        dstport = 1
        pktid = 0

        for field in pkt:
            if field == tcp_field[0]:
                srcport = pkt[tcp_field[0]]
            if field == tcp_field[1]:
                dstport = pkt[tcp_field[1]]
            if field == ip_field[0]:
                srcip = pkt[ip_field[0]]
            if field == ip_field[1]:
                dstip = pkt[ip_field[1]]
            if field == id_field[0]:
                pktid = pkt[id_field[0]]

        #pkt = packet.Packet(data=array.array('i', [6000]))
        print "srcip:",srcip
        print "srcport:",srcport
        print "dstip:",dstip
        print "dstport:",dstport
        print "pktid:",pktid

        pkt = packet.Packet()
        # src='' dst=''
        pkt.add_protocol(ethernet.ethernet(ethertype=2048))
        # pkt.add_protocol(ethernet.ethernet(ethertype=2048,src='11:22:33:44:55:66',dst='11:22:33:44:55:66'))
        # proto=6  tcp; proto=17  udp
        pkt.add_protocol(ipv4.ipv4(proto=6, src=srcip, dst=dstip))
        #pkt.add_protocol(udp.udp(src_port=srcport,dst_port=dstport))
        pkt.add_protocol(tcp.tcp(src_port=srcport, dst_port=dstport))

        #pkt.add_protocol(data)
        pkt.add_protocol("\x1f\x1f\x1f\x1f")
        #print struct.pack('>H',pktid)
        #print pktid
        pkt.add_protocol(struct.pack('>H',pktid))
        #pkt.add_protocol((pktid&0xff00)>>8)
        #pkt.add_protocol(pktid&0x00ff)
        pkt.serialize()
        import socket 
         
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
        s.bind(("em2", 0))
        s.send(pkt.data)
        s.close()
        return
        #print "packet data:",pkt.data
        #print len(pkt.data)
        datapath = get_switch(self, dpid)[0].dp
        self.pkt_out(datapath, pkt, port)
        print pktid

    # diaoyong
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def pkt_in(self, ev):

        '''
        pkt = {}
        pkt['srcip'] = '10.0.0.1'
        pkt['dstip'] = '10.0.0.2'
        pkt['srcport'] = 1234
        pkt['dstport'] = 2345
        self.sendpkt(1, pkt)
        input_file = open('data_to_injector.txt', 'r')
        line_list = input_file.readlines()

        for line in line_list:
            match = re.search(r"\{'([a-z]+)': (\d)\}", line)
        '''
        print "inside pkt_in"
        #data_file = open('/home/ubuntu/our_apps/probe/data_to_injector.txt', 'r')
        #rule_data = json.load(data_file)

        #for rule in rule_data:
            #print "inside pkt_in for"
            #pkt = {}
            #for key in rule:
                #pkt[key] = rule[key]
            #self.sendpkt(1, pkt)
        #data_file.close()
