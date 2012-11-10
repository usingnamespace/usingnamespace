<%inherit file="site.mako" />
<div id="Yearly">
<h1><a href="/${year}/">Archive for ${year}</a></h1>

% for ((monthnum, month), posts) in monthly: 
    <% curday = 0; first = True %>
    <div class="monthly">
        <h1><a href="/${year}/${monthnum}/">${month}</a></h1>
        % for post in posts:
            <% postday = post.date.strftime("%d") %>
            % if curday != postday:
                % if first == False:
                </ul>
            % endif
            <% curday = postday; first= False %>
            <h2>${postday}</h2>
            <ul>
            % endif
            <li><a href="${post.permapath()}">${post.title}</a></li>
        % endfor
    </ul>
</div>
% endfor
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
