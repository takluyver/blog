.. title: So you want to write a desktop app in Python
.. slug: so-you-want-to-write-a-desktop-app-in-python
.. date: 2014-06-16 23:55:03 UTC
.. tags: 
.. link: 
.. description: 
.. type: text

This is an overview of the best tools and the best resources for building
desktop applications in Python.

First things first. You can build great desktop applications in Python, and some
are widely used (like Dropbox). But you'll have to find your own way much more
than you would using Microsoft's or Apple's SDKs. The upside is that, with a bit
of legwork to package it appropriately, it's quite feasible to write a Python
application that works on all the major platforms.

GUI toolkits
------------

The first thing you'll need to choose is a GUI toolkit.

.. image:: /images/QtLogo.png
   :align: right
   :alt: Qt logo

- For traditional desktop UIs, **Qt** is a clear winner. It's powerful, looks
  native on all the major platforms, and has probably the biggest community.
  There are two different Python bindings: `PyQt <http://www.riverbankcomputing.com/software/pyqt/intro>`_
  is older and more mature, but it's only free if your application is open source
  (`licensing <http://www.riverbankcomputing.com/software/pyqt/license>`_), while
  `PySide <http://qt-project.org/wiki/PySide>`_ is newer and more permissively
  licensed (LGPL). I refer to the `main Qt docs <http://qt-project.org/doc/>`_
  a lot - the C++ examples mostly translate to Python quite well - but both `PyQt's
  <http://pyqt.sourceforge.net/Docs/PyQt4/index.html>`_ and `PySide's docs
  <http://qt-project.org/wiki/PySideDocumentation>`_ contain some useful information.
  `Qt Designer <http://qt-project.org/doc/qt-4.8/designer-manual.html>`_ is
  a drag and drop interface to design your UI; you can compile its .ui files
  to Python modules with the pyuic command line tool.

.. figure:: /images/Qt_Designer.png

   Qt Designer in action

.. image:: /images/kivy-logo.png
   :align: right
   :height: 64px
   :alt: Kivy logo

- For attractive, tablet-style interfaces, **Kivy** is the
  right choice. It's a fairly young but promising system. If you want to bring
  your application to tablets and smartphones, then Kivy is the only option
  that I'm aware of. `More info <http://kivy.org/>`_
- When you want a basic GUI and don't care about aesthetics, **Tkinter** is a
  simple option. It's installed as part of Python. Python's own `tkinter documentation
  <https://docs.python.org/3/library/tkinter.html>`_ is rather minimal, but it
  links to a bunch of other resources. `This site <http://effbot.org/tkinterbook/>`_
  is my favourite - it hasn't been updated in years, but then neither has Tkinter
  (except that in Python 3, you ``import tkinter`` rather than ``import Tkinter``).
- An increasingly popular option is to write your application as a local web
  server, and build the UI in HTML and Javascript. This lets you use Python's
  large ecosystem of web frameworks and libraries, but it's harder to integrate
  with desktop conventions for things like opening files and window management.
  `CEF Python <https://code.google.com/p/cefpython/>`_ lets you make a window
  for your application, based on Google Chrome, but I haven't tried that.

A couple of alternatives I wouldn't recommend unless you have a reason to prefer
them: **GTK** is popular on Linux, but it
looks ugly on other platforms. The older `pygtk <http://www.pygtk.org/>`_
bindings have excellent documentation; the newer `PyGObject <https://wiki.gnome.org/Projects/PyGObject>`_
system, which supports recent versions of GTK and Python, doesn't (though it's
getting better). **wx** seems to have a good community, but development is slow,
and new projects that could have used it now mostly seem to pick Qt.

