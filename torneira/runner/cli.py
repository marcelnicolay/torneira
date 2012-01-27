from optparse import OptionParser
import sys

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

    @staticmethod
    def show_colors():
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
        self.__parser = OptionParser(usage="usage: %prog [options] start")

        self.__parser.add_option("-s", "--settings",
                dest="settings_file",
                default="settings_local.py",
                help="Use a specific settings file. If not provided, will search for 'settings_local.py' in the current directory.")

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
                default=8080,
                type=int,
                help="Use a specific port number. (default is 8080)")

        self.__parser.add_option("--pidfile",
                dest="pidfile",
                default="/tmp/torneira.pid",
                help="Use a specific pidfile. If not provide, will create /tmp/torneira.pid")

        self.__parser.add_option("-v", "--version",
                action="store_true",
                dest="torneira_version",
                default=False,
                help="Displays torneira version and exit.")

        self.__parser.add_option("--color",
                action="store_true",
                dest="show_colors",
                default=False,
                help="Output with beautiful colors.")

    def get_parser(self):
        return self.__parser

    def parse(self):
        return self.__parser.parse_args()

    def error_and_exit(self, msg):
        self.msg("[ERROR] %s\n" % msg, "RED")
        sys.exit(1)

    def info_and_exit(self, msg):
        self.msg("%s\n" % msg, "BLUE")
        sys.exit(0)

    def msg(self, msg, color="CYAN"):
        print "%s%s%s" % (self.color[color], msg, self.color["END"])