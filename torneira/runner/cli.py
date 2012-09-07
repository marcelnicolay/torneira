import sys
from optparse import OptionParser


class CLI(object):

    color = {
        "PINK": "",
        "BLUE": "",
        "CYAN": "",
        "GREEN": "",
        "YELLOW": "",
        "RED": "",
        "END": "",
    }

    def enable_colors(self):
        CLI.color = {
            "PINK": "\033[35m",
            "BLUE": "\033[34m",
            "CYAN": "\033[36m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "RED": "\033[31m",
            "END": "\033[0m",
        }

    def __init__(self):
        self.__config_parser()

    def __config_parser(self):
        self.__parser = OptionParser(usage="usage: %prog [options]")

        self.__parser.add_option("-s", "--settings",
                dest="settings_file",
                default="settings.py",
                help="Use a specific settings file. If not provided, will search for 'settings.py' in the current directory.")

        self.__parser.add_option("-d", "--daemon",
                dest="daemon",
                default=False,
                action="store_true",
                help="Run torneira server as an daemon. (default is false)")

        self.__parser.add_option("-m", "--media", "--media_dir",
                dest="media_dir",
                default="media",
                help="User a specific media dir. If not provided, will search for media dir in the current directory")

        self.__parser.add_option("-x", "--xheaders",
                dest="xheaders",
                default=False,
                action="store_true",
                help="Turn extra headers parse on in tornado server. (default is false)")

        self.__parser.add_option("-p", "--port",
                dest="port",
                default=8888,
                type=int,
                help="Use a specific port number (default is 8888).")

        self.__parser.add_option("--pidfile",
                dest="pidfile",
                default="/tmp/torneira.pid",
                help="Use a specific pidfile. If not provide, will create /tmp/torneira.pid")

        self.__parser.add_option("-v", "--version",
                action="store_true",
                dest="print_version",
                default=False,
                help="Displays tornado and torneira version and exit.")

        self.__parser.add_option("--colors",
                action="store_true",
                dest="enable_colors",
                default=False,
                help="Output with beautiful colors.")

    def parse(self):
        return self.__parser.parse_args()

    def print_error(self, msg):
        self.print_msg(msg, "RED", out=sys.stderr)
        sys.exit(1)

    def print_info(self, msg):
        self.print_msg(msg, "BLUE")
        sys.exit(0)

    def print_msg(self, msg, color='END', out=None):
        if not out:
            out = sys.stdout
        out.write("%s%s%s\n" % (self.color[color], msg, self.color["END"]))
