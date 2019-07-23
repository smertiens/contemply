# Contemply

[![Build Status](https://travis-ci.org/smertiens/contemply.svg?branch=develop)](https://travis-ci.org/smertiens/contemply)
[![Documentation Status](https://readthedocs.org/projects/contemply/badge/?version=latest)](https://contemply.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/contemply.svg)](https://badge.fury.io/py/contemply)

Contemply turns your boring old templates and project scaffolds into interactive code generators. 

Everything (including your template) is kept in one file and easy to share and edit. With Contemply you can guide 
your users through the creation of any kind of text-file, Python or not.

How it works:

* Create your template file, place variables where needed. You can use if-clauses, loops and different formatting
functions if you like.
* Prompt your user for input or let him choose an option to get all the information you need to build your 
scaffold file.

Keep all things in one place:

* You can add template-paths using Contemply's storage function. Instead of typing the full path to your
template file you can use shortcuts like "work_templates::data_project.pytpl". 

If you want to **integrate code generation into you own project**, you can use the Contemply library,
see [developer docs](https://contemply.readthedocs.io/en/develop/developer.html) for more details.

Help by creating an issue on GitHub for bugs or feature requests.  Contributors are always welcome! 

## Installation

The easiest way to install Contemply is using pip:

````
pip install contemply
````

Give it a testdrive:

````
contemply run samples:class
````

## Documentation and support

You can find the documentation here: https://contemply.readthedocs.io/en/latest/

If you find any bugs or have a feature request, please create an issue on github: https://github.com/smertiens/contemply/issues

## Example

### 1. Take your template file and add some Contemply magic

````python
#::
classname = ask('How should the new class be called?')
text = ask('What should the text be?')
printVersion = yesno('Create the version function?', 'Yes')

version = '1.0.0'
#::

#: >> "$classname.py"
class $classname:

    def someFunction(self):
        print('$text')

#: if printVersion == True
    def versionFunction(self):
        print('$version')
#: endif
#: <<
````

Save this file as demo.pytpl

## 2. Run contemply

```
contemply run demo.pytpl
```

Contemply will ask you some questions...


```
How should the new class be called? MyClass
What should the text be? Hello World
Create the version function? [Yes]: No
```

## 3. Take a look at your outputfile

Called MyClass.py:

````python
# This is a demo file

class MyClass:

    def someFunction(self):
        print('Hello World')
````

# Changelog

1.1.0b1: Added support for the creation of multiple output files and folders

