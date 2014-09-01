<%inherit file="site.mako" />

<div id="page-header"><h1>API Tickets</h1></div>

% if tickets:
<p>You have the following API tickets: </p>
<ul>
    % for ticket in tickets:
    <li>
    <pre>${ticket}</pre>
    </li>
    % endfor
</ul>
% else:
<p>You don't have any API tickets yet</p>
% endif

<h4>New API Ticket</h4>
<div class="form-button">
    ${form|n}
</div>

<%block name="title">API Tickets - ${parent.title()}</%block>

