from multiprocessing import Queue
import concurrent.futures
import threading

from .crawler import *

"""
Notes to self:
- look at threading pool to handle crawler threads
--- https://www.codementor.io/lance/simple-parallelism-in-python-du107klle
--- package initializes handles the entire scheduler algo, but new links
    cannot be added to the pool after it has initialized
"""

"""
Usage: Instantiate a Scheduler object with an integer parameter setting
       the max number of crawler threads, then start the main scheduler
       loop. To access scheduler/function, make calls directly to its
       functions.
e.g.
 `
   scheduler = Scheduler(15) #instantiate Scheduler object
   scheduler.start() #starts the main loop
   scheduler.dump_hp_links(["https://google.com", "https://apple.com"]) #add links to the queue to process
 `
"""
class Scheduler(threading.Thread):

    #n: number of set crawlers
    def __init__(self, n):
        super(Scheduler, self).__init__()
        self.hp_queue = Queue()
        self.lp_queue = Queue()
        self.max_crawlers = n
        # Too receive schedule links, return [link].result()
        #    stores link as key, and 'future' object as value
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
        result = {}
        # block until all links are added into the crawled_hp dictionary
        while True:
            exists_flag = False
            for link in links:
                if link not in self.crawled_hp:
                    exists_flag = True
            if exists_flag == False:
                break
        # block until all items are finished processing.
        for items in self.crawled_hp.items():
            while items[1].running():
                continue
            result[items[0]] = items[1].result()
        self.crawled_hp.clear()
        return result



    #dump a list of low-priority links
    def dump_lp_links(self, links):
        for link in links:
            self.lp_queue.put(link)
            #print("Added link to lp_queue: " + link)

    #main thread loop
    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_crawlers) as executor:
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
                    self.crawled_hp[link] = executor.submit(crawl_link, link)
                else:
                    if(not self.lp_queue.empty()):
                        #print("Removed link from lp_queue: " + self.lp_queue.get())
                        link = self.lp_queue.get()
                        self.crawled_lp[link] = executor.submit(crawl_link, link)


# Tests for functions in scheduler.py
if __name__ == "__main__":
    k = Scheduler(15)
    k.start()
    k.dump_hp_links(["b", "a"])
