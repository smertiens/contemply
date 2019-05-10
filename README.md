# Contemply

[![Build Status](https://travis-ci.org/smertiens/contemply.svg?branch=master)](https://travis-ci.org/smertiens/contemply)
[![Documentation Status](https://readthedocs.org/projects/contemply/badge/?version=latest)](https://contemply.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/contemply.svg)](https://badge.fury.io/py/contemply)

A code generator that interactively creates boilerplate files from templates.

All the questions necessary to interactively create a file from your template are embedded in the template itself,
so all you need is Contemply and your template file to get up and running.
If you want to integrate code generation into you own project, you can use the Contemply library,
see [developer docs](https://contemply.readthedocs.io/en/latest/templates/developer.html) for more details.

The project is in early beta right now, you can help by creating an issue on GitHub for bugs or feature requests. 
Contributors are always welcome! 

## Installation

The easiest way to install Contemply is using pip:

````
pip install contemply
````

Give it a testdrive:

````
contemply samples:class
````

## Documentation and support

You can find the documentation here: https://contemply.readthedocs.io/en/latest/

If you find any bugs or have a feature request, please create an issue on github: https://github.com/smertiens/contemply/issues

## Quickstart

### 1. Take your template file and add some Contemply magic

````python
# This is a demo file
#: classname = ask('How should the new class be called?')
#: text = ask('What should the text be?')
#: printVersion = yesno('Create the version function?', 'Yes')

#: version = '1.0.0'
#: setOutput('$classname.py')

class $classname:

    def someFunction(self):
        print('$text')

#: if printVersion == True
    def versionFunction(self):
        print('$version')
#: endif
````

Save this file as demo.pytpl

## 2. Run contemply

```
contemply demo.pytpl
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

