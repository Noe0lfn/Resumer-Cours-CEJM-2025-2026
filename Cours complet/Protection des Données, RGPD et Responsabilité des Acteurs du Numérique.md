# Protection des Données, RGPD et Responsabilité des Acteurs du Numérique

Resumer des cours : 
- Critères de l'ACNIL et du CEPD
- La CNIL et le RGPD
- Responsabilité des hébergeurs et obligations du RGPD
- RGPD et CNIL
- video_RGPD


Ce cours traite du cadre juridique entourant la donnée personnelle, des pouvoirs de régulation de la CNIL et de la responsabilité spécifique des hébergeurs.

---

## I. Le Cadre Régulateur : CNIL et CEPD

Le respect des données en France et en Europe est supervisé par des autorités administratives indépendantes.

* **CNIL (France) :** Créée en 1978, elle veille à la protection des données, conseille les entreprises, contrôle les systèmes et sanctionne les abus.
* **CEPD (Europe) :** Regroupe toutes les "CNIL" européennes (remplace le G29) pour assurer une application uniforme du RGPD dans toute l'Union.

### A. Les Pouvoirs de la CNIL

La CNIL dispose de prérogatives plus larges que la police judiciaire :

* **Contrôles :** En ligne, sur pièces (registres), sur audition ou sur place (accès aux locaux).
* **Sanctions :** Graduées (avertissement > mise en demeure > amende).
* **Amendes records :** Jusqu'à **20 millions d’euros** ou **4% du Chiffre d'Affaires mondial**.

### B. Le Renversement de la Charge de la Preuve

C'est un principe clé du RGPD (**Accountability**) : En cas de plainte, ce n'est pas à la victime de prouver la faute, mais à l'organisme (entreprise/association) de **prouver qu'il respecte bien le règlement**.

---

## II. Le RGPD : Obligations et Mise en Conformité

Le **RGPD** (2018) repose sur le principe du **Privacy by Design** : la protection des données doit être pensée dès la conception d'un projet informatique.

### A. Les Obligations Techniques et Organisationnelles

1. **Le Registre des Traitements :** Document obligatoire répertoriant le "qui, quoi, pourquoi, comment" des données traitées.
2. **La Minimisation :** On ne collecte que le strict nécessaire (ex: pas besoin de la date de naissance pour une simple newsletter).
3. **La Sécurité :** Obligation de moyens proportionnée à la sensibilité des données (chiffrement, mots de passe forts).
4. **La Publicité des failles :** En cas de piratage, l'entreprise doit avertir la CNIL sous **72h** et informer les victimes si le risque est élevé.

### B. L'Analyse d'Impact relative à la Protection des Données (AIPD)

Obligatoire si le traitement réunit **2 des 9 critères** de l'ACNIL/CEPD (ex: surveillance à grande échelle + données sensibles).

* **Critères fréquents :** Scoring (évaluation), profilage, données de santé, surveillance automatique, usage de nouvelles technologies.

### C. Le Cycle de Vie de la Donnée

Les données ne se gardent pas indéfiniment. On distingue 3 phases :

1. **Utilisation courante :** Accès direct pour la finalité prévue.
2. **Archivage intermédiaire :** Accès restreint (obligations légales/contentieux).
3. **Archivage définitif :** Uniquement pour l'intérêt public (historique/scientifique).

---

## III. Les Droits des Personnes Physiques

Toute personne dont les données sont traitées dispose de droits opposables à l'entreprise :

* **Accès et Rectification :** Voir et corriger ses infos.
* **Droit à l'oubli (Effacement) :** Supprimer ses données.
* **Portabilité :** Récupérer ses données dans un format structuré pour les transférer ailleurs.
* **Opposition au profilage :** Refuser les décisions 100% automatisées.

---

## IV. Focus SIO : Responsabilité et Transferts

### A. La Responsabilité de l'Hébergeur (Jurisprudence Atcom)

L'arrêt *Atcom / Ville de Marseille* définit une règle cruciale pour les prestataires informatiques :

> **Principe :** Un hébergeur n'est responsable des contenus illicites que **tant qu'il les héberge effectivement**.

* S'il reçoit une mise en demeure mais que le site change d'hébergeur avant l'action en justice, l'ancien hébergeur ne peut plus être condamné à retirer le contenu (car il n'en a plus le contrôle technique). Seul l'hébergeur actuel est poursuivi.

### B. Transferts Hors Union Européenne

Le RGPD protège les citoyens européens même hors frontières.

* **Pays Adéquats :** Protection jugée suffisante par l'UE (ex: USA sous conditions spécifiques).
* **Pays Non-Adéquats :** Nécessite des clauses contractuelles types ou des règles contraignantes pour garantir la sécurité.

---

## 💡 Glossaire Express pour l'Examen

| Terme | Ce qu'il faut retenir |
| --- | --- |
| **Donnée Personnelle** | Toute info permettant d'identifier une personne (IP, nom, n° client). |
| **DPO** | Délégué à la Protection des Données : le chef d'orchestre du RGPD. |
| **AIPD / PIA** | Étude de risques obligatoire pour les traitements "dangereux". |
| **Accountability** | Obligation pour l'entreprise de documenter et prouver sa conformité. |
| **Hébergeur** | Statut juridique avec responsabilité limitée (réagit après signalement). |