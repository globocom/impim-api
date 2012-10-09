Images API
==========

API for handling images.

Dependencies
------------

- ElasticSearch
- Thumbor

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
