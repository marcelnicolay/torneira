import os
from functools import partial


ROOT_URLS = 'more_complex_app.urls'
DEBUG = True

join = partial(os.path.join, os.path.dirname(__file__))

TEMPLATE_DIRS = (
    join('templates'),
)
