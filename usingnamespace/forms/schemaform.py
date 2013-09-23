from deform import Form

class SchemaFormMixin(object):
    @classmethod
    def create_form(cls, *arg, **kw):
        schema_vars = {}
        form_vars = {}

        for sn in ['validator', 'preparer', 'after_bind']:
            if sn in kw:
                schema_vars[sn] = kw[sn]
                del kw[sn]

        for fv in ['action', 'buttons', 'method', 'formid', 'autocomplete',
                'use_ajax', 'ajax_options']:
            if fv in kw:
                form_vars[fv] = kw[fv]
                del kw[fv]

        if 'validator' not in schema_vars and hasattr(cls, '__validator__'):
            schema_vars['validator'] = cls.__validator__

        if 'buttons' not in form_vars and hasattr(cls, '__buttons__'):
            form_vars['buttons'] = cls.__buttons__
        
        schema = cls(**schema_vars).bind(**kw)
        form = Form(schema, **form_vars)

        return (schema, form)

