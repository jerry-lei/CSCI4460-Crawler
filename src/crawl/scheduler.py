from multiprocessing import Queue
import threading

from crawler import *


class Scheduler(threading.Thread):

    #n: number of set crawlers
    def __init__(self, n):
        super(Scheduler, self).__init__()
        self.hp_queue = Queue()
        self.lp_queue = Queue()
        self.crawlers = []
        self.crawled_hp = {}
        self.crawled_lp = {}

        #FOR THE CLI EXIT
        self.exit = False

    #FOR THE CLI EXIT
    def set_exit(self, value):
        self.exit = value


    def print_crawled_hp(self):
        print("Crawled high_priority: " + str(self.crawled_hp))


    def print_crawled_lp(self):
        print("Crawled low_priority: " + str(self.crawled_lp))

    #dump a list of high-priority links
    def dump_hp_links(self, links):
        for link in links:
            self.hp_queue.put(link)
            #print("Added link to hp_queue: " + link)

    #dump a list of low-priority links
    def dump_lp_links(self, links):
        for link in links:
            self.lp_queue.put(link)
            #print("Added link to lp_queue: " + link)

    #main thread loop
    def run(self):
        while(True):
            if self.exit == True:
                break;
            #Note: Queue.empty() does not guarentee that the queue is empty
            #        because this is a multithreaded implementation of queue.
            #        This is not a concern in our implementation, because we
            #        only have a single process (this one) accessing the queue.
            if(not self.hp_queue.empty()):
                #print("Removed link from hp_queue: " + self.hp_queue.get())
                link = self.hp_queue.get()
                self.crawled_hp[link] = crawl_link(link)
            else:
                if(not self.lp_queue.empty()):
                    #print("Removed link from lp_queue: " + self.lp_queue.get())
                    link = self.lp_queue.get()
                    self.crawled_lp[link] = crawl_link(link)


# Tests for functions in scheduler.py
if __name__ == "__main__":
    k = Scheduler(15)
    k.start()
    k.dump_hp_links(["b", "a"])
