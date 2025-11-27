# 🔍 Analyse d'une campagne fictive de phishing  
Projet Python – Sécurité / Datatelling

## 📌 Objectif du projet
Ce projet consiste à analyser un jeu de données fictif issu d'une campagne de phishing pédagogique.  
L’objectif est de :
- Nettoyer et préparer les données  
- Détecter les incohérences et valeurs aberrantes  
- Identifier les profils les plus vulnérables  
- Produire des visualisations  
- Construire un scénario de phishing fictif basé sur les résultats  


---

## 🧹 1. Nettoyage et préparation des données

Les opérations effectuées :
- Normalisation des textes (lowercase, strip)
- Harmonisation de catégories (`mail`, `instagram`, `facebook`)
- Correction de fautes (`fornite` → `fortnite`)
- Transformation du champ `campaign_success` en booléen
- Détection et suppression des valeurs aberrantes :
  - Âges < 16 ou > 60
  - Scores d’intérêt < 0 ou > 100

Dataset initial : **519 lignes**  
Dataset final (propre) : **499 lignes**

---

## 📊 2. Analyses statistiques

### **Taux global de réussite**
> **69.74%**

### **Par canal**
- **Facebook : 85.16%**
- Mail : 66.34%
- Instagram : 63.06%

➡️ Facebook = canal le plus vulnérable

### **Par produit**
- **FIFA : 72.25%**
- Fortnite : 70.22%
- Instagram Pack : 66.22%

➡️ Le thème “football” fonctionne très bien

### **Par tranche d’âge**
- **50–60 ans : 78.57%**
- 40–49 ans : 71.43%
- 30–39 ans : 70.63%

➡️ Les seniors sont les plus vulnérables

### **Centres d’intérêt**
- Foot élevé : **76%**
- Gaming élevé : **74%**
- Insta élevé : **79%**

➡️ Les intérêts augmentent la probabilité de clic

---

## 📈 3. Visualisations
Le script génère :
- Heatmap de corrélations  
- Barplots :
  - par canal  
  - par produit  
  - par tranche d’âge  
  - par niveaux d’intérêt (foot, gaming, insta)

---

## 🎯 4. Profil le plus vulnérable
Après croisement de toutes les analyses :

> **Utilisateur de 50–60 ans, fan de football, très actif sur Facebook.**

Ce profil est cohérent :
- Statistiquement (taux les plus élevés)
- Socialement (football + Facebook = très populaire chez cette tranche d'âge)

---

## 🎣 5. Scénario d’attaque fictive

> **“🎉 Billets VIP Ligue des Champions à -80% !  
> Offre exclusive réservée aux abonnés Facebook.  
> Cliquez ici pour vérifier votre identité.”**

Raisons :
- Exploite le thème du football (le plus engageant)
- Utilise Facebook (canal le plus vulnérable)
- Cible la tranche 50–60 ans (la plus susceptible de cliquer)

---

## 🚀 6. Comment exécuter le script

Assurez-vous d’avoir Python 3 + pandas + matplotlib :

```bash
pip install pandas matplotlib numpy
```

Puis lancez :
```bash
python src/analyse_phishing.py
```

Cela affiche :

- Les statistiques
- Les KPIs
- Les sections d’analyse
- Toutes les visualisations




