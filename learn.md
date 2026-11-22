---
layout: page
title: Learn
title_de: Lernen
permalink: /learn/
---

<p>{% include t.html en="Short explanations of the concepts that come up in the briefings, and of how this site works. Each page takes two or three minutes to read." de="Kurze Erklärungen der Begriffe aus den Briefings und dazu, wie diese Seite funktioniert. Jede Seite ist in zwei, drei Minuten gelesen." %}</p>

{% assign concepts = site.learn | sort: "order" %}
{% for cat in site.data.learn_categories.categories %}
<h2 class="learn-category">{% include t.html en=cat.en de=cat.de %}</h2>
<ul class="learn-list">
{%- for c in concepts -%}
  {%- if c.category == cat.id %}
  <li><a href="{{ c.url | relative_url }}">{% include t.html en=c.title de=c.title_de %}</a><br><small>{% include t.html en=c.summary de=c.summary_de %}</small></li>
  {%- endif -%}
{%- endfor %}
</ul>
{% endfor %}
