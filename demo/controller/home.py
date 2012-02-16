# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController
from torneira import __version__

class HomeController(BaseController):
    
    def index(self, request_handler):
        
        return self.render_to_template("home.html", version=__version__)