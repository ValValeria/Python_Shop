from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment
import os


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static':   os.path.join(BASE_DIR, "static"),
        'url': reverse,
    })
    return env