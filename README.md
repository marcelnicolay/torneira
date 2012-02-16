Torneira - Rapid Web Framework
======================

Torneira is a lightweight and rapid web framework build on top of [Tornado](http://www.tornadoweb.org/).
Its name came from the idea of getting rapid and fluid development.

Quick start
---------------------

To make an application with tornado you need create two files, settings.py and urls.py.
In settings.py you'll put your settings, and in urls.py you'll put your routes.

Install the latest version of torneira, go to your app directory and make:

$ torneira --port 8888 --settings settings.py start

Torneira will be started at http://localhost:8888

I'm working in documentation and a demo application, to help people understand the idea of torneira.

There is already an application for [demonstration](https://github.com/marcelnicolay/torneira/tree/master/demo)

Installing
-----------------

pip install torneira

Contributing
--------------------

 1. Create both unit and functional tests for your new feature
 2. Do not let the coverage go down, 100% is the minimum.
 3. Write properly documentation
 4. Send-me a patch with: ``git format-patch``

Issues
------

Please report any issues via [github issues](https://github.com/marcelnicolay/torneira/issues)

Dependencies
--------------------

 * [Tornado](http://www.tornadoweb.org/)
 * [Mako](http://www.makotemplates.org/)
 * [SqlAlchemy](http://www.sqlalchemy.org/)
 * [simplejson](http://code.google.com/p/simplejson/)
 * [simplexml](https://github.com/marcelnicolay/simplexml/)
 * [routes](http://routes.groovie.org)