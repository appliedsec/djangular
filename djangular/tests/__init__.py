import django

if django.VERSION < (1, 6):
    from djangular.tests.test_base import *
    from djangular.tests.test_finders import *
    from djangular.tests.test_middleware import *
    from djangular.tests.test_storage import *
    from djangular.tests.test_utils import *
