Releasing
=========

1. Increment the version in ``consumer/__init__.py``

2. Update the ``CHANGELOG.rst`` using:

.. code-block:: console

   $ git log --pretty=format:'  * %h - %s (%an, %ad)' vX.Y.Z..HEAD

3. Add files to git:

.. code-block:: console

   $ git add CHANGELOG.rst  consumer/__init__.py

4. Commit

.. code-block:: console

   $ git commit -m "Releasing version X.Y.Z"

5. Tag

.. code-block:: console

   $ git tag -a vX.Y.Z -m "Releasing version X.Y.Z"
   $ git push origin main --tags

6. Wait until travis has run and the new tag is available at https://github.com/sergeyklay/consumer-pact-example/releases/tag/vX.Y.Z

7. Set the title to ``vX.Y.Z``

8. Save
