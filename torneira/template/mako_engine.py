# coding: utf-8
from mako.exceptions import TopLevelLookupException, html_error_template
from mako.lookup import TemplateLookup
from tornado.web import HTTPError

from torneira import settings


class MakoMixin(object):

    def render_to_template(self, template_name, **context):
        assert hasattr(settings, 'TEMPLATE_DIRS'), "Missing TEMPLATE_DIRS config"

        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS,
            input_encoding='utf-8', output_encoding='utf-8',
            default_filters=['decode.utf8'])

        try:
            template = lookup.get_template(template_name)
        except TopLevelLookupException:
            raise HTTPError(500, "Template %s not found" % template_name)

        context.update({
            'settings': settings,
            'url_for': self.reverse_url
        })

        return template.render(**context)

    def output_errors(self, status_code, **kwargs):
        self.write(html_error_template().render())
