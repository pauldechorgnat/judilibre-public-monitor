from string import ascii_letters
from string import digits

from pandas.api.types import CategoricalDtype

LETTERS = [letter for letter in ascii_letters]
NUMBERS = [number for number in digits]

SOURCES = ["dila", "jurinet", "jurica", "juritj"]
SOURCES_DTYPE = CategoricalDtype(SOURCES)

JURISDICTIONS = {
    "cc": "Cour de cassation",
    "ca": "Cours d'appel",
    "tj": "Tribunaux judiciaires",
}


def remove_cour_dappel(string: str = "Cour d'appel de Paris"):
    string = string.replace("Cour d'appel de ", "")
    string = string.replace("Cour d'appel d'", "")
    string = string.replace("Tribunal judiciaire d'", "")
    string = string.replace("Tribunal judiciaire de ", "")

    return string


DECISION_TYPES = {
    "arret": "Arrêt",
    "other": "Autre",
    "ordonnance": "Ordonnance",
    "avis": "Avis",
    "qpc": "Question Prioritaire de Constitutionnalité",
    "saisie": "Saisie",
}

# TODO: Trouver les références
CHAMBERS_CC = {
    "cr": "cr",
    "civ1": "Iere chambre civile",
    "civ2": "IIeme chambre civile",
    "civ3": "IIIeme chambre civile",
    "pl": "Assemblée plénière",
    "comm": "Commerce",
    "mi": "mi",
    "ordo": "Ordonnance",
    "soc": "Sociale",
    "creun": "creun",
    "other": "other",
}

CHAMBERS_CA = {"inconnue": "Chambre inconnue"}

CHAMBERS_TJ = {}

CHAMBERS = {**CHAMBERS_CC, **CHAMBERS_CA, **CHAMBERS_TJ}
LOCATIONS_CC = {"cc": "Cour de cassation"}

LOCATIONS_CA = {
    "ca_toulouse": "Cour d'appel de Toulouse",
    "ca_poitiers": "Cour d'appel de Poitiers",
    "ca_caen": "Cour d'appel de Caen",
    "ca_basse_terre": "Cour d'appel de Basse-Terre",
    "ca_papeete": "Cour d'appel de Papeete",
    "ca_douai": "Cour d'appel de Douai",
    "ca_aix_provence": "Cour d'appel d'Aix-en-Provence",
    "ca_angers": "Cour d'appel d'Angers",
    "ca_versailles": "Cour d'appel de Versailles",
    "ca_besancon": "Cour d'appel de Besancon",
    "ca_limoges": "Cour d'appel de Limoges",
    "ca_chambery": "Cour d'appel de Chambery",
    "ca_pau": "Cour d'appel de Pau",
    "ca_paris": "Cour d'appel de Paris",
    "ca_lyon": "Cour d'appel de Lyon",
    "ca_rennes": "Cour d'appel de Rennes",
    "ca_colmar": "Cour d'appel de Colmar",
    "ca_montpellier": "Cour d'appel de Montpellier",
    "ca_bastia": "Cour d'appel de Bastia",
    "ca_bordeaux": "Cour d'appel de Bordeaux",
    "ca_rouen": "Cour d'appel de Rouen",
    "ca_nimes": "Cour d'appel de Nimes",
    "ca_amiens": "Cour d'appel d'Amiens",
    "ca_st_denis_reunion": "Cour d'appel de Saint-Denis de la Réunion",
    "ca_dijon": "Cour d'appel de Dijon",
    "ca_nancy": "Cour d'appel de Nancy",
    "ca_orleans": "Cour d'appel d'Orléans",
    "ca_grenoble": "Cour d'appel de Grenoble",
    "ca_riom": "Cour d'appel de Riom",
    "ca_fort_de_france": "Cour d'appel de Fort-de-France",
    "ca_noumea": "Cour d'appel de Noumea",
    "ca_metz": "Cour d'appel de Metz",
    "ca_bourges": "Cour d'appel de Bourges",
    "ca_reims": "Cour d'appel de Reims",
    "ca_agen": "Cour d'appel de Agen",
    "ca_cayenne": "Cour d'appel de Cayenne",
}

LOCATIONS_TJ = {
    "tj75056": "Tribunal judiciaire de Paris",
    "tj93008": "Tribunal judiciaire de Bobigny",
    "tj33063": "Tribunal judiciaire de Bordeaux",
    "tj13055": "Tribunal judiciaire de Marseille",
}

LOCATIONS = {
    **LOCATIONS_CA,
    **LOCATIONS_TJ,
}


FORMATIONS_CC = {
    "pl": "Assemblée plénière",
    "mi": "Chambre mixte",
    "civ1": "Première chambre civile",
    "civ2": "Deuxième chambre civile",
    "civ3": "Troisième chambre civile",
    "comm": "Chambre commerciale financière et économique",
    "soc": "Chambre sociale",
    "cr": "Chambre criminelle",
    "creun": "Chambres réunies",
    "ordo": "Première présidence (Ordonnance)",
    "allciv": "Toutes les chambres civiles",
    "other": "Autre",
}


CHAMBERS_CC = {
    "pl": "Plénière",
    "mi": "Mixte",
    "civ1": "Civile I",
    "civ2": "Civile II",
    "civ3": "Civile III",
    "comm": "Commerciale",
    "soc": "Sociale",
    "cr": "Criminelle",
    "creun": "Réunies",
    "ordo": "Ordonnance (PP)",
    "allciv": "Civiles",
    "other": "Autre",
}

TYPES = {
    "arret": "Arrêt",
    "avis": "Avis",
    "ordonnance": "Ordonnance",
    "other": "Autre",
    "qpc": "QPC",
    "saisie": "Saisie",
}


SOURCES = {
    "dila": "DILA",
    "jurinet": "Jurinet",
    "jurica": "Jurica",
    "juritj": "JuriTJ",
}


CLEAN_COLUMN_NAMES = {
    "chamber": "Chambre ou formation",
    "decision_date": "Date",
    "source": "Source",
    "jurisdiction": "Juridiction",
    "court": "Cour",
    "location": "Localisation",
    "type": "Type de décision",
    "Niveau 1": "Niveau 1 d'Affaire Civile",
    "Niveau 2": "Niveau 2 d'Affaire Civile",
}

FORMATIONS_CC = {
    "f": "Formation restreinte",
    "fm": "Formation mixte",
    "fp": "Formation plénière de chambre",
    "frh": "Formation restreinte hors RNSM/NA",
    "frr": "Formation restreinte RNSM/NA",
    "fs": "Formation de section",
}
