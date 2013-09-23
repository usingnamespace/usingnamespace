import colander
import deform

from schemaform import SchemaFormMixin
from csrf import CSRFSchema

class LoginForm(CSRFSchema, SchemaFormMixin):
    """The user login form."""
    username = colander.SchemaNode(colander.String(),
            title="Username",

    __buttons__ = (deform.form.Button(name=_("Submit"), css_class='btn btn-primary'),)
            widget=deform.widget.TextInputWidget(css_class='form-control'),
            )
    password = colander.SchemaNode(colander.String(),
            title="Password",
            validator=colander.Length(min=5),
            widget=deform.widget.PasswordWidget(size=20,
                css_class='form-control'),
            )

