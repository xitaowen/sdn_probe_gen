
import socket
import time
import json
if __name__ == '__main__':
    fname = "packets"
    data = {'tcpDstPort': 2}
    for i in range(0,10000):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(fname)
        print json.dumps(data)
        print "%.16f" % time.time()
        sock.send(json.dumps(data))
        #print sock.recv(1024)
        sock.close()
