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
* **Not a lot of deps**: sole dependency is docopt.
* **Pythonic**: because we're worth it.

Install
-------

``$ emerge dev-python/libzilla`` on Gentoo.

Usage
-----

To get you started, simply type ``lzilla --help``. The ``lzilla`` script is made up of three subcommands:

- ``$ lzilla bug`` to deal with bug reports from the CLI
- ``$ lzilla shell`` to deal with bug reports within a special shell
- ``$ lzilla git`` to parse git commit messages for bug reports and figure out what
  to do with them

License
-------

MIT
