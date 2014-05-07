from pyramid.view import (
        view_config,
        view_defaults,
        )

from ....views.finalisecontext import FinaliseContext

@view_defaults(context='...traversal.v1.Root',
        route_name='api',
        effective_principals='system.Authenticated',
        renderer='json',
        )
class APIV1(FinaliseContext):
    @view_config()
    def main(self):
        sites = []
        for site in self.context.sites:
            sites.append(
                        {
                            'id': site.id,
                            'title': site.title,
                            'tagline': site.tagline,
                        }
                    )
        return {
                'sites': sites,
                }

