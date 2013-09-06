# File: FinaliseContext.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-09-05

from pyramid.httpexceptions import HTTPNotFound

class FinaliseContext(object):

    """FinaliseContext

    This will attempt to finalise the context, this generally means the context
    actually verifies that the path it is trying to reach is valid.
    """

    def __init__(self, context, request):
        """Set's up the object, if the context has an function named finalise()
        it will call it first, and if that raises a ValueError this function
        will raise an HTTPException

        :request: A Pyramid request object
        :context: The context found after traversing the tree

        """

        finalise = getattr(context, "finalise", None)
        if callable(finalise):
            try:
                finalise()
            except ValueError:
                raise HTTPNotFound()

        self.context = context
        self.request = request

