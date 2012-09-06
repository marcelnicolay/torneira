# coding: utf-8
from mako.exceptions import TopLevelLookupException
from mako.lookup import TemplateLookup
from tornado.web import HTTPError

from torneira import settings


class MakoMixin(object):
    def render_to_template(self, template_name, **context):
        assert hasattr(settings, 'TEMPLATE_DIRS'), "Missing TEMPLATE_DIRS config"

        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS, input_encoding='utf-8', output_encoding='utf-8', default_filters=['decode.utf8'])
        try:
            template = lookup.get_template(template_name)
        except TopLevelLookupException:
            raise HTTPError(500, "Template %s not found" % template_name)

        return template.render(**context)
