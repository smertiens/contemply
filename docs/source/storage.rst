Template storage
================

.. _storage:

Basic usage
***********

Often your template file might not be in the same directory your new file should be in. Also you might want to define
one or more central locations for your templates, so other people can use them as well (e.g. on a network share).
In both cases the **Template Storage** feature can be helpful.

A template storage is simply a name that points to a directory with templates and can be used as a shortcut.
Let's take a look at an example:

Instead of doing this:

::

    contemply /Volumes/data/templates/for_work/default.pytpl


we will define a new template storage:

::

    contemply storage:add work_templates /Volumes/data/templates/for_work


and use this instead:

::

    contemply work_templates::default.pytpl


The list of storages are saved in the Contemply user settings. You can find the file at different location,
depending on your operating system:

* Linux and OSX: USERHOME/.contemply/settings.json
* Windows: USERHOME/contemply/settings.json

USERHOME corresponds to your users home directory.


Command line options
********************

Storages are added using the command line:

Add a new storage location
--------------------------

::

    contemply storage:add NAME PATH


NAME is the storage name and should contain only alphanumeric character, the . or the _ sign. PATH is the path
to your template directory.

Remove a storage location
-------------------------

::

    contemply storage:remove NAME


NAME is the name of the storage you want to remove.

List all locations
------------------

::

    contemply storage:list


This will show a list of all known storage locations.