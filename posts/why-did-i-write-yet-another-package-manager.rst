.. title: Why did I write yet another package manager?
.. slug: why-did-i-write-yet-another-package-manager
.. date: 2015-11-20 13:06:47 UTC
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

`Batis <http://batis-installer.github.io/>`_ is a package manager for desktop applications on Linux.
Linux users are probably already used to using several different package managers -
apt, pip, npm, etc. - so why on earth do we need one more?

Firstly, having many package managers is not a problem.
There are many different kinds of things we want to install.
Pip, for instance, knows how to install python packages;
if you want to install a ruby package, you'll need another tool. 
The atom text editor includes a package manager, apm, purely for its own extensions,
and other extensible applications, like browsers, are quietly doing their own package management too.
You can try to build one package manager to rule them all, as Linux distros do,
but that system has to be more complex.
‘Do one thing well’ applies to package managers too.

The best way to distribute desktop applications on Linux at present is through distro repositories.
The idea is that power users from each distro who like your application will prepare packages,
making it easily available for other users of the same distro.
But this has several drawbacks for application developers:

* You’re not in control of your distribution channels -
  if a distro doesn’t like your app, they can block their users’ easy access to it.
* Feature releases of your app are tied to releases of the entire distro.
  Launch version 2.0 at the wrong time, and even the keen Ubuntu users who
  update on release day it comes out won’t see your new features for six months.
  Some users will be stuck on old versions for *years*.
  There are exceptions, but this is the norm in the major Linux distributions.
* If you want to bypass the distros and host your own repositories,
  you have to deal with several different packaging systems -
  at a minimum, .deb and .rpm packages. Desktop Linux is a small market anyway,
  and this fragmentation makes it even more painful to target.
* Your install instructions either have to be vague,
  or contain a table of commands for different distros
  (like `0 A.D. <http://play0ad.com/download/linux/>`__ or `git-cola <https://git-cola.github.io/downloads.html>`__).
  Neither is ideal for less technical users.
* Distro packages can usually only be installed as root.
  This often doesn’t matter for desktop use, where the user is usually the owner of the computer,
  but it can be an annoying restriction.

The tools for packaging modules in many programming languages can also be used to
package command line applications. You've probably seen utilities that you install
using pip (e.g. `Nikola <https://getnikola.com/getting-started.html>`__),
npm (`bower <http://bower.io/#install-bower>`__),
or gem (`Jekyll <https://jekyllrb.com/>`__).
But these tools don't know about creating menu entries or file associations, so
they're not great for distributing graphical applications.

Many applications forgo all of these packaging mechanisms,
and distribute tarballs or zip files from their own website (e.g. 
`Powder Toy <http://powdertoy.co.uk/>`__,
`PyCharm <https://www.jetbrains.com/pycharm/download/#linux>`__,
`Visual Studio Code <https://code.visualstudio.com/>`__).
This is the starting point for Batis.
Batis adds a consistent way to install and uninstall applications, so that developers
can focus on their applications, not on rewriting Linux install code.
A Batis package is a regular tarball with some extra files, so there’s no need
to build another tarball for users without Batis.
You even get a free ``install.sh`` script inside your package for those users to run.

Batis adds one extra layer above tarball downloads, the index file.
This is a JSON file containing the URLs of the tarballs for download,
along with some basic metadata.
Batis uses this to select the best build to install -
for instance if you have separate builds for 64 bit and 32 bit systems.
In future versions, the index will also be used to check for updates to installed applications.

So, **Batis is** a distro-agnostic way for users to get applications directly
from developers. It works with the standard mechanisms to integrate applications
into the desktop environment. And it's an evolutionary improvement on distributing
plain tarballs.

`Batis website <http://batis-installer.github.io/>`__—for more information
