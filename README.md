# Contemply

[![Build Status](https://travis-ci.org/smertiens/contemply.svg?branch=develop)](https://travis-ci.org/smertiens/contemply)
[![Documentation Status](https://readthedocs.org/projects/contemply/badge/?version=latest)](https://contemply.readthedocs.io/en/latest/?badge=latest)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/smertiens/contemply.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/smertiens/contemply/context:python)
[![PyPI version](https://badge.fury.io/py/contemply.svg)](https://badge.fury.io/py/contemply)

A code generator that creates boilerplate files from templates.

All the questions necessary to interactively create a file from your template are embedded in the template itself,
so all you need is Contemply and your template file to get up and running.

The project is in early beta right now, you can help by creating an issue on github for bugs or feature requests. 
Contributors are always welcome! 

## Installation

The easiest way to install Contemply is using pip:

````
pip install contemply
````

## Documentation and support

You can find the documentation here: https://contemply.readthedocs.io/en/latest/

If you find any bugs or have a feature request, please create an issue on github: https://github.com/smertiens/contemply/issues

## Quickstart

### 1. Take your template file and add some Contemply magic

````python
# This is a demo file
#: ask('How should the new class be called? ', 'ClassName')
#: ask('What should the text be? ', 'mytext')
#: yesno('Create the version function?', 'printVersion', 'Yes')

#: version = '1.0.0'
#: output('$classname.py')

class $ClassName:

    def someFunction(self):
        print('$mytext')

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

