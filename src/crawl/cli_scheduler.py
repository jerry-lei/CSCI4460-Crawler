import cmd
from scheduler import Scheduler


# Calendar shell, to be created in a separate thread from our main site
# Documentation used: docs.python.org/3/library/cmd.html

class Shell(cmd.Cmd):
    """Cmd shell that handles user input and passes it to our site."""
    intro = '===SCHEDULER SHELL==='
    prompt = ''


    scheduler = Scheduler(5)
    scheduler.start()

    """Adds a list of links to the scheduler to handle
        Usage: addhp <link1> <link2>...
    """
    def do_addhp(self, arg):
        vals = arg.split(' ')
        self.scheduler.dump_hp_links(vals)

    def do_EOF(self, line):
        """Ignore EOF values; likely caused by lack of stdin."""
        return True


if __name__ == '__main__':
    MY_SHELL = Shell()
    MY_SHELL.cmdloop()
