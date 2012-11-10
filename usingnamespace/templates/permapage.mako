<%inherit file="site.mako" />
<%include file="post.mako" args="post=post, comments=comments" />

<div id="social">
    <div class="g-plusone" data-href="${post.permalink}"></div>
    <div><a href="https://twitter.com/share" class="twitter-share-button"
            data-url="${post.permalink}"
            data-via="funcptr">Tweet</a></div>
    <div><a href='http://coderwall.com/bertjwregeer'><img src='http://api.coderwall.com/bertjwregeer/endorsecount.png' /></a></div>
</div>

<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
<script type="text/javascript">gapi.plusone.go();</script>

<%def name="comments(post)">
    % if bf.config.blog.disqus.enabled:
    <div id="disqus_thread"></div>
    <script type="text/javascript">
        var disqus_url = "${post.permalink}";
    </script>
        <script type="text/javascript" src="http://disqus.com/forums/${bf.config.blog.disqus.name}/embed.js"></script>
        <noscript><a href="http://${bf.config.blog.disqus.name}.disqus.com/?url=ref">View the discussion thread.</a></noscript><a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
    % endif
</%def>

<%def name="post_title()">${post.title}</%def>
<%def name="canonical()"><link rel="canonical" href="${post.permalink}"></%def>
