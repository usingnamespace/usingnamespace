from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('usingnamespace')

import colander
import deform

from ...forms.schemaform import SchemaFormMixin
from ...forms.csrf import CSRFSchema

class APIForm(CSRFSchema, SchemaFormMixin):
    __buttons__ = (deform.form.Button(name=_("Create New API Ticket"),),)

