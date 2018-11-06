# Scheduler/Crawler -- Jerry


## Implementation:
#### Modules utilized:
- multiprocessing queue
- threading
- concurrent.futures ThreadPoolExecutor
- cmd

#### Details:
All interactions from other components of the crawler should only go to _scheduler.py_. This file holds the Scheduler class, which is initialized with a parameter indicating the maximum number of crawlers the scheduler will allow. This class holds the queues for high priority, and low priority links. Adding to these queues can be done using the _dump_hp_links_ and _dump_lp_links_ with a list of links as a parameter. To begin processing links (until the process exits), begin the instantiated scheduler's main loop function by calling: _Scheduler.start()_. This main loop will indefinitely check for links that are/have been added to the queues, prioritizing the links in the high priority queue. The instance of _ThreadPoolExecutor_ handles the crawler thread creation and execution of link creation. Submitting a link to the _ThreadPoolExecutor_ results in a _Future_ object with the thread return value. That return value is added to a dictionary located in the scheduler class with the key being the link.

## Testing:
Testing has been manually completed using Python's built in cmd module. This module gives easy access to the running scheduler thread (similar to the way it is going to be run in our main system) by using a command-line interface to hook into commands to the scheduler thread.
```sh
$ python cli_scheduler.py
```
#### Helpful command line functions:
Adding to the high priority queue:
```
addhp <link 1> <link 2> <link 3> ....
```
Showing the high priority queue:
```
showhp
```
