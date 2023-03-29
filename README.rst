.. raw:: html

    <h1 align="center">Consumer API Example</h1>
    <p align="center">
        <a href="https://github.com/sergeyklay/consumer-pact-example/actions/workflows/test-code.yaml">
            <img src="https://github.com/sergeyklay/consumer-pact-example/actions/workflows/test-code.yaml/badge.svg" alt="Test Code" />
        </a>
        <a href="https://codecov.io/gh/sergeyklay/consumer-pact-example">
            <img src="https://codecov.io/gh/sergeyklay/consumer-pact-example/branch/main/graph/badge.svg?token=9FdBH27I9K" alt="Coverage Status" />
        </a>
    </p>

.. teaser-begin

This is a Python application for explanation of Contract Testing based on
`Pact <https://docs.pact.io>`_.

Here you can find out how to use Pact using the Python language. You can find
more of an overview on Pact in the `Pact Introduction <https://docs.pact.io/>`_.

This project uses:

* `Pact <https://pact.io>`_, a code-first tool for testing HTTP and message
  integrations using contract tests
* `pact-python <https://github.com/pact-foundation/pact-python>`_, to create
  and verify consumer driven contracts

.. teaser-end

.. image:: https://raw.githubusercontent.com/sergeyklay/consumer-pact-example/main/cdc-example.png
  :alt: Interaction diagram

Consumer (this project)
=======================

Consumer API Example is a simple HTTP client that makes requests to Provider,
gets response from API server and creates data model using the data from
responses. For demonstration purposes, the project has simplified
logic and should not be considered as a full-fledged Production-ready solution.

Provider
========

For the purity of the experiment, the provider is implemented as a separate
project and can be found at
`the following repo <https://github.com/sergeyklay/provider-pact-example>`_.

Pact
====

Sample contracts (pacts) are located in
`tests/pacts <https://github.com/sergeyklay/consumer-pact-example/tree/main/tests/pacts>`_.

Getting Started
===============

Prerequisites
-------------

What kind of things you need to install on your workstation to start:

* Python >= 3.11
* Docker / Rancher
* Docker Compose / Rancher Compose

Installing
----------

First, install Python dependencies for consumer:

.. code-block:: console

   $ make init
   $ make install

Run tests
---------

To run unit tests use the command as follows:

.. code-block:: console

   $ make test

Run the dockerized broker using the ``docker-compose.yml`` file in the root of
the project:

.. code-block:: console

   $ docker compose -d


To publish contracts (pacts) to the broker use the following command:

.. code-block:: console

   $ ./publish-contracts.sh

Run lint check
--------------

To run code style checking use the command as follows:

.. code-block:: console

   $ make lint


.. -project-information-

Project Information
===================

Consumer API Example is released under the `MIT License <https://choosealicense.com/licenses/mit/>`_,
and its code lives at `GitHub <https://github.com/sergeyklay/consumer-pact-example>`_.
It’s rigorously tested on Python 3.11+.

If you'd like to contribute to Consumer API Example you're most welcome!

.. -support-

Support
=======

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the Consumer API Example, please
`open an issue <https://github.com/sergeyklay/consumer-pact-example/issues>`_.


