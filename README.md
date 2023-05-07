# Projet Flask

##Présentation

Mon code permet la création d'un compte utilisateur, puis la connexion de ce compte dans ça propre page tâches qui lui permet de créer, modifier, supprimer et rechercher ces tâches grâce a un systeme de filtre.

## Fonctionnalité

Ce code contient un ensemble de fonctionnalités pour créer une application Web Flask qui permet de :

    Configurer une base de données SQLite à l'aide de SQLAlchemy.
    Créer un modèle de données pour les utilisateurs et les tâches, qui est utilisé pour définir les colonnes de la table.
    Initialiser la base de données avec la fonction init_db().
    Définir plusieurs routes pour différentes pages de l'application.
    Créer une session utilisateur pour stocker des informations sur l'utilisateur connecté.
    Créer un formulaire de connexion pour permettre à l'utilisateur de se connecter à son compte.
    Créer un formulaire de création de compte pour permettre à un utilisateur de créer un compte.
    Créer un formulaire de création de tâche pour permettre à l'utilisateur de créer une nouvelle tâche associée à son compte.
    Afficher une liste de tâches pour l'utilisateur connecté avec la possibilité de rechercher une tâche spécifique.
    Effectuer des opérations de lecture et d'écriture dans la base de données pour stocker et récupérer des informations utilisateur et de tâches.

Ces fonctionnalités sont mises en œuvre en utilisant les modules Flask, render_template, request, redirect, url_for et session. Le code utilise également le module SQLAlchemy pour configurer et accéder à la base de données SQLite.
## Technologies
— Python et Flask pour le développement de l’application web.

— SQLAlchemy pour la gestion de la base de données.

— Flask-RESTful pour la création de l’API RESTful.

— HTML, CSS et JavaScript pour la création de l’interface utilisateur.

## Outils


Pour mon fichier app.py j'ai du prendre des cours suplémentaires a cause de mon manque de connaissance de la technologie Flask, je donnes alors les liens qui mon permis de rattraper mon retard et accompagner le long de ce projet:

https://www.youtube.com/watch?v=m2CCki_APxE

https://www.youtube.com/watch?v=2Zz97NVbH0U

https://www.youtube.com/watch?v=bxyaJ8w_wak

https://www.youtube.com/watch?v=4bccU9eMrkw

J'ai aussi utilisé ChatGPT pour corrigé la structure de mon code qui pouvait étre erroné par example je donnais des noms spécifique a mes variables ce qui ne me posait pas de probléme mais au fur et a mesure j'ai était bloqué a cause cela.
En plus c'es plus facil de suivre un cours sur internet en tout en travaillant sur un projet quand nos variables on le méme nom.
## Utilisation
Il faut penser a importer les librairies Flask et SQLAlchemy pour utilsé ce code.

Penser a donner une varriable a FLASK_APP pour lui permettre de chargé l'application Flask.

Si tout est bon vous pourrez executer un Flask run et normalement l'application devrait ce lancé correctement.

Je vous recommande d'utiliser un environnement virtuel et d'avoir le fichier .py pas loins des templates .

(Aussi il faut double clic sur le bouton créer)
## Auteur
Boudry Tom

## Bonus 

La barre de recherche permet le trie par ordre alphabétique des tâches créer.
