# -*- coding:utf-8 -*-

import threading

cv = threading.Condition()

class test(threading.Thread):
    
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        for i in range(10):
            cv.acquire()
            print str(self.num) + ":test:" + str(i)
            cv.release()

if __name__ == "__main__":
    t1 = test(1)
    t1.start()
    t2 = test(2)
    t2.start()
    t3 = test(3)
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print "end."
