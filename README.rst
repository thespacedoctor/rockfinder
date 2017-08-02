rockfinder 
=========================

.. image:: https://readthedocs.org/projects/rockfinder/badge/
    :target: http://rockfinder.readthedocs.io/en/latest/?badge
    :alt: Documentation Status

.. image:: https://cdn.rawgit.com/thespacedoctor/rockfinder/master/coverage.svg
    :target: https://cdn.rawgit.com/thespacedoctor/rockfinder/master/htmlcov/index.html
    :alt: Coverage Status

*A python package and command-line tools for A python package and command-line suite to generate solar-system body ephemerides and to determine if specific transient dections are in fact known asteroids*.





Command-Line Usage
==================

.. code-block:: bash 
   
    
    Usage:
        rockfinder where [-e] [csv|md|rst|json|yaml] <objectId> <mjd>...
    
        csv                   output results in csv format
        md                    output results as a markdown table
        rst                   output results as a restructured text table
        json                  output results in json format
        yaml                  output results in yaml format
        -e, --extra           return extra ephemeris info (verbose)
        -h, --help            show this help message
    

Documentation
=============

Documentation for rockfinder is hosted by `Read the Docs <http://rockfinder.readthedocs.org/en/stable/>`__ (last `stable version <http://rockfinder.readthedocs.org/en/stable/>`__ and `latest version <http://rockfinder.readthedocs.org/en/latest/>`__).

Installation
============

The easiest way to install rockfinder is to use ``pip``:

.. code:: bash

    pip install rockfinder

Or you can clone the `github repo <https://github.com/thespacedoctor/rockfinder>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/rockfinder.git
    cd rockfinder
    python setup.py install

To upgrade to the latest version of rockfinder use the command:

.. code:: bash

    pip install rockfinder --upgrade


Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

.. code:: bash

    git clone git@github.com:thespacedoctor/rockfinder.git
    cd rockfinder
    python setup.py develop

`Pull requests <https://github.com/thespacedoctor/rockfinder/pulls>`__
are welcomed!

Sublime Snippets
~~~~~~~~~~~~~~~~

If you use `Sublime Text <https://www.sublimetext.com/>`_ as your code editor, and you're planning to develop your own python code with rockfinder, you might find `my Sublime Snippets <https://github.com/thespacedoctor/rockfinder-Sublime-Snippets>`_ useful. 

Issues
------

Please report any issues
`here <https://github.com/thespacedoctor/rockfinder/issues>`__.

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
