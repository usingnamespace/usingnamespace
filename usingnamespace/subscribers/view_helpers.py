import logging
log = logging.getLogger(__name__)

from pyramid.events import BeforeRender
from pyramid.events import subscriber

from ..views.helpers import URLHelper

@subscriber(BeforeRender)
def view_helpers(event):
    if "h" in event:
        log.error('Another helper may have already been registered!')
        return

    h = {}
    h['url'] = URLHelper(event['req'])

    event['h'] = h


