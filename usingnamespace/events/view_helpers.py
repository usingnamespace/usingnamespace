from ..views.helpers import URLHelper


def view_helpers(event):
    if "h" in event:
        print "Someone else got here before us ..."
        return

    h = {}
    h['url'] = URLHelper(event['req'])

    event['h'] = h

