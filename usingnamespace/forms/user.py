from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('usingnamespace')

import colander
import deform

from .schemaform import SchemaFormMixin
from .csrf import CSRFSchema

from ..models import User

@colander.deferred
def login_username_password(node, kw):
    request = kw.get('request')

    if request is None:
        raise KeyError('Require bind: request')

    def username_password(form, value):
        user = User.validate_user_password(value['email'],
                value['password'])

        if user is None:
            exc = colander.Invalid(form, _("Username or password is incorrect"))
            exc['email'] = ''
            exc['password'] = ''
            raise exc

    return username_password

class LoginForm(CSRFSchema, SchemaFormMixin):
    """The user login form."""

    __buttons__ = (deform.form.Button(name=_("Submit"),),)
    __validator__ = login_username_password

    email = colander.SchemaNode(colander.String(),
            title=_("Email Address"),
            widget=deform.widget.TextInputWidget(),
            )
    password = colander.SchemaNode(colander.String(),
            title=_("Password"),
            validator=colander.Length(min=4),
            widget=deform.widget.PasswordWidget(size=20),
            )

