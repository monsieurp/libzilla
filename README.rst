libzilla: a pythonic Bugzilla API
=================================

Libzilla is a set of functions for managing Bugzilla bug reports. All
communications are carried out using the Bugzilla REST API over the HTTPS
scheme. The library is shipped with a fairly straightforward script built with
the beautiful docopt module.

Features
--------

* **Easy to use**: only requires a shell.
* **Scriptable**: can be used in conjunction with other scripts.
* **Not a lot of deps**: built with docopt and requests.
* **Pythonic**: because we're worth it.

Install
-------

``$ emerge dev-python/libzilla`` on Gentoo.

Usage
-----

To get you started, simply type ``lzilla --help``. The ``lzilla`` script is
made up of a bunch of subcommands:

- ``$ lzilla stable`` to read an ebuild and file a stabilisation request on the fly
- ``$ lzilla shell`` to deal with one or more bug numbers within a special shell
- ``$ lzilla git`` to parse the last git commit message for one or more bug numbers
- ``$ lzilla bug`` to deal with one or more bug numbers from the CLI

License
-------

MIT
