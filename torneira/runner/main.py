import torneira
import traceback

from cli import CLI
import os
import sys

class Main(object):

    def __init__(self):
        self.cli = CLI()
    
    def start(self, options, args):
        
        # set path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(options.settings_file)), ".."))
        sys.path.insert(0, os.path.dirname(os.path.abspath(options.settings_file)))
        
        # set setting
        exec("import %s as settings" % os.path.splitext(os.path.basename(options.settings_file))[0])
        torneira.settings = settings  

        from torneira.core.server import TorneiraServer
        server = TorneiraServer(
            pidfile=options.pidfile, 
            port=options.port, 
            media_dir=os.path.abspath(options.media_dir), 
            xheaders=options.xheaders
        )
        
        if options.daemon:
            if args[0] == "start":
                server.start()

            elif args[0] == "stop":
                server.stop()

            elif args[0] == "restart":
                server.restart()
        else:
            server.run()
            
    def excecute(self):
        
        (options, args) = self.cli.parse()
        
        if args and args[0] in ('start', 'stop', 'restart'):
            try:
                self.start(options, args)
            except Exception, e:
                traceback.print_exc(file=sys.stderr)
