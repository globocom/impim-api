Impim API [![Build Status](https://secure.travis-ci.org/globocom/impim-api.png)](http://travis-ci.org/globocom/impim-api)
=========

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

License
-------

Impim API is licensed under the MIT License:

> The MIT License

> Copyright (c) 2012 globo.com <lambda@corp.globo.com>

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
