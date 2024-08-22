# Flipr Python API REST Client

Client Python pour l'API Flipr. | Python client for Flipr API.

[![PyPi](https://img.shields.io/pypi/v/flipr-api)](https://pypi.org/project/flipr-api/)
[![GitHub Release](https://img.shields.io/github/release/cnico/flipr-api.svg)](https://github.com/cnico/flipr-api/releases)
[![Python Version](https://img.shields.io/pypi/pyversions/flipr-api)](https://pypi.org/project/flipr-api/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Read the docs](https://img.shields.io/readthedocs/flipr-api/latest.svg?label=Read%20the%20Docs)](https://flipr-api.readthedocs.io/)
[![Codecov](https://codecov.io/gh/cnico/flipr-api/branch/main/graph/badge.svg)](https://codecov.io/gh/cnico/flipr-api)
[![Github Activity](https://img.shields.io/github/commit-activity/y/cnico/flipr-api.svg)](https://github.com/cnico/flipr-api/commits/master)

You will find English README content in the section [For English speaking users](#for-english-speaking-users).

Vous trouverez le contenu francophone du README dans la section [Pour les francophones](#pour-les-francophones).

## Pour les francophones

### Description

Flipr est un objet connecté que l'on met dans sa piscine pour mesurer en continu les valeurs chimiques de celle-ci.
Ce package Python permet de gérer la communication avec l'API REST publique [Flipr API](https://apis.goflipr.com/Help).

Le client permet de :

- Récupérer l'id de votre flipr.
- Accéder à la mesure la plus récente de votre Flipr (données de température, ph, chlore et redox).

Pour utiliser le client, il vous faudra disposer de vos identifiants et mot de passe Flipr créés avec l'application mobile.

Ce package a été développé avec l'intention d'être utilisé par [Home-Assistant](https://home-assistant.io/) mais il peut être utilisé dans d'autres contextes.

### Installation

Pour utiliser le module Python **flipr_api** vous devez en premier installer le package en utilisant [pip](https://pip.pypa.io/) depuis [PyPI](https://pypi.org/):

```console
   pip install flipr-api
```

Vous pouvez trouver un exemple d'usage en regardant [le test d'intégration](https://github.com/cnico/flipr-api/blob/main/tests/test_integrations.py).

Vous pouvez également faire un test direct de l'API REST en suivant l'exemple [testing_api.md](https://github.com/cnico/flipr-api/blob/main/testing_api.md).

### Contribuer

Les contributions sont les bienvenues. Vous pouvez ouvrir une pull request.

## For English speaking users

### Description english

Flipr is a connect object that you put in your swimming pool in order to measure chemical values of it.
This Python package allows to communicate with the public REST API [Flipr API](https://apis.goflipr.com/Help).

This client allows to :

- Retrieve the id of your flipr
- Get the latest measure of your Flipr (data of temperature, ph, chlorine and redox).

To use this client, it requires you have your login and password created with Flipr's mobile application.

This package has been developed to be used with [Home-Assistant](https://home-assistant.io/) but it can be used in other contexts.

### Installation english

To use the **flipr_api** Python module, you have to install this package first via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```console
   pip install flipr-api
```

You will find an example ot usage in a Python program in the [le test d'intégration](https://github.com/cnico/flipr-api/blob/main/tests/test_integrations.py).

You can test directly the flipr API following the given sample [testing_api.md](https://github.com/cnico/flipr-api/blob/main/testing_api.md).

### Contributing

Contributions are welcomed. You can open pull requests.

## Credits

This project was inspired from the [MeteoFranceAPI](https://github.com/hacf-fr/meteofrance-api) HACF project.
