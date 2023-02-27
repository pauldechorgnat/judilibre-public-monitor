from string import ascii_letters
from string import digits

from pandas.api.types import CategoricalDtype

LETTERS = [l for l in ascii_letters]
NUMBERS = [n for n in digits]

SOURCES = ["dila", "jurinet", "jurica"]
SOURCES_DTYPE = CategoricalDtype(SOURCES)

JURISDICTIONS = {
    "cc": "Cour de cassation",
    "ca": "Cour d'appel",
    "tj": "Tribunal judiciaire",
}


def remove_cour_dappel(string: str = "Cour d'appel de Paris"):
    string = string.replace("Cour d'appel de ", "")
    string = string.replace("Cour d'appel d'", "")
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

LOCATIONS = {**LOCATIONS_CA}
