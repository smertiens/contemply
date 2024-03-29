Installation
============

Install via pip
***************

The easiest way to install Contemply is via pip:

::

    pip install contemply

Usage from the commandline
**************************

The only argument required is the name of the template file you want to run:

::

    contemply run template.pytpl

There are a number of command line options that you can use:

.. list-table:: Command line options
   :header-rows: 1

   * - Option
     - Description
   * - \\-h, \\-\\-help
     - show a list of possible arguments
   * - \\-v, \\-\\-verbose
     - increase output verbosity
   * - \\-p, \\-\\-print
     - Print output to console instead of creating a new file
   * - \\--no-header
     - If set the header will not be printed

To print the version of Contemply you can use the "version" subcommand:

::

    contemply version

For further subcommands see :ref:`storage`.

Get support
***********

You can issue a bug report or feature request on the project's GitHub page: https://github.com/smertiens/contemply/issues

Contribute
**********


Contributors are always welcome. You can fork the project on GitHub: https://github.com/smertiens/contemply
