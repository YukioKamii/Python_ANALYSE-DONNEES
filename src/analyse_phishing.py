import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)



# Affichage un peu plus lisible
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

# 1) Charger les données
df = pd.read_csv("data/result.csv", sep=";")

print("Aperçu des données :")
print(df.head(), "\n")

print("Infos :")
print(df.info(), "\n")

print("Stats numériques :")
print(df.describe())


# 2) Analyse des valeurs uniques et des plages de valeurs
print("\nValeurs uniques de 'canal_recommande' :")
print(df["canal_recommande"].value_counts(dropna=False))

print("\nValeurs uniques de 'recommended_product' :")
print(df["recommended_product"].value_counts(dropna=False))

print("\nValeurs uniques de 'campaign_success' :")
print(df["campaign_success"].value_counts(dropna=False))

print("\nÂges min / max :", df["age"].min(), df["age"].max())
print("Scores gaming min / max :", df["gaming_interest_score"].min(), df["gaming_interest_score"].max())
print("Scores insta min / max :", df["insta_design_interest_score"].min(), df["insta_design_interest_score"].max())
print("Scores foot min / max :", df["football_interest_score"].min(), df["football_interest_score"].max())


# 3) Nettoyage de base

print_section("ETAPE 3 - NETTOYAGE DE BASE")


# On travaille sur une copie pour ne pas casser le df original
df_clean = df.copy()

# -----------------------------
# 3.1 Normalisation des textes
# -----------------------------
# On met en str, on enlève les espaces autour, on passe en minuscules
for col in ["campaign_success", "recommended_product", "canal_recommande"]:
    df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()

print("\nAprès normalisation texte :")
print("\ncanal_recommande :")
print(df_clean["canal_recommande"].value_counts(dropna=False))
print("\nrecommended_product :")
print(df_clean["recommended_product"].value_counts(dropna=False))
print("\ncampaign_success :")
print(df_clean["campaign_success"].value_counts(dropna=False))

# ------------------------------------
# 3.2 Harmonisation des catégories
# ------------------------------------

# canal_recommande : regrouper les variantes
df_clean["canal_recommande"] = df_clean["canal_recommande"].replace({
    "mail": "mail",        # mail, Mail, MAIL -> "mail" grâce au lower()
    "insta": "instagram",  # insta / Insta -> "instagram"
    "facebook": "facebook",
    "non_defini": "non_defini",
    "nan": np.nan,         # le texte "nan" redevient une vraie valeur manquante
})

# recommended_product : corriger fautes + virer les valeurs bidon
df_clean["recommended_product"] = df_clean["recommended_product"].replace({
    "fortnite": "fortnite",
    "fornite": "fortnite",     # faute corrigée
    "fifa": "fifa",
    "instagram pack": "instagram pack",
    "test": np.nan,            # "test" = on considère que c'est pas un vrai produit
    "nan": np.nan,
})

print("\nAprès harmonisation des catégories :")
print("\ncanal_recommande :")
print(df_clean["canal_recommande"].value_counts(dropna=False))
print("\nrecommended_product :")
print(df_clean["recommended_product"].value_counts(dropna=False))

# ------------------------------------
# 3.3 Transformation de campaign_success en booléen
# ------------------------------------
df_clean["campaign_success"] = df_clean["campaign_success"].map({
    "true": True,
    "false": False
})

print("\nVérification de campaign_success après mapping :")
print(df_clean["campaign_success"].value_counts(dropna=False))
print("Type de campaign_success :", df_clean["campaign_success"].dtype)


# 4) Détection + suppression des valeurs suspectes/aberrantes

print_section("ETAPE 4 - DETECTION ET SUPPRESSION DES VALEURS SUSPECTES")


# -----------------------------
# 4.1 Identification des anomalies
# -----------------------------

print("\nÂges uniques triés :")
print(sorted(df_clean["age"].dropna().unique()))

# règles logiques :
# - âge < 16 : trop jeune pour être cible réaliste
# - âge > 60 : trop vieux selon le dataset
age_anormal = (df_clean["age"] < 16) | (df_clean["age"] > 60)

# scores d'intérêt normalement entre 0 et 100
gaming_anormal = (df_clean["gaming_interest_score"] < 0) | (df_clean["gaming_interest_score"] > 100)
insta_anormal  = (df_clean["insta_design_interest_score"] < 0) | (df_clean["insta_design_interest_score"] > 100)
foot_anormal   = (df_clean["football_interest_score"] < 0) | (df_clean["football_interest_score"] > 100)

# une ligne est anormale si l'un des critères est vrai
anomalies = age_anormal | gaming_anormal | insta_anormal | foot_anormal

print("\nNombre total de lignes anormales :", anomalies.sum())

# -----------------------------
# 4.2 Suppression des anomalies
# -----------------------------
df_model = df_clean[~anomalies].copy()

# Suppression des lignes sans info critique (produit ou âge manquant par ex.)
df_model = df_model.dropna(subset=["age", "recommended_product"])

print("\nTaille avant nettoyage :", df_clean.shape)
print("Taille après nettoyage :", df_model.shape)

