"""
Data cleaning pipeline.

This is a direct port of cells 3-7 of `Car_Project_Optimized_10_Visualizations.ipynb`
(dropping bad rows, fixing/imputing Body & Transmission from the model name,
median/mode imputation grouped by Make/Model, date parsing, and the
SaleYear / SaleMonth / car_age feature engineering). Kept intentionally close
to the original so the "Data Description" page in the dashboard describes
exactly what this code does.
"""

import re
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Body / Transmission lookup tables (same substring-match maps used in the
# original notebook to recover missing Body / Transmission from the Model
# text).
# --------------------------------------------------------------------------
BODY_MAP = {
    'cx-7': 'SUV', 'lr3': 'SUV', 'range': 'SUV', 'corvette': 'Coupe', 'impala': 'Sedan',
    'malibu': 'Sedan', 'g6': 'Sedan', 'sts': 'Sedan', 'accord': 'Sedan', 'civic': 'Sedan',
    'tundra': 'Truck', 'silverado': 'Truck', 'f-150': 'Truck', 'f150': 'Truck',
    'matrix': 'Wagon', 'hhr': 'Wagon', 'mazda5': 'Minivan', 'sienna': 'Minivan',
    'odyssey': 'Minivan', 'lancer': 'Sedan', 'c230': 'Sedan', 'c230wz': 'Sedan', '7': 'Sedan',
    'gx': 'SUV', 'rx': 'SUV', 'pilot': 'SUV', 'explorer': 'SUV', 'borrego': 'SUV',
    'c240': 'Sedan', 'rx8': 'Coupe', 'sr': 'Truck', '350z': 'Coupe', '911': 'Coupe',
    'lx': 'SUV', 'pacifica': 'Minivan', 's55': 'Sedan', 'silhouette': 'Minivan',
    'astro': 'Van', 'expedit': 'SUV', 'police': 'SUV', 'g55': 'SUV', 'discovery': 'SUV',
    'stratus': 'Sedan', 'escape': 'SUV', '1500': 'Truck', 'crossfire': 'Coupe',
    'tribute': 'SUV', 'durango': 'SUV', 'uplander': 'Minivan', 'ridgeline': 'Truck',
    'focus': 'Sedan', 'forester': 'SUV', 'sprinter': 'Van', 'alero': 'Sedan',
    'mountnr': 'SUV', 'wrangler': 'SUV', 'santa': 'SUV', 'camry': 'Sedan', 'gr': 'SUV',
    'camaro': 'Coupe', 'ram': 'Truck', 'caravan': 'Minivan', 'windstar': 'Minivan',
    'taurus': 'Sedan', 's10': 'Truck', 'f250': 'Truck', 'voyager': 'Minivan',
    'venture': 'Minivan', 'regal': 'Sedan', 'journey': 'SUV', 'mpv': 'Minivan',
    '300e': 'Sedan', 'pickup': 'Truck', 'ciera': 'Sedan', 'previa': 'Minivan',
    'b2300': 'Truck', 'patriot': 'SUV', 'rl': 'Sedan', 'passat': 'Sedan', 'g500': 'SUV',
    '420sel': 'Sedan', '42c': 'Coupe', 'subrbn': 'SUV', 'e250': 'Van', 'corolla': 'Sedan',
    'jetta': 'Sedan', 'a4': 'Sedan', 'rio': 'Sedan', 'elantra': 'Sedan', 'sebring': 'Sedan',
    '200': 'Sedan', 'endeavor': 'SUV', 'capt': 'SUV', 'g3500': 'Truck', 'colorado': 'Truck',
    'crown': 'Sedan', 'dts': 'Sedan', 'alp': 'Sedan', 'optima': 'Sedan', 'mazda6': 'Sedan',
    'montana': 'Minivan', 'vibe': 'Wagon', 'sx4': 'Hatchback', '3500': 'Truck',
    'quattroporte': 'Sedan', 'town': 'Sedan', 'mazda3': 'Sedan', 'g5': 'Sedan',
    'yaris': 'Sedan', 'optra': 'Sedan', 'magnum': 'Wagon', 'savana': 'Van',
    'ridgelin': 'Truck', 'rrs': 'SUV', 'carrera': 'Coupe', 'wave': 'Sedan', 'tt': 'Coupe',
    'pt': 'Hatchback', 'freestyle': 'SUV', 'pursuit': 'Sedan', 'x-trail': 'SUV',
    'el': 'Sedan', 'rainier': 'SUV', 'intrepid': 'Sedan', '320i': 'Sedan', 'cl55': 'Sedan',
    'sl55': 'Coupe', 'concorde': 'Sedan', '2500': 'Truck', 'cavalier': 'Sedan',
    'excurs': 'SUV', 'dakota': 'Truck', 'twn&country': 'Minivan', 'safari': 'Van',
    'sonoma': 'Truck', 'yukon': 'SUV', 'breeze': 'Sedan', 'villager': 'Minivan',
    'beetle': 'Hatchback', 'suburban': 'SUV', 'mountaineer': 'SUV', 'pathfinder': 'SUV',
    'quest': 'Minivan', 'e300dt': 'Sedan', 'intrigue': 'Sedan', 'lumina': 'Sedan',
    'thunderbird': 'Coupe', 'legacy': 'Sedan', 'corsica': 'Sedan', 'bronco': 'SUV',
    'century': 'Sedan', 'versa': 'Sedan', 'routan': 'Minivan', 'interstate': 'Van',
    'a6': 'Sedan', 'swift': 'Hatchback', 'escalade': 'SUV', 'neon': 'Sedan',
    'f350': 'Truck', 'cougar': 'Coupe', 'lacrosse': 'Sedan', 'tucson': 'SUV',
    '323i': 'Sedan', 'cobalt': 'Sedan', 'x3': 'SUV', 'sonic': 'Hatchback', 'rr': 'SUV',
    '1': 'Hatchback', '300': 'Sedan', '350': 'Truck', 'twn/cntry': 'Minivan', 'e': 'Van',
    'cruze': 'Sedan', 'compass': 'SUV', 'avalon': 'Sedan', 'pathfind': 'SUV',
    'golf': 'Hatchback', 'comm': 'Van', '328i': 'Sedan', 'upland': 'Minivan',
}

TRANSMISSION_MAP = {
    'verano': 'Automatic', 'cruze': 'Automatic', 'silverado 2500hd': 'Automatic',
    'sonata hybrid': 'Automatic', 'charger': 'Automatic', 'elantra': 'Automatic',
    'sentra': 'Automatic', 'k900': 'Automatic', 's-class': 'Automatic', 'optima': 'Automatic',
    'm-class': 'Automatic', 'versa': 'Automatic', 'rogue': 'Automatic', 'quest': 'Automatic',
    'frontier': 'Automatic', 'altima': 'Automatic', 'jetta': 'Automatic', 'murano': 'Automatic',
    '6 series': 'Automatic', 'rdx': 'Automatic', '3 series': 'Automatic',
    'e-series wagon': 'Automatic', 'flex': 'Automatic', 'escape': 'Automatic',
    'f-150': 'Automatic', 'x5': 'Automatic', 'silverado 1500': 'Automatic',
    'malibu': 'Automatic', 'e-series van': 'Automatic', '200': 'Automatic',
    'grand caravan': 'Automatic', 'mustang': 'Manual', 'fusion': 'Automatic',
    'odyssey': 'Automatic', 'cooper clubman': 'Automatic', 'navigator': 'Automatic',
    'sedona': 'Automatic', '1500': 'Automatic', 'q7': 'Automatic', 'passat': 'Automatic',
    'cr-v': 'Automatic', '300': 'Automatic', 'ranger': 'Automatic', 'xj': 'Automatic',
    'wrangler': 'Manual', 'cx-7': 'Automatic', 'range rover': 'Automatic',
    'cooper': 'Automatic', 'camry': 'Automatic', 'rio': 'Automatic', 'taurus': 'Automatic',
    'mazda3': 'Automatic', 'forester': 'Automatic', 'soul': 'Automatic', 'edge': 'Automatic',
    'corolla': 'Automatic', 'journey': 'Automatic', 'taurus x': 'Automatic',
    'acadia': 'Automatic', 'tahoe': 'Automatic', 'explorer': 'Automatic',
    'focus': 'Automatic', 'cobalt': 'Automatic', 'e350': 'Automatic', 'e-class': 'Automatic',
    'mkx': 'Automatic', 'g8': 'Automatic', 'expedition': 'Automatic',
    'grand cherokee': 'Automatic', 'g35': 'Automatic', 'liberty': 'Automatic',
    'magnum': 'Automatic', 'monte carlo': 'Automatic', 'tucson': 'Automatic',
    'escalade': 'Automatic', 'range': 'Automatic', 'highlander': 'Automatic',
    'aura': 'Automatic', 'prius': 'Automatic', 'a6': 'Automatic', 'b9 tribeca': 'Automatic',
    'mariner': 'Automatic', 'azera': 'Automatic', 'commander': 'Automatic',
    'sierra 2500hd': 'Automatic', 'f-250 super duty': 'Automatic', 'gs 430': 'Automatic',
    'mark lt': 'Automatic', 'clk-class': 'Automatic', 'pathfinder': 'Automatic',
    'xterra': 'Automatic', 'titan': 'Automatic', 'xb': 'Automatic', 'avalon': 'Automatic',
    'ram pickup 3500': 'Automatic', 'durango': 'Automatic', 'five hundred': 'Automatic',
    'equinox': 'Automatic', 'yukon xl': 'Automatic', 'suburban': 'Automatic',
    'yukon': 'Automatic', 'econoline cargo': 'Automatic', 'element': 'Automatic',
    'montana': 'Automatic', 'grand marquis': 'Automatic', 'mpv': 'Automatic',
    'grand prix': 'Automatic', 'express cargo': 'Automatic', 'qx4': 'Automatic',
    'z4': 'Manual', 'mazdaspeed protege': 'Manual', 'cts': 'Automatic', 'xc90': 'Automatic',
    '7 series': 'Automatic', 'f-350 super duty': 'Automatic', 'cougar': 'Automatic',
    'windstar': 'Automatic', 'deville': 'Automatic', 'celica': 'Manual',
    's-series': 'Automatic', 'tundra': 'Automatic', '5 series': 'Automatic',
    'impala': 'Automatic', 'land cruiser': 'Automatic', 'accord': 'Automatic',
    'cavalier': 'Automatic', 'g20': 'Automatic', 'caravan': 'Automatic', 'f150': 'Automatic',
    'civic': 'Automatic', 'sienna': 'Automatic', 'c-class': 'Automatic', 'prizm': 'Automatic',
    'ls 400': 'Automatic', 'mazda2': 'Manual', '3500': 'Automatic', 'tacoma': 'Manual',
    'fiesta': 'Manual', 'challenger': 'Automatic', 'nitro': 'Automatic',
    'town car': 'Automatic', 'town and country': 'Automatic', 'a4': 'Automatic',
    'g6': 'Automatic', 'maxima': 'Automatic', 'impreza': 'Manual', 'forenza': 'Manual',
    'sequoia': 'Automatic', 'pt cruiser': 'Automatic', 'mountaineer': 'Automatic',
    'ls 430': 'Automatic', 'diamante': 'Automatic', 'aviator': 'Automatic',
    'rodeo': 'Automatic', 'qx70': 'Automatic', 'avenger': 'Automatic', 'a3': 'Automatic',
    'legacy': 'Automatic', 'outback': 'Automatic', '2500': 'Automatic', 'tc': 'Manual',
    'beetle': 'Manual', 'venza': 'Automatic', 'rav4': 'Automatic', 's60': 'Automatic',
    'c70': 'Automatic', 'tiguan': 'Automatic', 'golf': 'Manual', 'mdx': 'Automatic',
    'q5': 'Automatic', 'tsx': 'Automatic', '1 series': 'Manual', 'tl': 'Automatic',
    'a5': 'Automatic', 'a8': 'Automatic', 'x3': 'Automatic', 'enclave': 'Automatic',
    'm3': 'Manual', 'lacrosse': 'Automatic', 'srx': 'Automatic', 'avalanche': 'Automatic',
    'camaro': 'Manual', 'traverse': 'Automatic', 'terrain': 'Automatic', 'fit': 'Manual',
    'pilot': 'Automatic', 'sonata': 'Automatic', 'g sedan': 'Automatic',
    'equus': 'Automatic', 'fx': 'Automatic', 'genesis': 'Automatic', 'veracruz': 'Automatic',
    'santa fe': 'Automatic', 'g coupe': 'Automatic', 'xk': 'Automatic', 'xf': 'Automatic',
    'sorento': 'Automatic', 'compass': 'Automatic', 'grand': 'Automatic', 'dart': 'Manual',
    'gx 460': 'Automatic', 'lr4': 'Automatic', 'sportage': 'Automatic', 'es 350': 'Automatic',
    'rx 350': 'Automatic', 'cx-9': 'Automatic', 'ls 460': 'Automatic', 'lx 570': 'Automatic',
    'is 350': 'Automatic', 'is 250': 'Automatic', 'is 250 c': 'Automatic', '3': 'Manual',
    'glk-class': 'Automatic', 'gl-class': 'Automatic', 'lancer': 'Manual',
    'slk-class': 'Manual', 'galant': 'Automatic', 'juke': 'Automatic', 'cube': 'Automatic',
    'cayenne': 'Automatic', '4runner': 'Automatic', 'xc60': 'Automatic', 'x6': 'Automatic',
    'e150': 'Automatic', 'transit connect': 'Automatic', 'police': 'Automatic',
    'accent': 'Automatic', 'forte': 'Automatic', '500l': 'Automatic', '500': 'Automatic',
    'mkt': 'Automatic', 'armada': 'Automatic', 'endeavor': 'Automatic', 'gr': 'Automatic',
    'xd': 'Automatic', 's5': 'Automatic', 'aveo': 'Automatic', 'caliber': 'Automatic',
    'crown': 'Automatic', 'econoline wagon': 'Automatic', 'savana cargo': 'Automatic',
    'mks': 'Automatic', 'rondo': 'Automatic', 'mkz': 'Automatic', 'vibe': 'Automatic',
    'fortwo': 'Automatic', 'cc': 'Automatic', 's6': 'Automatic', 'lucerne': 'Automatic',
    'hhr': 'Automatic', 'uplander': 'Automatic', 'sebring': 'Automatic',
    'sprinter cargo': 'Automatic', 'santa': 'Automatic', 'ridgeline': 'Automatic',
    'tribute': 'Automatic', 'eclipse spyder': 'Automatic', 'sable': 'Automatic',
    'torrent': 'Automatic', 'xl7': 'Automatic', 'fj cruiser': 'Automatic',
    'yaris': 'Automatic', 'matrix': 'Automatic', 'touareg 2': 'Automatic', 'gti': 'Automatic',
    'gli': 'Automatic', 'eos': 'Automatic', 'm6': 'Automatic', 'dts': 'Automatic',
    'corvette': 'Automatic', 'pacifica': 'Automatic', 'freestyle': 'Automatic',
    'envoy': 'Automatic', 'm45': 'Automatic', 'rx8': 'Manual', 'r-class': 'Automatic',
    'milan': 'Automatic', 'eclipse': 'Automatic', 'g5': 'Automatic', 'vue': 'Automatic',
    'ion': 'Automatic', 'sky': 'Manual', 'rabbit': 'Automatic', 'rendezvous': 'Automatic',
    'terraza': 'Automatic', 'sts': 'Automatic', 'optra': 'Automatic', 'sprinter': 'Automatic',
    'tiburon': 'Automatic', 'spectra': 'Automatic', 'ls': 'Automatic', 'rx 400h': 'Automatic',
    'cl-class': 'Automatic', 'mx-5 miata': 'Manual', 'raider': 'Automatic',
    'sl-class': 'Automatic', 'wave': 'Automatic', 's40': 'Automatic', 'touareg': 'Automatic',
    'tt': 'Automatic', 'blazer': 'Automatic', 'express': 'Automatic', 'colorado': 'Automatic',
    'trailblazer': 'Automatic', 'dakota': 'Automatic', 'neon': 'Manual',
    'freestar': 'Automatic', 'gx': 'Automatic', 'amanti': 'Automatic', 'cherokee': 'Automatic',
    'qx80': 'Automatic', 'montego': 'Automatic', 'bonneville': 'Automatic',
    'pursuit': 'Automatic', 'x-trail': 'Automatic', 'el': 'Automatic', 'lesabre': 'Automatic',
    'century': 'Automatic', 'concorde': 'Automatic', 'tracker': 'Automatic',
    'stratus': 'Automatic', 'intrepid': 'Automatic', 'f250': 'Automatic',
    'canyon': 'Automatic', 'x-type': 'Automatic', '9-5': 'Automatic', 'rsx': 'Manual',
    'v70': 'Automatic', 'venture': 'Automatic', 'h2': 'Automatic', 'protege5': 'Automatic',
    'alero': 'Automatic', 'echo': 'Automatic', 's-10': 'Manual', 'blackwood': 'Automatic',
    'discovery': 'Automatic', 'protege': 'Manual', 'l-series': 'Automatic', 'v40': 'Automatic',
    'cl': 'Automatic', 'trooper': 'Automatic', 'aztek': 'Automatic', 'bravada': 'Automatic',
    'rl': 'Automatic', 's-type': 'Automatic', 'sephia': 'Manual', 'g-class': 'Automatic',
    'intrigue': 'Automatic', 'montero sport': 'Automatic', 'mr2 spyder': 'Manual',
    's70': 'Automatic', 'contour': 'Automatic', 'firebird': 'Automatic',
    'villager': 'Automatic', 'aurora': 'Automatic', 'regal': 'Automatic',
    'seville': 'Automatic', 'escort': 'Manual', 'breeze': 'Manual', 'continental': 'Automatic',
    'lumina': 'Automatic', 'q45': 'Automatic', 'cx-5': 'Automatic', 'nv cargo': 'Automatic',
    'ilx': 'Automatic', 'ats': 'Automatic', 'm5': 'Automatic', 'x1': 'Automatic',
    '4 series': 'Automatic', 'a7': 'Automatic', 'sonic': 'Automatic', 'spark': 'Manual',
    'c-max hybrid': 'Automatic', 'm': 'Automatic', 'jx': 'Automatic', 'qx': 'Automatic',
    'rx 450h': 'Automatic', 'fr-s': 'Manual', 'xv crosstrek': 'Automatic', 'zdx': 'Automatic',
    'captiva sport': 'Automatic', '750li': 'Automatic', 'volt': 'Automatic',
    'crosstour': 'Automatic', 'ex': 'Automatic', 'swift': 'Manual', 'sx4': 'Manual',
    'cadenza': 'Automatic', 'xc': 'Automatic', 'ghibli': 'Automatic', 'sunfire': 'Automatic',
    'cirrus': 'Automatic', '960': 'Automatic', 's80': 'Automatic', 'routan': 'Automatic',
    'lr2': 'Automatic', 'borrego': 'Automatic', '750i': 'Automatic', 'lx 470': 'Automatic',
    'sc 400': 'Automatic', 'corsica': 'Automatic', '850': 'Automatic', 'xts': 'Automatic',
    'aspen': 'Automatic', 'town': 'Automatic', 's4': 'Manual', '626': 'Manual', 'e': 'Automatic',
    'g convertible': 'Automatic', 'insight': 'Manual', 'tribeca': 'Automatic',
    'xlr': 'Automatic', 'twn/cntry': 'Automatic', 'riviera': 'Automatic', 'xl-7': 'Automatic',
    'encore': 'Automatic', 'xa': 'Manual', 'gs 450h': 'Automatic', 'vitara': 'Manual',
    'pathfind': 'Automatic', 'allroad': 'Automatic', 'capt': 'Automatic', 'kizashi': 'Manual',
    'c/v cargo van': 'Automatic', '42c': 'Automatic', 'cr-z': 'Manual', 'nv': 'Automatic',
    '911': 'Manual', 'gt-r': 'Automatic', 'ss': 'Automatic', 'r8': 'Automatic',
    'hs 250h': 'Automatic', 'astra': 'Manual', 'gto': 'Manual', 'v50': 'Automatic',
    'astro': 'Automatic', 's8': 'Automatic', '6': 'Manual', '9-7x': 'Automatic',
    'lhs': 'Automatic', 'rs 6': 'Automatic', 'lx 450': 'Automatic', 'truck': 'Manual',
    'brz': 'Manual', 'v60': 'Automatic', 'f-250': 'Automatic', 's7': 'Automatic',
    'flying spur': 'Automatic', 'transit van': 'Automatic', 'transit wagon': 'Automatic',
    'gallardo': 'Automatic', 'rs 5': 'Automatic',
}

# A handful of manual fixes for specific Make/Model combinations that were
# known to have a missing Body in the source data.
MANUAL_BODY_FIXES = [
    ("lincoln", "mkt", "SUV"), ("bmw", "750i", "Sedan"), ("bmw", "750li", "Sedan"),
    ("ford", "e350", "Van"), ("ford", "e150", "Van"), ("mitsubishi", "galant", "Sedan"),
    ("chevrolet", "g1500", "Van"), ("chrysler", "town", "Minivan"), ("pontiac", "g6", "Sedan"),
    ("chevrolet", "2500", "Pickup Truck"), ("chevrolet", "impala", "Sedan"),
    ("bmw", "7", "Sedan"), ("chevrolet", "hhr", "Wagon"), ("landrover", "lr3", "SUV"),
    ("cadillac", "sts", "Sedan"), ("chevrolet", "corvette", "Coupe"),
    ("landrover", "rangerover", "SUV"), ("landrover", "range", "SUV"),
    ("land rover", "range", "SUV"), ("mitsubishi", "lancer", "Sedan"),
    ("mercedes", "c230wz", "Sedan"), ("mazda", "cx-7", "SUV"),
    ("toyota", "matrix", "Hatchback / Wagon"), ("toyota", "tundra", "Pickup Truck"),
    ("mazda", "mazda5", "Minivan"), ("lexus", "gx", "SUV"), ("gmc truck", "sr", "Pickup Truck"),
    ("honda", "pilot", "SUV"), ("nissan", "350z", "Coupe"),
]


def _apply_manual_body_fixes(df: pd.DataFrame) -> pd.DataFrame:
    for make, model, body in MANUAL_BODY_FIXES:
        mask = (df["Model"] == model) & (df["Make"] == make) & (df["Body"].isna())
        df.loc[mask, "Body"] = body
    return df


def _recover_body_and_transmission(df: pd.DataFrame) -> pd.DataFrame:
    """Recover missing Body (any row) / Transmission (only-null rows) from
    a substring match against the Model text, same as the notebook.

    Matches are anchored to whole words (\\b...\\b) and tried longest-key
    first. Without this, a short lookup key like the single-letter "e" ->
    "Van" entry in BODY_MAP matches as a substring inside unrelated model
    names (e.g. "sorento", "3 series" both contain the letter "e"), silently
    overwriting perfectly good Body values on real-world data.
    """
    mapping_specs = [
        ("Body", BODY_MAP, False),
        ("Transmission", TRANSMISSION_MAP, True),
    ]
    for column, mapping, only_null in mapping_specs:
        series = df["Model"].str.lower()
        keys_sorted = sorted(mapping.keys(), key=len, reverse=True)
        pattern = "|".join(r"\b" + re.escape(k) + r"\b" for k in keys_sorted)
        extracted = series.str.extract(f"({pattern})", expand=False)
        mapped_values = extracted.map(mapping)

        if only_null:
            mask = df[column].isna()
            df.loc[mask, column] = mapped_values.loc[mask]
        else:
            mask = mapped_values.notna()
            df.loc[mask, column] = mapped_values.loc[mask]

    df["Transmission"] = df["Transmission"].replace(["sedan", "Sedan"], "automatic")
    df["Transmission"] = df["Transmission"].str.lower()
    return df


def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline. Returns a new, cleaned DataFrame; does not
    mutate the input."""
    df = df_raw.copy()

    # 1) Drop rows with no Make/Model, drop the unused Trim column
    df.dropna(subset=["Make", "Model"], inplace=True)
    if "Trim" in df.columns:
        df.drop(columns=["Trim"], inplace=True)

    # 2) Manual, known Body fixes for specific Make/Model combos
    df = _apply_manual_body_fixes(df)

    # 3) Recover Body / Transmission from the Model text, clean up values,
    #    drop rows with no VIN (can't be de-duplicated/tracked)
    df = _recover_body_and_transmission(df)
    df.dropna(subset=["VIN"], inplace=True)

    # 4) Normalize text, impute remaining numeric/categorical gaps using
    #    Make/Model medians and modes (falling back to broader groups)
    df["Make"] = df["Make"].str.lower().str.strip()
    df["Model"] = df["Model"].str.lower().str.strip()

    df["ConditionValue"] = (
        df["ConditionValue"]
        .fillna(df.groupby(["Make", "Model"])["ConditionValue"].transform("median"))
        .fillna(df.groupby("Make")["ConditionValue"].transform("median"))
        .fillna(df["ConditionValue"].median())
    )

    df["Odometer"] = df["Odometer"].fillna(
        df.groupby(["Make", "Model"])["Odometer"].transform("median")
    )
    df["Odometer"] = df["Odometer"].fillna(df["Odometer"].median())

    for col in ["Color", "Interior"]:
        group_mode = (
            df.groupby(["Make", "Model"])[col]
            .transform(lambda x: x.mode().iloc[0] if not x.mode().empty else "unknown")
        )
        df[col] = df[col].fillna(group_mode)

    df["MMR"] = (
        df["MMR"]
        .fillna(df.groupby(["Make", "Model", "Year"])["MMR"].transform("median"))
        .fillna(df.groupby(["Make", "Model"])["MMR"].transform("median"))
        .fillna(df["MMR"].median())
    )

    df["SellingPrice"] = df["SellingPrice"].fillna(
        df.groupby(["Make", "Model", "Year"])["SellingPrice"].transform("median")
    )
    df["SellingPrice"] = df["SellingPrice"].fillna(df["SellingPrice"].median())

    df["SaleDate"] = pd.to_datetime(df["SaleDate"])
    df["SaleDate"] = df["SaleDate"].fillna(
        df.groupby(["Make", "Model"])["SaleDate"]
        .transform(lambda x: x.mode().iloc[0] if not x.mode().empty else pd.NaT)
    )
    if df["SaleDate"].isna().any():
        df["SaleDate"] = df["SaleDate"].fillna(df["SaleDate"].mode().iloc[0])

    # 5) Any Body still missing after the substring-match recovery (models
    #    not present in the lookup table) gets the most common body style
    #    for that Make, falling back to the overall most common body style.
    if df["Body"].isna().any():
        make_mode = (
            df.groupby("Make")["Body"]
            .transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
        )
        df["Body"] = df["Body"].fillna(make_mode)
        df["Body"] = df["Body"].fillna(df["Body"].mode().iloc[0])

    # 5b) Same fallback for any Transmission still missing after the
    #     substring-match recovery (models not present in TRANSMISSION_MAP).
    if df["Transmission"].isna().any():
        make_mode = (
            df.groupby("Make")["Transmission"]
            .transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
        )
        df["Transmission"] = df["Transmission"].fillna(make_mode)
        df["Transmission"] = df["Transmission"].fillna(df["Transmission"].mode().iloc[0])

    # 5c) Normalize Body casing. The raw feed mixes cases for the same value
    #     ("Sedan"/"sedan", "SUV"/"suv"), which would otherwise fragment every
    #     chart, dropdown and one-hot-encoded feature into duplicate
    #     categories.
    df["Body"] = df["Body"].astype(str).str.strip().str.title()
    df["Body"] = df["Body"].replace({"Suv": "SUV"})

    # 6) Feature engineering used by the charts and the model
    df["SaleYear"] = df["SaleDate"].dt.year
    df["SaleMonth"] = df["SaleDate"].dt.month
    df["car_age"] = df["SaleYear"] - df["Year"]

    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":
    import os

    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_vehicle_sales.csv")
    raw = pd.read_csv(raw_path)
    clean = clean_data(raw)
    print("raw:", raw.shape, "clean:", clean.shape)
    print(clean.isna().sum()[clean.isna().sum() > 0])
