"""
Synthetic raw data generator.

This mirrors the schema of the SQL Server table the original notebook
reads from (MotoDB.dbo.VehicleSales): Id, VIN, Year, Make, Model, Trim,
Body, Transmission, State, ConditionValue, Odometer, Color, Interior,
Seller, MMR, SellingPrice, SaleDate.

If you have access to the real database or a CSV export, skip this file
entirely -- just point `utils/data_loader.py` at your own raw CSV. This
generator exists so the dashboard works out-of-the-box with a realistic,
similarly-shaped dataset (including the same kinds of missing values the
original notebook had to clean).
"""

import numpy as np
import pandas as pd

RANDOM_STATE = 42

MAKE_MODELS = {
    "toyota": ["camry", "corolla", "rav4", "tacoma", "avalon", "yaris", "highlander", "4runner"],
    "honda": ["accord", "civic", "cr-v", "odyssey", "pilot", "fit", "element"],
    "ford": ["f-150", "focus", "explorer", "fusion", "escape", "mustang", "taurus", "edge"],
    "chevrolet": ["silverado 1500", "malibu", "impala", "cruze", "camaro", "equinox", "tahoe", "corvette"],
    "nissan": ["altima", "sentra", "maxima", "rogue", "murano", "frontier", "titan", "versa"],
    "bmw": ["3 series", "5 series", "x5", "x3", "7 series", "1 series"],
    "mercedes": ["c-class", "e-class", "s-class", "m-class", "glk-class"],
    "hyundai": ["sonata", "elantra", "accent", "santa fe", "tucson", "azera"],
    "kia": ["optima", "forte", "sorento", "sportage", "soul", "rio"],
    "jeep": ["grand cherokee", "wrangler", "liberty", "compass", "patriot"],
    "dodge": ["charger", "challenger", "durango", "avenger", "caliber"],
    "chrysler": ["300", "town and country", "sebring", "200"],
    "volkswagen": ["jetta", "passat", "golf", "tiguan", "cc"],
    "audi": ["a4", "a6", "q5", "a3", "a8"],
    "lexus": ["es 350", "rx 350", "is 250", "gs 430", "ls 460"],
    "mazda": ["mazda3", "mazda6", "cx-7", "cx-9", "mx-5 miata"],
    "subaru": ["outback", "legacy", "forester", "impreza"],
    "gmc": ["sierra 2500hd", "yukon", "acadia", "terrain"],
    "cadillac": ["cts", "srx", "escalade", "dts"],
    "landrover": ["range rover", "lr3", "discovery"],
}

BODY_BY_MODEL_HINT = {
    "f-150": "Truck", "silverado 1500": "Truck", "sierra 2500hd": "Truck", "tacoma": "Truck",
    "frontier": "Truck", "titan": "Truck",
    "explorer": "SUV", "escape": "SUV", "rav4": "SUV", "cr-v": "SUV", "highlander": "SUV",
    "4runner": "SUV", "rogue": "SUV", "murano": "SUV", "x5": "SUV", "x3": "SUV",
    "grand cherokee": "SUV", "wrangler": "SUV", "liberty": "SUV", "compass": "SUV", "patriot": "SUV",
    "santa fe": "SUV", "tucson": "SUV", "sorento": "SUV", "sportage": "SUV", "durango": "SUV",
    "tiguan": "SUV", "q5": "SUV", "rx 350": "SUV", "cx-7": "SUV", "cx-9": "SUV", "outback": "SUV",
    "forester": "SUV", "yukon": "SUV", "acadia": "SUV", "terrain": "SUV", "escalade": "SUV",
    "range rover": "SUV", "lr3": "SUV", "discovery": "SUV", "equinox": "SUV", "tahoe": "SUV",
    "murano ": "SUV",
    "odyssey": "Minivan", "town and country": "Minivan",
    "camaro": "Coupe", "mustang": "Coupe", "corvette": "Coupe", "challenger": "Coupe",
    "mx-5 miata": "Coupe",
    "camry": "Sedan", "corolla": "Sedan", "avalon": "Sedan", "accord": "Sedan", "civic": "Sedan",
    "malibu": "Sedan", "impala": "Sedan", "cruze": "Sedan", "altima": "Sedan", "sentra": "Sedan",
    "maxima": "Sedan", "versa": "Sedan", "3 series": "Sedan", "5 series": "Sedan",
    "7 series": "Sedan", "1 series": "Sedan", "c-class": "Sedan", "e-class": "Sedan",
    "s-class": "Sedan", "sonata": "Sedan", "elantra": "Sedan", "accent": "Sedan",
    "azera": "Sedan", "optima": "Sedan", "forte": "Sedan", "soul": "Sedan", "rio": "Sedan",
    "charger": "Sedan", "avenger": "Sedan", "caliber": "Sedan", "300": "Sedan",
    "sebring": "Sedan", "200": "Sedan", "jetta": "Sedan", "passat": "Sedan", "cc": "Sedan",
    "a4": "Sedan", "a6": "Sedan", "a3": "Sedan", "a8": "Sedan", "es 350": "Sedan",
    "is 250": "Sedan", "gs 430": "Sedan", "ls 460": "Sedan", "mazda3": "Sedan", "mazda6": "Sedan",
    "legacy": "Sedan", "impreza": "Sedan", "cts": "Sedan", "dts": "Sedan",
    "focus": "Hatchback / Wagon", "fit": "Hatchback / Wagon", "golf": "Hatchback / Wagon",
    "yaris": "Hatchback / Wagon", "element": "SUV",
    "fusion": "Sedan", "taurus": "Sedan", "edge": "SUV", "m-class": "SUV", "glk-class": "SUV",
    "srx": "SUV", "pilot": "SUV",
}