print("\nStats après nettoyage :")
print(df_model.describe(include="all"))


# 5) KPI: Taux de réussite global de la campagne

print_section("ETAPE 5 - KPIs IMPORTANTS")

# 5.1 Taux global
success_rate_global = df_model["campaign_success"].mean()
print(f"\nTaux de réussite global : {success_rate_global*100:.2f}%")

# 5.2 Par canal
success_by_canal = df_model.groupby("canal_recommande")["campaign_success"].mean().sort_values(ascending=False)
print("\nTaux de réussite par canal (%):")
print((success_by_canal * 100).round(2).astype(str) + " %")

# 5.3 Par produit
success_by_product = df_model.groupby("recommended_product")["campaign_success"].mean().sort_values(ascending=False)
print("\nTaux de réussite par produit (%):")
print((success_by_product * 100).round(2).astype(str) + " %")

# 5.4 Par tranche d'âge
bins = [16, 20, 25, 30, 40, 50, 60]
labels = ["16-19", "20-24", "25-29", "30-39", "40-49", "50-60"]
df_model["age_group"] = pd.cut(df_model["age"], bins=bins, labels=labels, right=True)

success_by_age_group = df_model.groupby("age_group")["campaign_success"].mean().sort_values(ascending=False)
print("\nTaux de réussite par tranche d'âge (%):")
print((success_by_age_group * 100).round(2).astype(str) + " %")



# 6) Analyse des corrélations et scoring des intérêts

print_section("ETAPE X - ANALYSE DES CORRELATIONS")


# -----------------------------
# 6.1 Matrice de corrélation
# -----------------------------
corr = df_model[[
    "gaming_interest_score",
    "insta_design_interest_score",
    "football_interest_score",
    "age",
    "campaign_success"
]].corr(numeric_only=True)

print("\nMatrice de corrélation :\n")
print(corr)

# -----------------------------
# 6.2 Analyse par tranches de scores
# -----------------------------
def score_group(series):
    return pd.cut(series, bins=[0, 33, 66, 100], labels=["faible", "moyen", "élevé"])

df_model["gaming_group"] = score_group(df_model["gaming_interest_score"])
df_model["insta_group"] = score_group(df_model["insta_design_interest_score"])
df_model["foot_group"] = score_group(df_model["football_interest_score"])

print("\nTaux de réussite par niveau d'intérêt FOOT (%):")
print((df_model.groupby("foot_group")["campaign_success"].mean() * 100).round(2).astype(str) + " %")


print("\nTaux de réussite par niveau d'intérêt GAMING (%):")
print((df_model.groupby("gaming_group")["campaign_success"].mean() * 100).round(2).astype(str) + " %")

print("\nTaux de réussite par niveau d'intérêt INSTAGRAM (%):")
print((df_model.groupby("insta_group")["campaign_success"].mean() * 100).round(2).astype(str) + " %")


# 7) Visualisations (heatmap + barplots)

print_section("ETAPE 7 - VISUALISATIONS")

# 7.1 Heatmap de corrélation
corr = df_model[[
    "gaming_interest_score",
    "insta_design_interest_score",
    "football_interest_score",
    "age",
    "campaign_success"
]].corr(numeric_only=True)

plt.figure(figsize=(6, 5))
plt.imshow(corr, interpolation="nearest")
plt.title("Matrice de corrélation")
plt.colorbar()
tick_marks = range(len(corr.columns))
plt.xticks(tick_marks, corr.columns, rotation=45, ha="right")
plt.yticks(tick_marks, corr.columns)
plt.tight_layout()
plt.show()

# 7.2 Barplot - Taux de réussite par canal
plt.figure(figsize=(6, 4))
(success_by_canal * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par canal")
plt.tight_layout()
plt.show()

# 7.3 Barplot - Taux de réussite par produit
plt.figure(figsize=(6, 4))
(success_by_product * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par produit")
plt.tight_layout()
plt.show()

# 7.4 Barplot - Taux de réussite par tranche d'âge
plt.figure(figsize=(6, 4))
(success_by_age_group * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par tranche d'âge")
plt.tight_layout()
plt.show()

# 7.5 Barplot - Taux de réussite par niveau d'intérêt FOOT
success_by_foot_group = df_model.groupby("foot_group")["campaign_success"].mean()
plt.figure(figsize=(6, 4))
(success_by_foot_group * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par niveau d'intérêt FOOT")
plt.tight_layout()
plt.show()

# 7.6 (optionnel) Taux par niveau GAMING
success_by_gaming_group = df_model.groupby("gaming_group")["campaign_success"].mean()
plt.figure(figsize=(6, 4))
(success_by_gaming_group * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par niveau d'intérêt GAMING")
plt.tight_layout()
plt.show()

# 7.7 (optionnel) Taux par niveau INSTAGRAM
success_by_insta_group = df_model.groupby("insta_group")["campaign_success"].mean()
plt.figure(figsize=(6, 4))
(success_by_insta_group * 100).plot(kind="bar")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite par niveau d'intérêt INSTAGRAM")
plt.tight_layout()
plt.show()