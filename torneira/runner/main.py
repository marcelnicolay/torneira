# coding: utf-8
from __future__ import with_statement

import daemon
import os
import sys
import traceback
from cli import CLI

import lockfile
import tornado
import torneira


class Main(object):
    def __init__(self, cli, options, args):
        self.options = options
        self.args = args
        self.cli = cli

    def start(self):
        options = self.options
        # set path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(options.settings_file)), ".."))
        sys.path.insert(0, os.path.dirname(os.path.abspath(options.settings_file)))

        # set setting
        exec("import %s as settings" % os.path.splitext(os.path.basename(options.settings_file))[0])
        torneira.settings = settings  

        from torneira.core.server import TorneiraServer
        server = TorneiraServer(
            port=options.port,
            media_dir=os.path.abspath(options.media_dir),
            xheaders=options.xheaders
        )

        if options.daemon:
            pidfile = '%s.%s' % (options.pidfile, options.port)
            lock = lockfile.FileLock(pidfile)
            if lock.is_locked():
                sys.stderr.write("torneira already running on port %s\n" % options.port)
                return

            context = daemon.DaemonContext(pidfile=lock)
            with context:
                server.run()
        else:
            server.run()

    def print_version(self):
        msg = 'torneira v%s' % torneira.__version__
        self.cli.print_msg(msg)
