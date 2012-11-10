<%page args="post, comments=None"/>

<article>
    <header>
        <!-- date published or updated -->
        <time pubdate datetime="${self.post_time_full(post)}">
            <span class='time'>${post.pubdate.strftime("%H:%M")}</span>
            <span class='daymonth'><a href="/${post.pubdate.strftime("%Y/%m/%d")}/">${post.pubdate.strftime("%d")}</a> <abbr title="${post.pubdate.strftime("%B")}"><a href="/${post.pubdate.strftime("%Y/%m")}/">${post.pubdate.strftime("%b")}</a></abbr></span>
            <span class='year'><a href="/${post.pubdate.strftime("%Y")}/">${post.pubdate.strftime("%Y")}</a></span>
        </time>
    </header>
    <section>
    <h1><a href="${post.slug}">${post.current_revision.title}</a></h1>
    ${self.post_prose(post)}
    </section>
</article>

<%def name="post_prose(post)">
  ${post.current_revision.entry}
</%def>

<%def name="post_time_full(post)">${post.pubdate.isoformat()}</%def>

<%def name="categories(post)">
    <ul class="categories">
    % for category in post.categories:
        % if post.draft == True:
        <li>${category.name}</li>
        % else:
        <li><a href='${category.path}'>${category.name}</a></li>
        % endif
    % endfor
    </ul>
</%def>
