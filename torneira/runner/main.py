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

    def setup_import_path(self):
        filename = os.path.abspath(self.options.settings_file)
        if not os.path.exists(filename):
            self.cli.print_error("Settings file %s not found" % filename)
            return None

        settings_dir = os.path.dirname(filename)
        parent_dir = os.path.abspath(os.path.join(settings_dir, '..'))

        sys.path.insert(0, parent_dir)
        sys.path.insert(0, settings_dir)

    def start(self):
        self.setup_import_path()

        from torneira.core.server import TorneiraServer

        options = self.options
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
