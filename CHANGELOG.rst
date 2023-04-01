Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

1.1.0 (2023-04-01)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Migrated provider API v2.
* Moved docker-compose.yml to the project root.


Features
^^^^^^^^

* Provided ability to delete product and cover this feature by contract tests.
* Provided ability to get list of products and cover this feature by contract tests.
* Provide test and delete for get non-existent product.
* Extended matchers for testing purposes.
* Added more contract tests and examples for education purposes.
* Provided brand new http client.
* Used marshmallow for data deserialization.


Improvements
^^^^^^^^^^^^

* Tuned pact participant version number format.
* Cleaned CLI options when publishing pacts.
* Removed no longer needed nginx from docker compose file.


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Improved project documentation.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Provided Labeler GitHub Action.
* Setup code lint at CI phase.
* Setup unit testing at CI phase.
* Improve coverage configuration.
* Moved ``pylint`` and ``flake8`` configs to ``setup.cfg``.
* Bumped ``coverage[toml]`` from 7.2.0 to 7.2.1.
* Bumped ``pylint`` from 2.16.2 to 2.17.1.
* Bumped ``pytest`` from 7.2.1 to 7.2.2.


Bug Fixes
^^^^^^^^^

* Fixed database seeder to not try to create tables twice.


----


1.0.0 (2023-02-26)
------------------

Features
^^^^^^^^

* Initial release


----
