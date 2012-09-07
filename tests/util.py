## copied from tornado source code:

import sys

# Encapsulate the choice of unittest or unittest2 here.
# To be used as 'from tests.util import unittest'.
if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest
