<%inherit file="site.mako" />
<div id="Yearly">
    <h1><a href="${h['url'].y_archive(year)}">Archive for ${year}</a></h1>

<% curmonth = 0; curday = 0 %>
% for entry in entries:
    % if curmonth != entry.month:
        % if curmonth != 0:
        </div>
        % endif
        <% curmonth = entry.month; curday = 0 %>
        <div class="monthly">
            <h1><a href="${h['url'].ym_archive(entry.year, curmonth)}">${entry.pubdate.strftime('%B')}</a></h1>
    % endif

    % if curday != entry.day:
        % if curday != 0:
        </ul>
        % endif
        <% curday = entry.day %>
        <h2><a href="${h['url'].ymd_archive(entry.year, curmonth, curday)}">${curday}</a></h2>
        <ul>
    % endif

    <li><a href="${h['url'].entry(entry)}">${entry.title}</a></li>
% endfor
        </ul>
    </div>
</div>


<ul class="prevnext">
    % if prev_year:
        <li><a href="${h['url'].y_archive(prev_year)}">« Previous Year</a></li>
    % endif
    % if next_year and prev_year:
        <li>•</li>
    % endif
    % if next_year:
        <li><a href="${h['url'].y_archive(next_year)}">Next Year »</a></li>
    % endif
</ul>


<%def name="post_title()">Archive for ${year}</%def>
