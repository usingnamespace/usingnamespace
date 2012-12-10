<%inherit file="site.mako" />
<%namespace name="entry_funcs" file="post.mako"/>
<div id="Yearly">
<h1><% entry_funcs.yearlink(entries[0], "Archive for " + year) %></h1>

<% curmonth = 0; curday = 0 %>
% for entry in entries:
    % if curmonth != entry.month:
        % if curmonth != 0:
        </div>
        % endif
        <% curmonth = entry.month; curday = 0 %>
        <div class="monthly">
            <h1><% entry_funcs.yearmonthlink(entry, entry.pubdate.strftime('%B')) %></a></h1>
    % endif

    % if curday != entry.day:
        % if curday != 0:
        </ul>
        % endif
        <% curday = entry.day %>
        <h2><% entry_funcs.yearmonthdaylink(entry, curday) %></h2>
        <ul>
    % endif

    <li><% entry_funcs.permapath(entry, entry.title) %></a></li>
% endfor
        </ul>
    </div>
</div>


<ul class="prevnext">
    % if prev_link:
        <li><a href="${prev_link}">« Previous Year</a></li>
    % endif
    % if next_link and prev_link:
        <li>•</li>
    % endif
    % if next_link:
        <li><a href="${next_link}">Next Year »</a></li>
    % endif
</ul>


<%def name="post_title()">Archive for ${year}</%def>
