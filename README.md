# Description de l'application

Ce projet consiste a développer une API sécurisée pour une application de suivi de 
développement logiciel.En utilisant Django REST Framework et l'utilisation des JSON Web Token (JWT) pour gérer l'authentification.

## Lancement de l'application

* Ouvrez un invite de commande
* Placez-vous dans le dossier contenant le répertoire OC10
* Création de l'environnement virtuel : ```python -m venv env```
* Activation de l'environnement virtuel :
    * Pour Windows : ```env\Scripts\activate.bat```
    * Pour Linux   : ```env/bin/activate```
* Installation des dépendances : ```pip install -r requirements.txt```
* Placez-vous dans le dossier contenant manage.py
* Lancement du serveur local : ```python manage.py runserver```
* Ouvrez votre navigateur web a l'url : ```http://127.0.0.1:8000/```

## Ensemble des requetes geré par l'API

* Register User
* Login User
* Create User Project
* List User Projects
* Retrieve Project
* Update Project
* Delete Project
* Create Contributor
* List Project Users (Contributors)
* Delete Contributor
* Create Issue Project
* List Issues Project
* Update Issue Project
* Delete Issue Project
* Create Comment Issue
* List Comments Issue
* Update Comment Issue
* Retrieve Comment Issue
* Delete Comment Issue

L'ensemble des points de terminaison des requetes ci-dessus sont accéssible via la documentation
de l'API : https://documenter.getpostman.com/view/16912752/UUxtEVwm
