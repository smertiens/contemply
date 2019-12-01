# Contemply

[![Build Status](https://travis-ci.org/smertiens/contemply.svg?branch=develop)](https://travis-ci.org/smertiens/contemply)
[![Documentation Status](https://readthedocs.org/projects/contemply/badge/?version=latest)](https://contemply.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/contemply.svg)](https://badge.fury.io/py/contemply)

Contemply turns your boring old templates and project scaffolds into interactive code generators. 

Template contents and all the information necessary to process them are kept in a single file.
Contemply's storage allows you to easily access your templates on your computer or in your network.

What else can it do?

* Different ways to prompt your users for input
* Create different files and folders from one template
* Add your own functions using extensions

If you want to **integrate code generation into you own project**, you can use the Contemply library,
see [developer docs](https://contemply.readthedocs.io) for more details.

Help by creating an issue on GitHub for bugs or feature requests.  Contributors are always welcome! 

## Installation

The easiest way to install Contemply is using pip:

````
pip install contemply
````

## Your first template

```
#: time_of_day = choose("What is your preferred time of day?", ["day", "night", "morning"])

#: >> "say_hello.txt"
Hello $("What's your name?"), have a nice $time_of_day!
```

Save it as demo.pytpl.

```
contemply run demo.tpl
```

## Documentation and support

You can find the documentation here: https://contemply.readthedocs.io/en/latest/

If you find any bugs or have a feature request, please create an issue on github: https://github.com/smertiens/contemply/issues

## Changes

1.2.0: Added support for "inline asks", "$" is now escapable in content lines 

1.1.0: Added support for the creation of multiple output files, added functions to create folders

1.0.0: First production release
