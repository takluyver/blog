.. link: 
.. description: 
.. tags: 
.. date: 2014/04/27 17:39:44
.. title: ASTsearch - code searching that knows about code
.. slug: astsearch-code-searching-that-knows-about-code

This weekend's hack is a tool for searching Python code.

`ASTsearch source code on Github <https://github.com/takluyver/astsearch>`_

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
46 results, all of which represent division operations.

In this case, grep produced a lot of false positives. In other cases, it will
have false negatives—results that you wanted but didn't find. ``a=1`` won't
match ``a= 1``, and ``"this"`` won't match ``'this'``. For simple cases, regexes
can help (``a\s*=\s*1``), but they soon get unwieldy. ASTsearch is insensitive
to how you format your code: even statements split over several lines are easy
to find.

How does it work?
-----------------

The string pattern—``?/?`` in the example above—is turned into an AST pattern.
ASTs, or Abstract Syntax Trees, are a structured representation of a formal
language such as Python source code.

``?`` is a wildcard, so ``?/?`` means "anything divided by anything". I picked
``?`` for this because it's not used in Python syntax, so it doesn't stop you
writing more specific search patterns.

Some more patterns:

- ``a = ?`` - Something is assigned to ``a``
- ``class ?(TemplateExporter): ?`` - A subclass of TemplateExporter
- ``for ? in ?: ? \nelse: ?`` - A for loop with an ``else`` clause

Then it walks the directory, parsing each file with a ``.py`` extension using
Python's built in parser. The standard library `ast module
<https://docs.python.org/3/library/ast.html>`_ contains the tools to parse the
code and walk the AST, and `astcheck <https://pypi.python.org/pypi/astcheck>`_,
another tool I wrote, can compare AST nodes against a template.

Besides the command line interface, you can also use ASTsearch as a Python
module (``import astsearch``). It's possible to define complex search patterns
in Python code that can't be written at the command line. `See the docs
<http://astsearch.readthedocs.org/en/latest/api.html>`_ for some more details.

What's the catch?
-----------------

ASTsearch only works on Python files, and Python files that are entirely valid
syntax (that's Python 3 syntax for now). If just the last line can't be parsed,
it won't find any matches in that file.

It's slower than grep, because what it's doing is much more complex, and grep is
`highly optimised <http://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html>`_.
But Python's parser is doing most of the hard work, and that's written in C. On
my laptop, scanning the IPython codebase (about 100k lines of code) takes about
3.5 seconds—definitely not instant, but far faster than I can think about even a
couple of results.

There are search patterns you can't express at the command line. For instance,
you can't match function calls with a specific number of arguments (but you can
find function *definitions* with a given number of arguments: ``def ?(?, ?): ?``).
I might extend the pattern mini-language once I've got a feel for what would be
useful.

How do I install it?
--------------------

::

    pip install astsearch
