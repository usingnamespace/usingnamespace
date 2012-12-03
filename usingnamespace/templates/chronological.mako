<%inherit file="site.mako" />
% for entry in entries:
  <%include file="post.mako" args="post=entry" />
% endfor
<ul class="prevnext">
% if prev_link:
 <li><a href="${prev_link}">« Previous Page</a></li>
% endif
% if next_link and prev_link:
 <li>•</li>
% endif
% if next_link:
 <li><a href="${next_link}">Next Page »</a></li>
% endif
</ul>

