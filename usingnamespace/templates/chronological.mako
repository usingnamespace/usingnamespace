<%inherit file="site.mako" />
% for post in posts:
  <%include file="post.mako" args="post=post" />
% if bf.config.blog.disqus.enabled:
  <div class="after_post"><a href="${post.permalink}#disqus_thread">Read and Post Comments</a></div>
% endif
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

<%def name="post_title()">${title if title else ''}</%def>
