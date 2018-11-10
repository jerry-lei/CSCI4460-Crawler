""" This script is used to test commands on the threaded scheduler class.

The shell created in this allows for arbitrary access to a threaded instance
of the scheduler class in order to test behavior similar to the behavior
that will be seen with API interaction

Documentation: docs.python.org/3/library/cmd.html
"""


import cmd
from scheduler import Scheduler

class Shell(cmd.Cmd):
    """Cmd shell that handles user input and passes it to our scheduler instance."""
    intro = '=== (SCHEDULER SHELL) ==='
    prompt = ''


    # Instantiates the scheduler objects, and begins running the main thread loop
    scheduler = Scheduler(5)
    scheduler.start()

    def do_addhp(self, arg):
        """Adds a list of links to the scheduler to handle
        Usage: $ addhp <link1> <link2>...
        """
        vals = arg.split(' ')
        self.scheduler.dump_hp_links(vals)

    def do_showhp(self, arg):
        """Shows the lists of links that the crawler has already processed
        Usage: $ showhp
        """
        self.scheduler.print_crawled_hp()

    def do_EOF(self, line):
        """Ignore EOF values; likely caused by lack of stdin."""
        return True

    def do_exit(self, arg):
        """Ends the main loop in the scheduler thread by changing an exit flag.
           Exits out of 'this' process
        Usage: $ exit
        """
        self.scheduler.set_exit(True)
        exit()

    def do_sanity(self, arg):
        """Sanity check to ensure that the CLI is actually running"""
        print("(CHECKED)")


if __name__ == '__main__':
    MY_SHELL = Shell()
    MY_SHELL.cmdloop()
