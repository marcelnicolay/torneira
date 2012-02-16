import logging, os

DEBUG = True
PROFILING = False

DATABASE_ENGINE = "mysql://root:@localhost:3306/demo?charset=utf8&use_unicode=0"
DATABASE_POOL_SIZE = 50

logging.basicConfig(
    level = logging.DEBUG,
)

ROOT_URLS = 'demo.urls'

COOKIE_SECRET = ""

TEMPLATE_DIRS = (
    "%s/templates" % os.path.abspath(os.path.dirname(__file__))
)