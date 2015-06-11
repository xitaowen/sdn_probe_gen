import threading
import time

class TimeLog():
    instance = None
    mutex = threading.Lock()
    def __init__(self):
        self.calc = 0
        self.solver = 0
        self.send = 0
        self.total = 0
        self.last = 0

    @staticmethod
    def GetInstance():
        if TimeLog.instance == None:
            TimeLog.mutex.acquire()
            if TimeLog.instance == None:
                TimeLog.instance = TimeLog()
            else:
                pass
            TimeLog.mutex.release()
        else:
            pass
        return TimeLog.instance
    
    def reset(self):
        self.calc = 0
        self.solver = 0
        self.send = 0
        self.total = 0
        self.last = time.time()

    def clock(self):
        self.last = time.time()

    def add(self):
        self.time += time.time()-self.last
        self.last = time.time()

    def addCalc(self):
        self.calc += time.time()-self.last
        self.last = time.time()
    def addSolver(self):
        self.solver += time.time()-self.last
        self.last = time.time()
    def addSend(self):
        self.send += time.time()-self.last
        self.last = time.time()
    def addTotal(self):
        self.total += time.time()-self.last
        self.last = time.time()

    def getCost(self):
        ret = {}
        self.total += self.calc+self.solver+self.send
        ret['calc'] = self.calc
        ret['solver'] = self.solver
        ret['send'] = self.send
        ret['total'] = self.total
        return ret
