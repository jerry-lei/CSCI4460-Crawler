""" scheduler.py stores a threaded scheduler class which manages
    threaded instances of crawlers
"""

from multiprocessing import Queue
import concurrent.futures
import threading

from .crawler import crawl_link



class Scheduler(threading.Thread):
    """Scheduler manages the crawlers and sending links received by properly
       handing them off to the individual crawlers


    Usage: Instantiate a Scheduler object with an integer parameter setting
           the max number of crawler threads, then start the main scheduler
           loop. To access scheduler/function, make calls directly to its
           functions.
    e.g.
     `
       scheduler = Scheduler(15) #instantiate Scheduler object
       scheduler.start() #starts the main loop
       #add links to the queue to process
       scheduler.dump_hp_links(["https://google.com", "https://apple.com"])
     `
    """
    #n: number of set crawlers
    def __init__(self, n):
        """ Initializes an instance of scheduler. Begins with calling the super
            class init (threading.Thread)

        Input:
            int -- The number of crawlers to initialize the scheduler with

        Returns:
            void
        """
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
        """ Sets the exit flag to end the main loop

        Input:
            bool -- value to set the exit flag

        Returns:
            void
        """
        self.exit = value



    def print_crawled_hp(self):
        """ Debugging function: prints high priority queue """
        print("Crawled high_priority: " + str(self.crawled_hp))


    def print_crawled_lp(self):
        """ Debugging function: prints low priority queue """
        print("Crawled low_priority: " + str(self.crawled_lp))


    def dump_hp_links(self, links):
        """ Adds a list of high priority links to the queue

        NOTE: This blocks the function caller until all input links are
              finished processing.

        Inputs:
            [List] -- list of URL strings

        Returns:
            {Key:Value} --
                Key: URL string
                Value: urllib response object
        """
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
            if exists_flag is False:
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
        """ Adds a list of low priority links to the queue

        NOTE: This blocks the function caller until all input links are
              finished processing.

        Inputs:
            [List] -- list of URL strings

        Returns:
            {Key:Value} --
                Key: URL string
                Value: urllib response object
        """
        for link in links:
            self.lp_queue.put(link)
            #print("Added link to hp_queue: " + link)
        result = {}
        # block until all links are added into the crawled_lp dictionary
        while True:
            exists_flag = False
            for link in links:
                if link not in self.crawled_lp:
                    exists_flag = True
            if exists_flag is False:
                break
        # block until all items are finished processing.
        for items in self.crawled_lp.items():
            while items[1].running():
                continue
            result[items[0]] = items[1].result()
        self.crawled_lp.clear()
        return result

    #main thread loop
    def run(self):
        """ Main threaded loop, pops off high priority queue and hands the links
            off to the ThreadPoolExecutor to handle threaded crawling. Only if
            the high priority queue is empty does links from the low priority
            queue get processed.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_crawlers) as executor:
            while True:
                if self.exit is True:
                    break
                #Note: Queue.empty() does not guarentee that the queue is empty
                #        because this is a multithreaded implementation of queue.
                #        This is not a concern in our implementation, because we
                #        only have a single process (this one) accessing the queue.
                if not self.hp_queue.empty():
                    #print("Removed link from hp_queue: " + self.hp_queue.get())
                    link = self.hp_queue.get()
                    self.crawled_hp[link] = executor.submit(crawl_link, link)
                else:
                    if not self.lp_queue.empty():
                        #print("Removed link from lp_queue: " + self.lp_queue.get())
                        link = self.lp_queue.get()
                        self.crawled_lp[link] = executor.submit(crawl_link, link)


# Tests for functions in scheduler.py
if __name__ == "__main__":
    k = Scheduler(15)
    k.start()
    k.dump_hp_links(["b", "a"])
