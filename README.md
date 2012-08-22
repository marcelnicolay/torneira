Torneira - Rapid Web Framework
======================

Torneira is a lightweight and rapid web framework build on top of [Tornado](http://www.tornadoweb.org/).
Its name came from the idea of getting rapid and fluid development.

Quick start
---------------------

To make an application with tornado you need create two files, settings.py and urls.py.
In settings.py you'll put your settings, and in urls.py you'll put your routes.

Install the latest version of torneira, go to your app directory and make:

    torneira --port 8888 --settings settings.py start

Torneira will be started at http://localhost:8888

I'm working in documentation and a demo application, to help people understand the idea of torneira.

There is already an application for [demonstration](https://github.com/marcelnicolay/torneira/tree/master/demo)

Installing
-----------------

    pip install torneira

Usage torneira script
-----------------------

    torneira --help

Contributing
------------

 Send a pull request (preferred) or patches using ``git format-patch``. Please,
 write unit and/or functional tests for your new feature.

Issues
------

Please report any issues via [github issues](https://github.com/marcelnicolay/torneira/issues)

Dependencies
--------------------

 * [Tornado](http://www.tornadoweb.org/)
 * [Mako](http://www.makotemplates.org/)
 * [SqlAlchemy](http://www.sqlalchemy.org/)
 * [simplexml](https://github.com/marcelnicolay/simplexml/)

 On Python 2.5, [simplejson](http://code.google.com/p/simplejson/).
