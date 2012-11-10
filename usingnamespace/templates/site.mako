<!DOCTYPE html>
<html lang="en">
    <!-- Copyright (c) 2012 Bert JW Regeer -->
    <head><%block name="head">
        <title><%block name="title"></%block></title>
        <link rel="shortcut icon" href="${request.static_url('usingnamespace:static/favicon.ico')}">
        <%block name="atom">
        <link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="" />
        <link rel="alternate" type="application/atom+xml" title="Atom 1.0" href="" />
        </%block>
        <%block name="stylesheets">
        <link rel="stylesheet" href="${request.static_url('usingnamespace:static/usingnamespace.css')}" type="text/css" media="screen" />
        <link rel="stylesheet" href="${request.static_url('usingnamespace:static/pygments.css')}" type="text/css" media="screen" />
        </%block>
        <meta charset="utf-8" />
        <%block name="javascript"><%include file="javascript.mako" /></%block>
    </%block></head>
    <body>
        <header>
        <%block name="header"><%include file="header.mako" /></%block>
        </header>
        <div id="Mwrapper">
            <div id="MainContent">
                % if hasattr(next.__class__, "body"):
                    ${next.body()}
                % endif
            </div>
        </div>
        <aside>
        <nav>
        <%block name="menu"><%include file="menu.mako" /></%block>
        </nav>
        </aside>

        <footer>
        <%block name="footer"><%include file="footer.mako" /></%block>
        </footer>
    </body>

</html>
