.. link: 
.. description: 
.. tags: 
.. date: 2014/04/27 17:39:44
.. title: ASTsearch - code searching that knows about code
.. slug: astsearch-code-searching-that-knows-about-code

This weekend's hack is a tool for searching Python code.

What's wrong with grep, you might ask? Let's try to find every division in
IPython's codebase::

    $ grep --include "*.py" -rF "/" .
    config/loader.py:        after applying any insert / extend / update changes
    config/configurable.py:                    # ConfigValue is a wrapper for using append / update on containers
    config/tests/test_loader.py:        argv = ['--a=~/1/2/3', '--b=~', '--c=~/', '--d="~/"']
    config/tests/test_loader.py:        self.assertEqual(config.a, os.path.expanduser('~/1/2/3'))
    config/tests/test_loader.py:        self.assertEqual(config.c, os.path.expanduser('~/'))
    config/tests/test_loader.py:        self.assertEqual(config.d, '~/')
    ...

In all, it finds 1685 lines, and very few of them are actual division. You could
write a regex that tries to ignore comments and strings, but `now you have two
problems <http://regex.info/blog/2006-09-15/247>`_.

Let's do the same with ASTsearch::

    $ astsearch "?/?"
    core/oinspect.py
     646|        shalf = int((string_max -5)/2)

    core/ultratb.py
    1254|        return h / i

    core/page.py
     347|        whalf = int((width -5)/2)
    ...

The output is 89 lines, and when spacing and filenames are removed, there are
46 results, all of which represent actual division operations.

How does it work?
-----------------

The string pattern—``?/?`` in the example above—is turned into an AST pattern.
ASTs, or Abstract Syntax Trees, are a structured representation of Python source
code. I've made ``?`` a wildcard (it's not used in regular Python syntax), so
``?/?`` means "anything divided by anything".

Some more patterns:

- ``a = ?`` - Something is assigned to ``a``.
- ``class ?(TemplateExporter): ?`` - A class defintion subclassing TemplateExporter
- ``for ? in ?: ? \nelse: ?`` - A for loop with an ``else`` clause

Then it walks the directory, parsing each file with a ``.py`` extension using
Python's built in parser. The standard library `ast module
<https://docs.python.org/3/library/ast.html>`_ contains the tools to parse the
code and walk the AST, and my `astcheck module
