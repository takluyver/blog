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
- `pygame <http://pygame.org/>`_ is popular for building simple 2D games. There
  are also frameworks for 3D graphics (`pyglet <http://www.pyglet.org/>`_,
  `Panda3d <https://www.panda3d.org/>`_), but I don't know much about them.
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

Packaging and Distribution
--------------------------

This is probably the roughest part of making an application in Python. You can
easily distribute tools for developers as Python packages to be installed using
pip, but end users don't generally have Python and pip already set up. Python
packages also can't depend on something like Qt. There are a number of ways to
package your application and its dependencies:

- `Pynsist <http://pynsist.readthedocs.org/>`_, my own project, makes
  a Windows installer which installs a version of Python that you specify, and
  then installs your application. Unlike the other tools listed here, it doesn't
  try to 'freeze' your application into an exe, but makes shortcuts which launch
  .py files. This avoids certain kinds of bugs.
- `cx_Freeze <http://cx-freeze.sourceforge.net/>`_ is a freeze tool:
  it makes an executable out of your application. It works on Windows, Mac and
  Linux, but only produces the executable for the platform you run it on (you
  can't make a Windows exe on Linux, for example).
  It can make simple packages (.msi for Windows, .dmg for Mac, .rpm for Linux),
  or you can feed its output into `NSIS <http://nsis.sourceforge.net/>`_ or
  `Inno Setup <http://www.jrsoftware.org/isinfo.php>`_ to have more control over
  building a Windows installer.
- `PyInstaller <http://www.pyinstaller.org/>`_ is similar to cx_Freeze.
  It doesn't yet support Python 3, but it does have the ability to produce a
  'single file' executable.
- `py2app <http://pythonhosted.org/py2app/>`_ is a freeze tool specifically
  for building Mac .app bundles.
- `py2exe <http://www.py2exe.org/>`_ is a Windows-only freeze tool.
  Development stopped for a long time, but at the time of writing there is some
  recent activity on it.

Linux packaging
~~~~~~~~~~~~~~~

Although some of the freeze tools can build Linux binaries, the preferred way to
distribute software is to make a package containing just your application, which
has *dependencies* on Python and the libraries your application uses. So your
package doesn't contain everything it needs, but it tells the package manager
what other pieces it needs installed.

Unfortunately, the procedures for preparing these are pretty complex, and Linux
distributions still don't have a common package format. The main ones are deb
packages, used by Debian, Ubuntu and Mint, and rpm packages, used by Fedora and
Red Hat. I don't know of a good, simple guide to packaging Python applications
for either - if you find one or write one, let me know.

You can get users to download and install your package, but if you want it to
receive updates through the package manager, you'll need to host it in a
repository. Submitting your package to the distribution's main repositories makes
it easiest for users to install, but it has to meet the distro's quality
standards, and you generally can't push new feature releases to people except when
they upgrade the whole distribution. Some distributions offer hosting for
personal repos: Ubuntu's PPAs, or Fedora's Fedorapeople repositories. You can
also set up a repository on your own server.

If you don't want to think about all that, just make a tarball of your application,
and explain to Linux users next to the download what it requires.

Miscellaneous
-------------

- **Threading**: If your application does anything taking longer than about a tenth
  of a second, you should do it in a background thread, so your UI doesn't freeze
  up. Be sure to only interact with GUI elements from the main thread, or you
  can get segfaults. Python's GIL isn't a big issue here: the UI thread shouldn't
  need much Python processing time.
- **Updates**: `Esky <https://pypi.python.org/pypi/esky>`_ is a framework for
  updating frozen Python applications. I haven't tried it, but it looks interesting.
