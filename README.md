# Contemply

[![Build Status](https://travis-ci.org/smertiens/contemply.svg?branch=master)](https://travis-ci.org/smertiens/contemply)


A code generator that creates boilerplate files from templates.

All the questions necessary to interactively create a file from your template are embedded in the template itself,
so all you need is Contemply and your template file to get up and running.

## Installation

The easiest way to install Contemply is using pip:

````
pip install contemply
````

## Documentation and support



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
Print the super function? [Yes]: No
```

## 3. Take a look at your outputfile

Called MyClass.py:

````python
# This is a demo file

class MyClass:

    def someFunction(self):
        print('Hello World')
````

