import codecs
import sys
from cli import CLI
from main import Main


# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def run():
    cli = CLI()
    (options, args) = cli.parse()

    if options.enable_colors:
        cli.enable_colors()

    try:
        main = Main(cli, options, args)
        if options.print_version:
            main.print_version()
        else:
            main.start()
    except KeyboardInterrupt:
        cli.print_info("\nExecution interrupted by user")
        sys.exit(2)

    sys.exit(0)

if __name__ == '__main__':
    run()
