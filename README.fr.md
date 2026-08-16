# 🔮 Nostradamus

### Un moteur déterministe de prédiction de rencontres sportives

**Nostradamus** est un projet de prédiction sportive conçu pour prédire **quelles équipes ou quels joueurs se rencontreront au cours d'une compétition**.

Contrairement aux modèles traditionnels de prédiction sportive, Nostradamus ne cherche pas principalement à prédire les vainqueurs des matchs. Son objectif est d'anticiper la structure des rencontres à venir à partir des règles officielles des compétitions, des données disponibles et de mécanismes de prédiction déterministes.

Le projet porte le nom de **Michel de Nostredame (Nostradamus)**, médecin et apothicaire français surtout connu pour ses prophéties. Cette fois-ci, cependant, les prédictions de Nostradamus reposent sur les données, le raisonnement mathématique, les règles officielles et des méthodes reproductibles.

---

## 🎯 Objectif

L'objectif principal de Nostradamus est de prédire les **rencontres potentielles au sein de compétitions sportives comportant un tirage au sort ou un mécanisme similaire**.

Le projet se concentre actuellement sur deux sports :

- ⚽ **Football masculin**
- 🎾 **Tennis féminin**

L'objectif n'est pas simplement de générer des prédictions indépendantes. Nostradamus doit produire des **prédictions globalement cohérentes**, respectant les règles et les contraintes structurelles de chaque compétition.

---

## 🌍 Périmètre du projet

Nostradamus se concentre sur les compétitions pour lesquelles au moins un tirage au sort est réalisé.

### ⚽ Football

La partie football se concentre initialement sur les grandes compétitions internationales comportant un tirage au sort.

Le périmètre actuel comprend :

- UEFA Champions League
- Coupe d'Afrique des Nations (CAN)
- Championnat d'Europe de l'UEFA (EURO)
- Coupe du Monde de la FIFA

La première compétition ciblée par Nostradamus est la **Ligue des Champions de l'UEFA**.

Pour la phase de ligue de la Ligue des Champions, Nostradamus vise à prédire les huit adversaires que chacune des 36 équipes participantes rencontrera, ainsi que la configuration domicile/extérieur.

À l'issue de la phase de ligue, le projet pourra également prédire les parcours potentiels lors des phases à élimination directe à partir du classement final et des tirages suivants.

### 🎾 Tennis féminin

La partie tennis se concentre sur les principaux tournois **WTA** comportant un tirage au sort.

Le périmètre initial comprend :

- Tournois WTA 500
- Tournois WTA 1000
- Tournois du Grand Chelem

Pour chaque tournoi, Nostradamus vise à prédire les premières rencontres ainsi que les parcours potentiels dans le tournoi.

La partie tennis pourra notamment prendre en compte :

- les changements de classement
- les forfaits de joueuses
- les wildcards
- les autres changements pertinents survenant avant le tirage

---

## ⚙️ Fonctionnement de Nostradamus

Nostradamus est conçu pour fonctionner comme une personne réalisant un tirage au sort tout en respectant l'ensemble des règles applicables à la compétition.

### Football

Pour la phase de ligue de la Ligue des Champions, Nostradamus vise à :

1. Identifier les équipes participantes.
2. Déterminer les informations et contraintes pertinentes de la compétition.
3. Générer une prédiction des huit adversaires de chaque équipe.
4. Déterminer la configuration domicile/extérieur.
5. Vérifier que l'ensemble de la prédiction est globalement cohérent.
6. Après la phase de ligue, utiliser le classement final et les informations des tirages suivants afin de générer les parcours potentiels des phases à élimination directe.

### Tennis féminin

Pour chaque tournoi sélectionné, Nostradamus vise à :

1. Identifier les participantes attendues.
2. Prendre en compte les informations de classement pertinentes.
3. Prendre en compte les forfaits, wildcards et autres changements pertinents.
4. Générer une prédiction des premières rencontres.
5. Générer les parcours potentiels des joueuses dans le tournoi.

---

## 🧠 Principes fondamentaux

### Prédictions déterministes

Nostradamus est conçu pour être **déterministe**.

À partir du même jeu de données, des mêmes paramètres et des mêmes règles, Nostradamus doit produire **la même prédiction**.

Une nouvelle prédiction ne doit être générée que lorsqu'une information pertinente modifie les données ou les paramètres disponibles pour le système.

Ce principe est conceptuellement similaire à l'utilisation d'un `random_state` fixe dans une expérience de machine learning : des entrées identiques doivent produire des sorties identiques.

L'objectif n'est donc pas de générer une prédiction différente à chaque exécution du programme, mais de produire **une prédiction reproductible pour un état donné des informations disponibles**.

### Principe de cohérence des tirages

Nostradamus respecte un **principe de cohérence des tirages**.

Une rencontre prédite ne peut pas être considérée indépendamment de la prédiction réalisée pour l'adversaire.

Par exemple, si Nostradamus prédit :

> Paris Saint-Germain → Liverpool, 4e journée, domicile

alors la prédiction correspondante doit automatiquement être :

> Liverpool → Paris Saint-Germain, 4e journée, extérieur

