from pyramid.view import view_config


from ....views.finalisecontext import FinaliseContext

class APIV1(FinaliseContext):
    @view_config(context='...traversal.v1.Root', route_name='api', renderer='json')
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

