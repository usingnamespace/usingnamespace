<!DOCTYPE html>
<html lang="en">
    <head>
        <%block name="head">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><%block name="title">Using Namespace Management</%block></title>
        <link rel="shortcut icon" href="${request.static_url('usingnamespace:static/favicon.ico')}">
        <%block name="stylesheets">
        <link rel="stylesheet" href="${request.static_url('usingnamespace:static/bootstrap/css/bootstrap.min.css')}" type="text/css">
        ## <link rel="stylesheet" href="${request.static_url('usingnamespace:static/management/usingnamespace.css')}" type="text/css" />
        </%block>
        <%block name="javascript_head"></%block>
        <style type="text/css">
            body {
                padding-top: 50px;
            }
        </style>
        </%block>
    </head>

    <body>
        <%block name="body_content">
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="#">Project name</a>
                </div>
                <nav class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <%block name="nav">
                    <li class="active"><a href="#">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                    </%block>
                </ul>
                </nav>
            </div>
        </div>

        <%block name="main_content">
        <div class="container">
            <%block name="flash"></%block>
            % if hasattr(next, "body"):
            ${next.body()}
            % endif
        </div>
        </%block>
        </%block>
        <footer>
        <%block name="footer">
        </%block>
        </footer>
        <%block name="javascript_end">
        <script type="text/javascript" src="${request.static_url('usingnamespace:static/jquery-2.0.3.min.js')}"></script>
        <script type="text/javascript" src="${request.static_url('usingnamespace:static/bootstrap/js/bootstrap.min.js')}"></script>
        </%block>
    </body>
</html>

