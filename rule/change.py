#!/usr/bin/python
import sys
import os
import re
import copy

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage:"
        sys.exit(1)

    cb = open(sys.argv[1],"r")
    ft = open(sys.argv[2],"w")
    content = cb.readlines()
    ft.write("[")
    for rule in content:
        counts = 0
        flow = {}
        item = rule.split("\t")
        #source address
        ipSrc = item[0]
        ipSrc = ipSrc[1:]
        tmp = ipSrc.split("/")
        if tmp[1] == "0":
            ipSrc = -1
        #destination address
        ipDst = item[1]
        tmp = ipDst.split("/")
        if tmp[1] == "0":
            ipDst = -1
        #src port
        tcpSrcPort = item[2]
        srcport = tcpSrcPort.split(":")
        if srcport[0] == srcport[1]:
            tcpSrcPort = srcport[0]
        elif int(srcport[0]) == 0 and int(srcport[1]) == 65535:
            tcpSrcPort = -1
        else:
            tcpSrcPort = srcport[0]
        #dst port
        tcpDstPort = item[3]
        dstport = tcpDstPort.split(":")
        if dstport[0] == dstport[1]:
            tcpDstPort = dstport[0]
        elif int(dstport[0]) == 0 and int(dstport[1]) == 65535:
            tcpDstPort = -1
        else:
            tcpDstPort = dstport[0]
        #add to flow together
        ft.write("{pattern={")
        if tcpSrcPort != -1:
            if counts > 0:
                ft.write(",")
            counts += 1
            ft.write("tcpSrcPort=")
            ft.write(tcpSrcPort)
        if tcpDstPort != -1:
            if counts > 0:
                ft.write(",")
            counts += 1
            ft.write("tcpDstPort=")
            ft.write(tcpDstPort)
        if ipSrc != -1:
            if counts > 0:
                ft.write(",")
            counts += 1
            ft.write("ipSrc=")
            ft.write(ipSrc)
        if ipDst != -1:
            if counts > 0:
                ft.write(",")
            counts += 1
            ft.write("ipDst=")
            ft.write(ipDst)
        ft.write("},action=OutputPort()}")
        ft.write("\n")
    ft.write("]")
    ft.close()
    cb.close()

    ft = open(sys.argv[2],"r")
    content = ft.readlines()
    ft.close()
    content = content[1:]
    hh = {}
    for i in range(0,len(content)-1):
        con = content[i]
        hh[con] = 1
    ft = open(sys.argv[2],"w")
    ft.write("[")
    for con in hh.keys():
        #print con,
        ft.write(con)
        #ft.write("\n")
    ft.write("]")
    ft.close()