TRANSMISSION_BY_MODEL_HINT = {
    "mustang": "manual", "wrangler": "manual", "camaro": "manual", "mx-5 miata": "manual",
    "civic": "automatic", "3 series": "manual",
}

STATES = ["ca", "tx", "fl", "ny", "pa", "il", "ga", "nc", "oh", "mi", "nj", "wa", "az", "va", "co", "in"]
COLORS = ["black", "white", "gray", "silver", "red", "blue", "green", "brown", "beige"]
INTERIORS = ["black", "gray", "beige", "tan", "brown"]
SELLERS = [f"{name} auto group" for name in [
    "sunrise", "capital", "metro", "liberty", "pacific", "atlantic", "midwest",
    "heritage", "summit", "gateway", "premier", "national", "valley", "crown"
]]

BASE_PRICE_BY_BODY = {
    "SUV": 15000, "Truck": 16000, "Sedan": 11000, "Coupe": 13000,
    "Minivan": 10000, "Hatchback / Wagon": 9000,
}


def _pick_body(model):
    return BODY_BY_MODEL_HINT.get(model, "Sedan")


def _pick_transmission(model):
    return TRANSMISSION_BY_MODEL_HINT.get(model, "automatic")


def generate_raw_data(n_rows: int = 12000, seed: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    makes = list(MAKE_MODELS.keys())
    make_choices = rng.choice(makes, size=n_rows, p=_make_weights(makes))

    rows = []
    sale_dates = pd.date_range("2014-01-01", "2015-12-31", freq="D")

    for i in range(n_rows):
        make = make_choices[i]
        model = rng.choice(MAKE_MODELS[make])
        body = _pick_body(model)
        transmission = _pick_transmission(model)
        year = int(rng.integers(1998, 2016))
        sale_date = rng.choice(sale_dates)
        sale_year = pd.Timestamp(sale_date).year
        age = max(sale_year - year, 0)

        condition = float(np.clip(rng.normal(3.4 - 0.06 * age, 0.9), 0.5, 5.0))
        odometer = max(int(rng.normal(12000 * age + 8000, 9000)), 500)

        base = BASE_PRICE_BY_BODY.get(body, 11000)
        depreciation = base * (0.90 ** age)
        mileage_penalty = odometer * 0.045
        condition_bonus = (condition - 3) * 900
        noise = rng.normal(0, 850)
        mmr = max(depreciation - mileage_penalty + condition_bonus + noise + 1200, 800)
        selling_price = max(mmr + rng.normal(0, 550) + (condition - 3) * 150, 500)

        rows.append({
            "Id": i + 1,
            "VIN": f"VIN{100000 + i}",
            "Year": year,
            "Make": make,
            "Model": model,
            "Trim": rng.choice(["base", "se", "le", "sport", "limited", "ex", "lx", np.nan]),
            "Body": body,
            "Transmission": transmission,
            "State": rng.choice(STATES),
            "ConditionValue": round(condition, 1),
            "Odometer": odometer,
            "Color": rng.choice(COLORS),
            "Interior": rng.choice(INTERIORS),
            "Seller": rng.choice(SELLERS),
            "MMR": round(mmr, 2),
            "SellingPrice": round(selling_price, 2),
            "SaleDate": pd.Timestamp(sale_date),
        })

    df = pd.DataFrame(rows)

    # ---- Inject the same kinds of missingness the real dataset has ----
    def blank(col, frac):
        idx = rng.choice(df.index, size=int(len(df) * frac), replace=False)
        df.loc[idx, col] = np.nan

    blank("Body", 0.05)
    blank("Transmission", 0.07)
    blank("ConditionValue", 0.09)
    blank("Odometer", 0.02)
    blank("Color", 0.02)
    blank("Interior", 0.02)
    blank("MMR", 0.015)
    blank("SellingPrice", 0.01)
    blank("SaleDate", 0.005)
    blank("Make", 0.004)
    blank("Model", 0.004)
    blank("VIN", 0.003)

    return df


def _make_weights(makes):
    # A handful of high-volume brands, like a real used-car auction dataset.
    weights = {
        "ford": 0.16, "chevrolet": 0.14, "toyota": 0.12, "nissan": 0.10, "honda": 0.09,
        "hyundai": 0.06, "kia": 0.05, "bmw": 0.05, "mercedes": 0.04, "jeep": 0.04,
        "dodge": 0.03, "chrysler": 0.03, "volkswagen": 0.02, "audi": 0.02, "lexus": 0.02,
        "mazda": 0.01, "subaru": 0.01, "gmc": 0.01, "cadillac": 0.005, "landrover": 0.005,
    }
    w = np.array([weights.get(m, 0.01) for m in makes], dtype=float)
    return w / w.sum()


if __name__ == "__main__":
    df = generate_raw_data()
    print(df.shape)
    print(df.isna().sum())
