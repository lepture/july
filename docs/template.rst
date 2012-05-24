.. _template:

Template
==========

July is a set of tools to make tornado easier to organize, it didn't create a new template
engine, instead, this section is all about tornado's template engine.


.. _syntax-overview:

Syntax Overview
----------------

The basic syntax overview:

.. sourcecode:: html+jinja

    ### base.html
    <html>
      <head>
        <title>{% block title %}Default title{% end %}</title>
      </head>
      <body>
        <ul>
          {% for student in students %}
            {% block student %}
              <li>{{ escape(student.name) }}</li>
            {% end %}
          {% end %}
        </ul>
      </body>
    </html>

    ### bold.html
    {% extends "base.html" %}

    {% block title %}A bolder title{% end %}

    {% block student %}
      <li><span style="bold">{{ escape(student.name) }}</span></li>
    {% end %}


Variable
------------

Just like Django, variables are::

    Hello, {{ variable }}

Something you should know:

1. dict must be accessed with ``{{ var["key"] }}``, not ``{{ var.key }}``.
2. unlike Django and Jinja, there is no filter, just function: ``{{ escape(var) }}`` , not
   ``{{ var|escape }}``.

You can set a variable in template::

    {% set name = "July" %}

Basic Logic
------------

Logic end with ``{% end %}``:

.. sourcecode:: html+jinja

    {% if not current_user %}
        You're not logged in!
    {% elif current_user and curent_user.is_admin %}
        Good day, sir!
    {% else %}
        Howdy!
    {% end %}

    {% for link in links %}
        <a href="{{ link.href }}">{{ link.title }}</a>
    {% end %}

    {% set i = 10 %}
    {% while i %}
        Item {{ i }}
        {% set i -= 1 %}
    {% end %}


Unlike Django and Jinja, all logic end with ``{% end %}``, not ``{% endif %}`` or something
like this.


Comments
---------

To comment out a section::

    {#
        ...
        ...
    #}

Or with ``comment`` keyword for oneline::

    {% comment "..." %}



Inherits and Includes
---------------------

Just like Django and Jinja, tornado template provides ``extends``,
``block`` and ``include``, example at :ref:`syntax-overview`.

Differences from Django and Jinja:

.. sourcecode:: html+jinja

    templates/
        layout.html
        app/
            index.html
    
    ### templates/app/index.html
    {% extends "../layout.html" %}


Tornado template finds a template by reversing path. But July changed the way,
so you can ``extends`` or ``include`` with::

    {% extends "layout.html" %}


Python Code
------------

Tornado template support python code:

.. sourcecode:: jinja

    {% import os %}
    {{ os.name }}

    {% from tornado import escape %}
    {{ escape.xhtml_escape(var) }}


Actually everything in tornado template is python code, you can write for-logic::

    {% for student in [p for p in people if p.student and p.age > 23] %}
        <li>{{ escape(student.name) }}</li>
    {% end %}


You can even try catch::

    {% try %}
        ...
    {% except %}
        ...
    {% finally %}

Module
---------

Applying 
---------

Understand ``apply`` keyword::

    {% apply function %}
    ...
    {% end %}

means::

    {{ function(...) }}

But it will be very useful when applying a function to a section.


Autoescape
-----------

Register a function
-------------------

