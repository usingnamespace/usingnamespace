<%inherit file="site.mako" />

<%block name="body_content">
<div class="container">
    <div class="form-signin">
        <h1>Authenticate</h1>
        ${form|n}
    </div>
</div>
</%block>

<%block name="title">Authenticate - ${parent.title()}</%block>

<%block name="stylesheets">${parent.stylesheets()}
<style type="text/css">
    body {
        padding-top: 40px;
        padding-bottom: 40px;
        background-color: #f5f5f5;
    }

    .form-signin {
        max-width: 600px;
        padding: 19px 29px 29px;
        margin: 0 auto 20px;
        background-color: #fff;
        border: 1px solid #e5e5e5;
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        border-radius: 5px;
        -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.05);
        -moz-box-shadow: 0 1px 2px rgba(0,0,0,.05);
        box-shadow: 0 1px 2px rgba(0,0,0,.05);
    }

    .form-signin h1 {
        text-align: center;
        padding-bottom: 20px;
    }

    .form-signin input[type="text"],
    .form-signin input[type="password"] {
        width: auto;
        margin-left: 180px;
        font-size: 16px;
        padding: 7px 9px;
    }
    
    .field label {
        float: left;
        width: 160px;
        padding-top: 5px;
        text-align: right;
        display: block;
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: normal;
        line-height: 20px;
    }

    .form-signin ul {
        list-style: none;
    }

    .form-signin .req {
        display: none;
    }

    .form-signin li.buttons {
        display: block;
        padding-left: 180px;
        margin-top: 20px;
        margin-bottom: 20px;
        border-top: 1px solid #e5e5e5;
        padding-top: 5px;
    }

    .error .form-control,
    .error .desc {
        color: #b94a48;
    }

    .error .form-control {
        border-color: #b94a48;
        -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
    }

    .error .form-control:focus {
        border-color: #953b39;
        -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 6px #d59392;
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 6px #d59392;
    }

</style>
</%block>
