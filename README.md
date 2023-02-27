# Judilibre Public Monitor

Cette application permet de suivre les données publiées en Open Data par la cour de cassation sur l'API Judilibre. Ceci n'est pas une application officielle de la cour de cassation.

## Fonctionnement

### Version de Python

Pour lancer l'application, il faut une version récente de Python. La version utilisée pendant le développement de l'application est Python 3.10.

### Librairies

Les librairies ainsi que les versions pour lancer l'application sont contenues dans le fichier `requirements.txt`. Pour installer ces librairies, on peut lancer la commande suivante:

```sh
python -m pip install -r requirements.txt
```

Le fichier `requirements-dev.txt` contient, lui, les librairies utilisées pendant le développement de l'application.

### Lancement de l'application

Pour lancer l'application, il suffit d'exécuter la commande suivante:

```sh
python main.py
```

On peut spécifier le port sur lequel l'application tournera avec `--port` ou `-p`. On peut aussi activer le mode `debug` en ajoutant l'argument `--debug-mode` ou `-d`.

### Docker

Pour simplifier la gestion de l'environnement, on peut utiliser Docker pour lancer l'application.

Pour créer l'image Docker, il faut exécuter la commande suivante:

```sh
docker image build . -t judilibre-public-monitor:latest
```

Une fois créé, on peut lancer l'application en faisant:

```sh
docker container run -p 9999:9999 judilibre-public-monitor:latest
```

## Données

Les données utilisées par l'application sont stockées dans le dossier [data](/judilibre-public-monitor/data) de même que certains utilitaires pour générer de fausses données ou pour télécharger les données existantes.

### Téléchargement de l'historique des données

Le téléchargment des données n'est pas simple à cause des limitations de l'API Judilibre. Il faut en effet trouver une bonne solution entre le nombre de requêtes faites à l'API et la limitation de 10 000 décisions par requête. Le fichier `full_data.parquet` contient beaucoup des décisions déja disponible dans l'application mais on peut souhaiter faire son propre extract de données.

Les fonctions contenues dans le fichier [`download_historic_data.py`](/judilibre-public-monitor/data/download_historic_data.py) sont pensées pour limiter le nombre de requêtes faites à l'API.

## Mise à jour des données
