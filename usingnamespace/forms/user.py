import colander
import deform

from csrf import CSRFSchema

class LoginForm(CSRFSchema):
    """The user login form."""
    username = colander.SchemaNode(colander.String(),
            title="Username",
            widget=deform.widget.TextInputWidget(css_class='form-control'),
            )
    password = colander.SchemaNode(colander.String(),
            title="Password",
            validator=colander.Length(min=5),
            widget=deform.widget.PasswordWidget(size=20,
                css_class='form-control'),
            )