La prédiction complète doit donc rester **globalement cohérente**.

Ce principe est fondamental pour Nostradamus : le système ne génère pas une collection de prédictions indépendantes, mais **une prédiction cohérente de la structure de la compétition**.

### Règles officielles des compétitions

Nostradamus repose sur les règles officielles qui régissent chaque compétition.

Les contraintes propres à chaque compétition constituent des exigences fondamentales du processus de prédiction.

L'utilisation du machine learning ne sera envisagée que lorsqu'elle apporte une réelle valeur au problème de prédiction. Nostradamus n'a pas vocation à utiliser du machine learning simplement pour utiliser du machine learning.

### Explicabilité

Nostradamus vise à produire des résultats **compréhensibles et accessibles**, plutôt que des prédictions opaques.

Les prédictions finales doivent donc être présentées de manière claire et lisible.

---

## 🔮 Vision à long terme

À long terme, Nostradamus a pour objectif de devenir un **moteur de prédiction sportive** capable de suivre en continu les informations pertinentes relatives aux compétitions.

Idéalement, Nostradamus générerait une prédiction pour un état donné d'une compétition et conserverait cette prédiction jusqu'à ce qu'un événement pertinent survienne.

Ces événements peuvent notamment inclure :

- les forfaits de joueuses
- les changements de classement
- les wildcards
- les changements affectant la structure de la compétition

Lorsque des informations pertinentes changent, Nostradamus pourrait générer une nouvelle prédiction à partir de l'état actualisé des informations.

Une version future pourrait également notifier les utilisateurs lorsqu'un événement important entraîne le recalcul d'une prédiction.

---

## 🚧 État du projet

Nostradamus est actuellement en **phase de conception et de développement initial**.

La première implémentation se concentre sur la partie football et, plus précisément, sur la Ligue des Champions de l'UEFA.

Les priorités actuelles sont :

- définir les données nécessaires
- identifier des sources de données fiables
- documenter les règles officielles des compétitions
- traduire les règles des compétitions en contraintes informatiques
- concevoir le mécanisme de prédiction déterministe
- développer le premier prototype football

Aucun moteur de prédiction final n'a encore été implémenté.

---

## 🗺️ Feuille de route

### Phase 0 — Définition du projet
- [x] Définir le concept du projet
- [x] Définir le périmètre du projet
- [x] Définir les principes fondamentaux
- [x] Définir la philosophie de prédiction déterministe
- [x] Définir le principe de cohérence des tirages

### Phase 1 — Données et règles du football
- [x] Définir les données nécessaires
- [x] Identifier les sources de données
- [x] Collecter les données historiques des compétitions
- [x] Documenter les règles de la compétition UEFA
- [ ] Traduire les règles en contraintes informatiques

### Phase 2 — Moteur de prédiction football
- [ ] Concevoir le mécanisme de prédiction
- [ ] Implémenter le mécanisme de tirage déterministe
- [ ] Implémenter la cohérence des tirages
- [ ] Gérer les contraintes domicile/extérieur
- [ ] Valider les prédictions à partir de tirages historiques

### Phase 3 — Prédiction de la Ligue des Champions
- [ ] Générer une prédiction avant le tirage officiel
- [ ] Comparer la prédiction de Nostradamus avec le tirage officiel
- [ ] Analyser la précision et les limites de la prédiction

### Phase 4 — Phases à élimination directe
- [ ] Modéliser les tirages des phases à élimination directe
- [ ] Prédire les parcours potentiels
- [ ] Intégrer le classement final de la phase de ligue
- [ ] Étendre la prédiction jusqu'à la finale

### Phase 5 — Tennis féminin
- [ ] Définir les besoins en données pour le tennis
- [ ] Identifier les sources de données WTA
- [ ] Modéliser les contraintes spécifiques aux tirages des tournois
- [ ] Développer le premier moteur de prédiction tennis
- [ ] Tester l'approche sur des tournois historiques

### Futur
- [ ] Développer une interface utilisateur
- [ ] Implémenter les mises à jour des prédictions en fonction des événements
- [ ] Ajouter des notifications de prédiction
- [ ] Explorer d'autres sports et compétitions

---

## 🛠️ Technologies

La stack technique de Nostradamus n'est volontairement pas figée au début du projet.

Les choix technologiques seront effectués en fonction des besoins identifiés au cours du développement.

Les technologies potentielles peuvent notamment inclure :

- Python
- Bibliothèques de traitement et d'analyse de données
- Méthodes mathématiques et probabilistes
- Machine learning, lorsque pertinent
- Docker pour un déploiement reproductible
- Une interface web pour les versions futures

---

## 👩🏾‍💻 Auteur

**Lorame Bakaboula**

Nostradamus est un projet personnel conçu, développé et documenté par Lorame Bakaboula.

Le projet vise à documenter non seulement le résultat final, mais également le **processus de recherche, d'expérimentation, de collecte de données et de développement** qui se trouve derrière le moteur de prédiction.

---

## 📄 Licence

Voir le fichier [`LICENSE`](LICENSE) pour les informations relatives à la licence du projet.