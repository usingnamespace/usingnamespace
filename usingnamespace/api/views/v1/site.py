from pyramid.view import (
        view_config,
        view_defaults,
        )

@view_defaults(context='...traversal.v1.Site',
        route_name='api',
        renderer='json',
        )
class Site:
    @view_config()
    def main(self):
        cur_site = self.context.site

        return {
                'id': str(cur_site.id),
                'title': cur_site.title,
                'tagline': cur_site.tagline,
                'domains': [{'domain': x.domain, 'default': x.default} for x in cur_site.domains],
                }
