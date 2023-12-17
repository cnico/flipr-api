Flipr Python API REST Client
============================
Client Python pour l'API Flipr. | Python client for Flipr API.

|PyPI| |GitHub Release| |Python Version| |License| |Black|

|Read the Docs| |Codecov| |GitHub Activity|


.. |PyPI| image:: https://img.shields.io/pypi/v/flipr-api
   :target: https://pypi.org/project/flipr-api/
   :alt: PyPI
.. |GitHub Release| image:: https://img.shields.io/github/release/cnico/flipr-api.svg
   :target: https://github.com/cnico/flipr-api/releases
   :alt: GitHub Release
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/flipr-api
   :target: https://pypi.org/project/flipr-api/
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/flipr-api
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/flipr-api/latest.svg?label=Read%20the%20Docs
   :target: https://flipr-api.readthedocs.io/
   :alt: Read the documentation at https://flipr-api.readthedocs.io/
.. |Codecov| image:: https://codecov.io/gh/cnico/flipr-api/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/cnico/flipr-api
   :alt: Codecov
.. |GitHub Activity| image:: https://img.shields.io/github/commit-activity/y/cnico/flipr-api.svg
   :target: https://github.com/cnico/flipr-api/commits/master
   :alt: GitHub Activity
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

You will find English README content in the section `For English speaking users`_.

Vous trouverez le contenu francophone du README dans la section `Pour les francophones`_.

Pour les francophones
---------------------

Description
^^^^^^^^^^^

Flipr est un objet connecté que l'on met dans sa piscine pour mesurer en continu les valeurs chimiques de celle-ci.
Ce package Python permet de gérer la communication avec l'API REST publique `Flipr <https://apis.goflipr.com/Help>`_.

Le client permet de :
* Récupérer l'id de votre flipr.
* Accéder à la mesure la plus récente de votre Flipr (données de température, ph, chlore et redox).

Pour utiliser le client, il vous faudra disposer de vos identifiants et mot de passe Flipr créés avec l'application mobile.

Ce package a été développé avec l'intention d'être utilisé par `Home-Assistant <https://home-assistant.io/>`_
mais il peut être utilisé dans d'autres contextes.

Installation
^^^^^^^^^^^^

Pour utiliser le module Python ``flipr_api`` vous devez en premier installer
le package en utilisant pip_ depuis PyPI_:

.. code:: console

   $ pip install flipr-api


Vous pouvez trouver un exemple d'usage en regardant
`le test d'intégration <tests/test_integrations.py>`_.

Vous pouvez également faire un test direct de l'API REST en suivant l'exemple `testing_api.rst`_.

Contribuer
^^^^^^^^^^

Les contributions sont les bienvenues. Veuillez consulter les bonnes pratiques
détaillées dans `CONTRIBUTING.rst`_.


For English speaking users
--------------------------

Description En
^^^^^^^^^^^^^^

Flipr is a connect object that you put in your swimming pool in order to measure chemical values of it.
This Python package allows to communicate with the public REST API `Flipr <https://apis.goflipr.com/Help>`_.

This client allows to :
* Retrieve the id of your flipr
* Get the latest measure of your Flipr (data of temperature, ph, chlorine and redox).

To use this client, it requires you have your login and password created with Flipr's mobile application.

This package has been developed to be used with `Home-Assistant <https://home-assistant.io/>`_
but it can be used in other contexts.

Installation
^^^^^^^^^^^^

To use the ``flipr_api`` Python module, you have to install this package first via
pip_ from PyPI_:

.. code:: console

   $ pip install flipr-api

You will find an example ot usage in a Python program in the `integration test <tests/test_integrations.py>`_.

You can test directly the flipr API following the given sample `testing_api.rst`_.

Contributing
^^^^^^^^^^^^

Contributions are welcomed. Please check the guidelines in `CONTRIBUTING.rst`_.


Credits
-------

This project was inspired from the MeteoFranceAPI_ HACF project.

.. _MeteoFranceAPI: https://github.com/hacf-fr/meteofrance-api
.. _PyPI: https://pypi.org/
.. _pip: https://pip.pypa.io/
.. _CONTRIBUTING.rst: CONTRIBUTING.rst
