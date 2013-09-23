# File: csrf.py
# Author: Bert JW Regeer <bertjw@regeer.org>
# Created: 2013-01-26

import logging
log = logging.getLogger(__name__)

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('usingnamespace')

import colander
import deform

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')

    if request is None:
        raise KeyError('Require bind: request')

    csrf_token = request.session.get_csrf_token()
    return csrf_token

@colander.deferred
def deferred_csrf_validator(node, kw):
    request = kw.get('request')

    if request is None:
        raise KeyError('Require bind: request')

    def validate_csrf(node, value):
        csrf_token = request.session.get_csrf_token()
        if value != csrf_token:
            log.error('CSRF Failed: expected "{}" got "{}"'.format(csrf_token,
                value))
            exc = colander.Invalid(node, _('Invalid cross-site scripting token. Please submit your form again.'))
            raise exc
    return validate_csrf

class CSRFSchema(colander.Schema):
    csrf_token = colander.SchemaNode(
            colander.String(),
            default=deferred_csrf_default,
            validator=deferred_csrf_validator,
            widget=deform.widget.HiddenWidget()
            )

