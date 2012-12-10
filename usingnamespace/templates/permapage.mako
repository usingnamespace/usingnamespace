<%inherit file="site.mako" />
<%include file="post.mako" args="post=post, comments=comments" />

<%def name="post_title()">${post.title}</%def>
<%def name="canonical()"><link rel="canonical" href="${post.permalink}"></%def>
