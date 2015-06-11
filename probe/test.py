
import pcap
import sys
import string
import time
import socket
import struct


import threading
import Queue

from PostCardProcessor import PostCardProcessor
from PostCardProcessor import *

if __name__ == "__main__":
    post = PostCardProcessor('s1-eth4')
    post.start()
    print postCardQueue.get()
    print postCardQueue.qsize()
    time.sleep(1)
