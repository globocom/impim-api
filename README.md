Dependencies
------------

- ElasticSearch
- Thumbor

Setup
-----

Install ElasticSearch (needs to be done manually).

Install Thumbor in its own virtualenv:

    make setup

Running
-------

Start dependencies and API server:

    make run

Tests
-----

Make sure dependencies are running, then:

    make test
