.. _intro:

Fuel-CI Introduction
====================

The main idea of artifact-based build system (even if it can solve many
kinds of tasks) is to build an artifact (which should be thinked of as an
abstract binary file with some metadata) based on its dependencies and
to publish it into some storage to use in future builds. This helps to
avoid rebuilding all parts of the project from the beginning (dependencies
can already be downloaded), simplifying and speeding up the whole building
process.

Building of the code with Fuel-CI includes two phases:

- Writing data YAML including objects build system will deal with
- Passing created YAML to command line `fci` script

Let's assume you want to build a Python package from the repo and upload it
as an artifact into some storage for future use. An example of data YAML
can look like this:

.. code-block:: yaml

    scenario:
      - build_package

    repositories:
      fuel_web:
        url: "https://github.com/stackforge/fuel-web.git"
        path: "fuel-web"
        package_path: "fuel-web/nailgun"

    packages:
      robots:
        drivers:
          package: "python_package"

    artifact_storages:
      local_storage:
        drivers:
          storage: "localfs"
        url: "test_storage"

    build_artifacts:
      nailgun:
        version: "0.1"
        description: "Nailgun API service"
        storage: "local_storage"
        packed: true


Let's go step by step.

.. code-block:: yaml

    scenario:
      - build_package

This is a scenario you wish to execute. It is one of the default scenarios (:meth:`fuel_ci.scenarios.build_package`) supported bu Fuel-CI. By default `build()` method (or "stage") is executed, but you can specify your own stage to call in specified scenario, like this:

.. code-block:: yaml

    scenario:
      - my_module.my_stage

After you specified scenario to run, you should describe objects scenario
will be dealing with during building process.

.. code-block:: yaml

    repositories:
      fuel_web:
        url: "https://github.com/stackforge/fuel-web.git"
        path: "fuel-web"
        package_path: "fuel-web/nailgun"

This is a description for a Repository object (:class:`fuel_ci.objects.repo.Repository`).
**fuel-web** here is an object name to simplify finding it inside
parsed YAML. **url** is an url to repository. By default Git driver
(:meth:`fuel_ci.drivers.cvs.git`) is used, but you can specify any other
driver to use for checking out the repository, if it's present e.g.:

.. code-block:: yaml

    repositories:
      fuel_web:
        drivers:
          cvs: "svn"
        url: "svn+ssh://username@hostname/fuel-web"
        path: "fuel-web"
        package_path: "fuel-web/nailgun"

**path** is a local path to checkout repository to, and **package_path** is
an internal path to directory inside cloned repo to use as a working dir
while building package.

.. code-block:: yaml

    packages:
      fuel-web:
        drivers:
          package: "python_package"

This is a description for a Package object (:class:`fuel_ci.objects.package.Package`).
As you can see, the only thing we're doing here is specifying which driver
to use while building package. In this example we're dealing with Python
package.

.. code-block:: yaml

    artifact_storages:
      local_storage:
        drivers:
          storage: "localfs"
        url: "test_storage"

This is a description for an ArtifactStorage object (:class:`fuel_ci.objects.artifact_storage.ArtifactStorage`).
In this case it will use "localfs" storage driver and **url** points to
some local path where storage keeps its artifacts.

.. code-block:: yaml

    build_artifacts:
      nailgun:
        version: "0.1"
        description: "Nailgun API service"
        storage: "local_storage"
        packed: true

This is a description for an Artifact object (:class:`fuel_ci.objects.artifact.Artifact`), which will be built as a result.
We're specifying name of the storage to use in a **storage** attribute (by
default first storage in list will be used). Also we specify that artifact
doesn't require to be packed (as it will be Python package already represented as "tar.gz" archive).

Now you can take a look at :meth:`fuel_ci.scenarios.build_package` for
description what will be done with these objects according to chosen
scenario.
