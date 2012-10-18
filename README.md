Images API [![Build Status](https://secure.travis-ci.org/globocom/images-api.png)](http://travis-ci.org/globocom/impim-api)
==========

API for managing images.

Dependencies
------------

- [ElasticSearch](http://www.elasticsearch.org/)
- [Thumbor](https://github.com/globocom/thumbor)

Setup
-----

Install ElasticSearch (needs to be done manually).

Install Thumbor in its own virtualenv and install python dependencies from requirements files:

    make setup

Update python dependencies from requirements files:

    make requirements

Running
-------

Start dependencies and API server:

    make run

Tests
-----

Make sure dependencies are running, then:

    make test
