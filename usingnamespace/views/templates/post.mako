<%page args="post, comments=None"/>

<article>
    <header>
        <!-- date published or updated -->
        <time pubdate datetime="${self.post_time_full(post)}">
            <span class='time'>${post.time}</span>
            <span class='daymonth'>${yearmonthdaylink(post, post.day)}</a> <abbr title="${post.pubdate.strftime("%B")}">${yearmonthlink(post, post.pubdate.strftime("%b"))}</a></abbr></span>
            <span class='year'>${yearlink(post, post.year)}</a></span>
        </time>
    </header>
    <section>
    <h1>${permapath(post, post.title)}</a></h1>
    ${self.post_prose(post)}
    </section>
</article>

<%def name="post_prose(post)">
  ${post.entry}
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

<%def name="yearlink(entry, text)">
    <a href="${h['url'].y_archive(entry)}">${text}</a>
</%def>

<%def name="yearmonthlink(entry, text)">
    <a href="${h['url'].ym_archive(entry)}">${text}</a>
</%def>

<%def name="yearmonthdaylink(entry, text)">
    <a href="${h['url'].ymd_archive(entry)}">${text}</a>
</%def>

<%def name="permapath(entry, text)">
    <a href="${h['url'].entry(entry)}">${text}</a>
</%def>
