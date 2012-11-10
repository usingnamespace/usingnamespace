<%page args="post, comments=None"/>

<article>
    <header>
        <!-- date published or updated -->
        <time pubdate datetime="${self.post_time_full(post)}">
            <span class='time'>${post.date.strftime("%H:%M")}</span>
            <span class='daymonth'><a href="/${post.date.strftime("%Y/%m/%d")}/">${post.date.strftime("%d")}</a> <abbr title="${post.date.strftime("%B")}"><a href="/${post.date.strftime("%Y/%m")}/">${post.date.strftime("%b")}</a></abbr></span>
            <span class='year'><a href="/${post.date.strftime("%Y")}/">${post.date.strftime("%Y")}</a></span>
        </time>
    </header>
    <section>
    <h1><a href="${post.permapath()}">${post.title}</a></h1>
    ${self.post_prose(post)}
    </section>
    ${self.categories(post)}

    % if comments is not None:
        ${comments(post)}
    % endif
</article>

<%def name="post_prose(post)">
  ${post.content}
</%def>

<%def name="post_time_full(post)">${post.date.isoformat()}</%def>

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
