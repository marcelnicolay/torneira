from getpass import getpass
import codecs
import sys
import torneira

from cli import CLI
from main import Main

# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def run():
    cli = CLI()
    try:
        (options, args) = cli.parse()

        if options.torneira_version:
            msg = 'torneira v%s' % torneira.__version__
            cli.info_and_exit(msg)

        if options.show_colors:
            CLI.show_colors()
            
        Main().excecute()
            
    except KeyboardInterrupt:
        cli.info_and_exit("\nExecution interrupted by user...")
    except Exception, e:
        cli.error_and_exit(str(e))

if __name__ == '__main__':
    run()