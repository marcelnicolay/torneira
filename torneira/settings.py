try:
    import settings_local as settings
    logging.debug("Using settings_local.py as settings")
except ImportError, ie:
    try:
        import settings
    except ImportError, ie:
        logging.warn("Not found settings_local.py or settings.py file, using settings default!")
        from torneira.core import settings_default as settings

DEBUG = True
PROFILING = False

# make this unique and secret
COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"
        
settings = settings
