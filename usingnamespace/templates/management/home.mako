<%inherit file="site.mako" />

<div "page-header"><h1>My Sites</h1></div>

% if sites:
<p>You have the following sites: </p>
<ul>
    % for site in sites:
    <li>${site.title} (${site.idna})
    <p>Entries:
    <ul>
        % for entry in site.entries.limit(2):
        <li>${entry.title}</li>
        % endfor
    </ul>
    </p>
    <p>Domains:
    <ul>
        % for domain in site.domains:
        <li>${domain.domain}</li>
        % endfor
    </ul>
    </p>
    </li>
    % endfor
</ul>
% else:
<p>You don't have any sites</p>
% endif

<%block name="title">Home - ${parent.title()}</%block>
