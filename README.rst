libzilla: a pythonic Bugzilla API
===============================================================================

Libzilla is a set of functions for managing Bugzilla bug reports. All
communications are carried out using the Bugzilla REST API over the HTTPS
scheme. The library is shipped with a fairly straightforward script built with
the beautiful docopt module.

Get started
-------------------------------------------------------------------------------

To get you started, simply type:

.. code-block:: bash
    $ lzilla --help

The lzilla script is made up of three subcommands:
* `lzilla bug` to deal with bug reports from the CLI
* `lzilla shell` to deal with bug reports within a special shell
* `lzilla git` to parse git commit messages for bug reports and figure out what
  to do with them
