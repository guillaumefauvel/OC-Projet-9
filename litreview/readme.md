# Readme - OC-Projet-9 - LitReview

*Le site LitReview a été développé à l'aide du Framework Django 4.0.1.*

---


LitReview est un site permettant à des utilisateurs de demander des critiques de livre au membre du site.  
Chaque utilisateur possède le droit de publier une critique ou d'ouvrir un nouveau ticket (Une demande de critique).  
Il peut également répondre à un ticket en publiant sa propre critique. Une fois qu'une critique a été publiée en réponse  
à un ticket, ce dernier est clôturé et ne figure plus sur la page 'Tickets ouverts'.

Grâce à un système d'abonnement, l'utilisateur peut suivre les activités d'utilisateurs sélectionnés.  
Il peut ainsi être tenu au courant des récentes publications dans son flux.  Notez que le flux d'un utilisateur est également  
rempli de ses propres publications. L'utilisateur peut effectuer toutes les opérations CRUD sur ses publications, sauf sur ses tickets fermés.

---

## Lancement de l'application :


1. Afin de lancer le programme, assurez-vous d'avoir préalablement créé et activé un **environnement virtuel**.

    - Vérifiez que votre version de python est supérieure ou égale à la 3.3. Tapez `python --version` dans le terminal pour  
      vérifier que vous possédez cette fonctionnalité. 
    - Si vous ne savez pas initialiser un environnement virtuel référez-vous à ce [lien](https://openclassrooms.com/fr/courses/6951236-mettez-en-place-votre-environnement-python/7014018-creez-votre-premier-environnement-virtuel) :
    - Si vous utilisez le PowerShell, au moment d'activer l'environnement virtuel utiliser la commande : `env/scripts/activate.ps1` 


2. Une fois l'environnement virtuel activé, installez-les requirements à l'aide d'un `pip install requirements.txt`.  
Activez le serveur en entrant `python manage.py runserver` dans le dossier source, le repository `litreview`.
   

3. Le serveur est maintenant en ligne, cliquer sur le lien affiché dans votre terminal afin de vous rendre sur le site. 


4. Afin d'obtenir les droits d'administrateur créer vous un profil en entrant `python manage.py createsuperuser` ou utilisez
un compte déjà prévu à cet effet grâce au identifiant suivant : Login = `admingithub` Password = `githubmotdepasse`.


---

