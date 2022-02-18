# Readme - OC-Projet-9 - LitReview

Le site LitReview a été développé à l'aide du Framework Django 4.0.1. 
LitReview est un site permettant à des utilisateurs de demander des critiques de livre au membre du site. 
Chaque utilisateur possède le droit de publier une critique ou d'ouvrir un nouveau ticket (Une demande de critique).
Il peut également répondre à un ticket en publiant sa propre critique. Une fois qu'une critique a été publiée en réponse 
à un ticket, ce dernier est clôturé et ne figure plus sur la page 'Tickets ouverts'.
Grâce à un système d'abonnement, l'utilisateur peut suivre les activités d'utilisateurs sélectionnés. Il peut ainsi
être tenu au courant des récentes publications dans son flux. Notez que le flux d'un utilisateur est également rempli de ses
propres publications. L'utilisateur peut effectuer toutes les opérations CRUD sur ses publications, sauf sur ses tickets fermés.


### Lancement de l'application :

Afin de lancer le programme, assurez-vous d'avoir préalablement créé et activé un environnement virtuel. Installez-les 
requirements à l'aide d'un `pip install requirements.txt`. Activez le serveur en entrant `python manage.py runserver` 
dans le dossier source, le repository `litreview`. Le serveur est maintenant en ligne, cliquer sur le lien affiché dans
votre terminal afin de vous rendre sur le site. 
Afin d'obtenir les droits d'administrateur créer vous un profil en entrant `python manage.py createsuperuser` ou utilisez
un compte déjà prévu à cet effet grâce au identifiant suivant : Login = `admingithub` Password = `githubmotdepasse`.


