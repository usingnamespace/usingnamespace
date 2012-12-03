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
    <h1>${permapath(post, post.current_revision.title)}</a></h1>
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

<%def name="yearlink(entry, text)">
    <a href="${request.route_url('uns.year', year=entry.year)}">${text}</a>
</%def>

<%def name="yearmonthlink(entry, text)">
    <a href="${request.route_url('uns.year.month', year=entry.year, month=entry.month)}">${text}</a>
</%def>

<%def name="yearmonthdaylink(entry, text)">
    <a href="${request.route_url('uns.year.month.day', year=entry.year, month=entry.month, day=entry.day)}">${text}</a>
</%def>

<%def name="permapath(entry, text)">
    <a href="${request.route_url('uns.year.month.day.title', year=entry.year, month=entry.month, day=entry.day, title=entry.slug)}">${text}</a>
</%def>
