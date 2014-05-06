<!DOCTYPE html>
<html lang="en">
    <head>
        <%block name="head">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><%block name="title">Using Namespace Management</%block></title>
        <link rel="shortcut icon" href="${request.static_url('usingnamespace:static/favicon.ico')}">
        <%block name="stylesheets">
        <link rel="stylesheet" href="${request.static_url('usingnamespace:static/management.css')}" type="text/css" />
        </%block>
        <%block name="javascript_head"></%block>
        </%block>
    </head>

    <body>
        <%block name="body_content">
        <header>
            <h1>
                <a href="${request.route_url('management', traverse='')}">${request.registry.settings['usingnamespace.name']}</a>
            </h1>
            <nav>
                <ul>
                    <%block name="nav">
                    <li><a href="${request.route_url('management', traverse='')}">Home</a></li>
                    <li><a href="${request.route_url('management', traverse='api')}">API Tickets</a></li>
                    <li><a href="${request.route_url('management', traverse='deauth')}">Deauth</a></li>
                    </%block>
                </ul>
            </nav>
        </header>

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
        </%block>
    </body>
</html>

