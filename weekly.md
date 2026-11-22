---
layout: page
title: Weekly recaps
title_de: Wochenrückblicke
permalink: /weekly/
---

{% if site.categories.weekly %}
{% include post-list.html posts=site.categories.weekly limit=100 %}
{% else %}
<p>{% include t.html en="No weekly recap yet. The first one appears on the next Monday." de="Noch kein Wochenrückblick. Der erste erscheint am nächsten Montag." %}</p>
{% endif %}
