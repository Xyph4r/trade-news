---
layout: page
title: Weekly recaps
permalink: /weekly/
---

{% for post in site.categories.weekly %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>{{ post.date | date: "%d %b %Y" }}</small>
{% else %}
No weekly recap yet. The first one appears on the next Monday.
{% endfor %}
