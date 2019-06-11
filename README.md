# Modèle de TP pour étudiants (privé)

Ce repo contient un modèle pour organiser un TP à faire par les étudiants avec la contrainte d'utiliser le gitlab de l'école. Il est constitué des fichiers privés de l'enseignant ainsi que d'un script python pour récupérer tous les forks des étudiants du repo public, ce dernier étant un repository git à part entière et submodule du premier.

La syntaxe du script est la suivante :
```bash
python3 clone_all.py <token> <project_id>
```
Vous pouvez générer un `token` [sur cette page](https://gitedu.hesge.ch/profile/personal_access_tokens), en cochant la case "api". Le `project_id` correspond à celui affiché sur la page de repo :
![image](project_id.png)

Le script clone tous les forks du repository public et les place dans le répertoire `repositories`.