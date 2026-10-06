#!/usr/bin/env python3
"""Build the daycare comparison dataset for Lipstikkakuja 14, Rekola.

Sources
- Helsinki region Service Map (Helsinki and Vantaa units within 10 km)
- OpenStreetMap kindergartens, used for Kerava and Tuusula, which the
  service map does not cover
- Municipal fee rules in force from 1 August 2026

The page recomputes the score from the factors stored here, so the weights
can be changed without rebuilding.
"""

from __future__ import annotations

import json
import math
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data.json"
CACHE = Path("/tmp/daycare")

HOME = (60.3381055, 25.0572163)
HOME_LABEL = "Lipstikkakuja 14, 01400 Rekola, Vantaa"
RADIUS_KM = 10

# Early-childhood service ids on the Service Map.
SVC_FI = 663
SVC_EN = 151
SVC_SV = 603
SVC_RU = 773
SVC_FAMILY = 664
SVC_MEALS = 860
SVC_PRESCHOOL = 861
SVC_SHIFT = 831
SVC_EVENING = 200
SVC_SPECIAL = 156
SVC_PRIVATE = 811
CORE = {SVC_FI, SVC_EN, SVC_SV, SVC_RU, SVC_FAMILY, SVC_SHIFT, SVC_EVENING, SVC_PRIVATE, 569, 292, 614, 164}

PRESCHOOL_ONLY_OK = True


def hav(lat1, lon1, lat2, lon2) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def norm(name: str) -> str:
    name = name.lower().replace("ä", "a").replace("ö", "o").replace("å", "a")
    name = re.sub(r"[^a-z0-9]+", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def txt(value) -> str:
    if isinstance(value, dict):
        return (value.get("fi") or value.get("en") or value.get("sv") or "").strip()
    return (value or "").strip() if isinstance(value, str) else ""


def clean_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\n", " ")).strip()


def hours_of(unit) -> str:
    lines = []
    for c in unit.get("connections") or []:
        if c.get("section_type") == "OPENING_HOURS":
            lines.append(txt(c.get("name")))
    if not lines:
        return ""
    raw = clean_space(lines[0])
    raw = raw.replace("–", "-").replace("—", "-")
    raw = re.sub(
        r"(?i)(valid for the time being|voimassa toistaiseksi|gäller tills vidare)\s*:?\s*",
        "",
        raw,
    )
    raw = re.sub(r"(?i)\bma-pe\b", "Mon-Fri", raw)
    raw = re.sub(r"(?i)\bma-su\b", "Mon-Sun", raw)
    raw = re.sub(r"(?i)\bmån-fre\b", "Mon-Fri", raw)
    raw = re.sub(r"(?i)\bmon-fri\b", "Mon-Fri", raw)
    raw = re.sub(r"(?i)\bmon-sun\b", "Mon-Sun", raw)
    raw = re.sub(r"(?i)ennalta sovitun tarpeen mukaan", "when arranged", raw)
    raw = re.sub(r"(?i)\bsat closed\b", "Sat closed", raw)
    raw = re.sub(r"(?i)\bsun closed\b", "Sun closed", raw)
    raw = re.sub(r"\s*-\s*la suljettu\s*-\s*su suljettu", "", raw, flags=re.I)
    return raw.strip(" -")[:180]


def contact_of(unit):
    phone, email, person = "", "", ""
    for c in unit.get("connections") or []:
        if c.get("section_type") != "PHONE_OR_EMAIL":
            continue
        role = txt(c.get("name")).lower()
        if not phone and c.get("phone"):
            phone = c["phone"]
            person = c.get("contact_person") or txt(c.get("name"))
        if "johtaja" in role or "director" in role or "manager" in role:
            phone = c.get("phone") or phone
            email = c.get("email") or email
            person = c.get("contact_person") or person
            break
        email = email or (c.get("email") or "")
    if not email:
        email = unit.get("email") or ""
    if email and "etunimi.sukunimi" in email:
        email = ""
    return phone, email, person


def website_of(unit) -> str:
    www = unit.get("www") or {}
    if isinstance(www, dict):
        return www.get("en") or www.get("fi") or www.get("sv") or ""
    return www or ""


def curriculum_of(name: str, blob: str) -> list[str]:
    text = f"{name} {blob}".lower()
    found = []
    rules = [
        ("montessori", "Montessori"),
        ("reggio", "Reggio Emilia"),
        ("steiner", "Steiner pedagogy"),
        ("stainer", "Steiner pedagogy"),
        ("tiedep", "Science"),
        ("luonnontiede", "Science"),
        ("luontop", "Nature"),
        ("luonnon lähe", "Nature nearby"),
        ("liikuntap", "Sports and movement"),
        ("liikunta", "Sports and movement"),
        ("seikkailu", "Adventure and outdoors"),
        ("musiikki", "Music"),
        ("ilmaisu", "Arts and expression"),
        ("taidepäiväkoti", "Arts"),
        ("kielikylpy", "Language immersion"),
        ("kielisuihku", "English language shower"),
        ("kielirikaste", "Language-enriched pre-primary"),
        ("kaksikiel", "Bilingual programme"),
    ]
    for needle, label in rules:
        if needle in text and label not in found:
            found.append(label)
    if "Bilingual programme" in found and "English language shower" in found:
        found = [f for f in found if f != "English language shower"]
    return found[:4]


def age_from_text(blob: str, services: set[int], name: str) -> tuple[str, str, float]:
    low = blob.lower()
    title = name.lower()
    if "esiopetusryhm" in title or re.search(r"vain esiopet", low):
        return (
            "preschool",
            "Pre-primary only (around age 6)",
            0.08,
        )
    patterns = [
        (r"0\s*[-–]\s*6\s*[- ]?vuot", "Ages 0–6", 1.0),
        (r"1\s*[-–]\s*6\s*[- ]?vuot", "Ages 1–6", 1.0),
        (r"1\s*[-–]\s*5\s*[- ]?vuot", "Ages 1–5", 1.0),
        (r"0\s*[-–]\s*3", "Under-3 group", 1.0),
        (r"alle\s*3", "Under-3 places", 1.0),
        (r"1\s*[-–]\s*3", "Ages 1–3", 1.0),
        (r"1\s*[-–]\s*2\s*vuot", "Ages 1–2", 1.0),
        (r"taapero", "Toddler group", 1.0),
        (r"pikkulaps", "Young-child group", 1.0),
    ]
    for pat, label, factor in patterns:
        if re.search(pat, low):
            return "strong", label, factor
    if services & {SVC_FAMILY}:
        return "likely", "Small group family daycare, mixed ages", 0.72
    preschoolish = low.startswith("tarjoamme normaaliaikaista esiopetusta") or (
        "esiopetusta ja sitä täydentävää" in low and not re.search(r"\d\s*[-–]\s*\d", low)
    )
    if preschoolish and "1-" not in low and "0-" not in low:
        return (
            "weak",
            "Description leads with pre-primary education",
            0.35,
        )
    if services & {SVC_FI, SVC_EN, SVC_SV, SVC_RU, SVC_SHIFT, SVC_EVENING}:
        return "likely", "Early childhood education; group ages not published", 0.78
    if SVC_PRESCHOOL in services and not (services & CORE):
        return "preschool", "Pre-primary only (around age 6)", 0.08
    return "likely", "Daycare; group ages not published", 0.7


def language_of(name: str, blob: str, services: set[int]) -> tuple[str, str, float]:
    low = f"{name} {blob}".lower()
    extensive = "laajamittaista" in low or "75 %" in low or "75%" in low
    if SVC_EN in services or (extensive and "englann" in low):
        if "75" in low:
            return "english", "English about 75%, Finnish about 25%", 1.0
        if "kaksikiel" in low or SVC_FI in services:
            return "english", "Bilingual Finnish and English", 1.0
        return "english", "English-language daycare", 1.0
    if "kielisuihku" in low and "englann" in low:
        return "shower", "Finnish, with an English language shower", 0.55
    if "kielirikaste" in low and "englann" in low:
        return "shower", "Finnish; English enrichment is described for pre-primary", 0.42
    if SVC_SV in services or 862 in services or "ruotsinkiel" in low:
        return "swedish", "Swedish", 0.24
    if SVC_RU in services or "venäj" in low:
        return "russian", "Russian and Finnish", 0.18
    # Match the language, not a street name such as Nissaksentie.
    if re.search(r"saksankiel|german-language|\bspielhaus\b", low):
        return "german", "German", 0.22
    if SVC_FI in services or SVC_FAMILY in services or 861 in services or "suomenkiel" in low or "varhaiskasvat" in low:
        return "finnish", "Finnish", 0.34
    return "unknown", "Language not stated in the open data", 0.30


def sector_of(provider: str, contract: str) -> tuple[str, str]:
    if provider == "VOUCHER_SERVICE" or contract == "VOUCHER_SERVICE":
        return "voucher", "Private, Vantaa service voucher"
    if provider == "SELF_PRODUCED" or contract == "MUNICIPAL_SERVICE":
        return "municipal", "Municipal"
    return "private", "Private"


def factors_for_sector(municipality: str, sector: str) -> tuple[float, float, str, str]:
    """Return access factor, price factor, price band, price label."""
    if municipality == "vantaa" and sector == "municipal":
        return (
            1.0,
            1.0,
            "municipal-cap",
            "Income-based municipal fee, at most €335/month full-time. Meals included.",
        )
    if municipality == "vantaa" and sector == "voucher":
        return (
            0.92,
            0.94,
            "voucher-vantaa",
            "Vantaa service voucher. The family fee is at most €30/month above the municipal fee.",
        )
    if municipality == "vantaa" and sector == "private":
        return (
            0.62,
            0.38,
            "private-unknown",
            "Private fee. Vantaa's voucher cap may not apply; ask for the family share.",
        )
    if sector == "municipal":
        return (
            0.22,
            1.0,
            "municipal-cap",
            "Same national fee rules if a place were granted (max €335/month). A Vantaa resident is unlikely to be offered one.",
        )
    if sector == "voucher":
        return (
            0.48,
            0.55,
            "voucher-other",
            "Service voucher from this municipality, not automatically from Vantaa. Confirm what a Rekola family pays.",
        )
    return (
        0.48,
        0.38,
        "private-unknown",
        "Private fee for a non-resident. Vantaa's €30 voucher cap probably does not apply.",
    )


def summary_for(name, city, language_label, age_label, sector_label, km, curriculum) -> str:
    focus = ""
    if curriculum:
        focus = " Focus: " + ", ".join(curriculum[:3]) + "."
    return (
        f"{name} in {city}, {km:.1f} km from Lipstikkakuja 14. {sector_label}. "
        f"Language: {language_label}. {age_label}.{focus}"
    )


def build_notes(row: dict) -> tuple[list[str], list[str], list[str]]:
    pros, cons, traits = [], [], []
    km = row["distanceKm"]
    if km <= 1.2:
        pros.append(f"{km:.1f} km from home, close enough to walk with a stroller.")
    elif km >= 6:
        cons.append(f"{km:.1f} km from Rekola, so both drop-off and pick-up are a commute.")
    elif km >= 4:
        cons.append(f"{km:.1f} km away. Doable by car or train, not a daily walk.")

    lang = row["language"]
    if lang == "english":
        pros.append(f"{row['languageLabel']}. This is the closest match to wanting English first and Finnish as a bonus.")
    elif lang == "shower":
        pros.append(row["languageLabel"] + ".")
        cons.append("English here is a light addition or aimed at pre-primary, not the toddler day.")
    elif lang == "finnish":
        cons.append("The day runs in Finnish. Useful long-term, and not the English start you asked for.")
    elif lang == "swedish":
        cons.append("Swedish-language daycare. Strong if you want Swedish, off-target for English.")
    elif lang == "russian":
        cons.append("Russian and Finnish, rather than English.")
    elif lang == "german":
        cons.append("German-language programme, rather than English.")
    else:
        cons.append("The open data does not say which language the adults speak with the children.")

    if row["ageFit"] == "strong":
        pros.append(f"{row['ageLabel']}, which fits a child who will be about 15 months in November 2027.")
    elif row["ageFit"] == "likely":
        pros.append("Registered for early childhood education, the right service at 15 months. Confirm the toddler group has a free place.")
    elif row["ageFit"] == "weak":
        cons.append("The public text leads with pre-primary education. Ask whether a one-year-old can start here in November 2027.")
    else:
        cons.append("Pre-primary education is for children in the year before school, around age six. It does not fit this start.")

    if row["municipality"] == "vantaa" and row["sector"] == "municipal":
        pros.append("Municipal Vantaa place. Apply in VaSa at least four months ahead, so by early July 2027 for a November start.")
        pros.append("Fee follows family income. Full-time care is at most €335/month from 1 August 2026, meals included. July 2028 is unlikely to be the free month, because a November 2027 start is after September 2027.")
    elif row["municipality"] == "vantaa" and row["sector"] == "voucher":
        pros.append("Accepts the Vantaa service voucher. The city caps your monthly fee at €30 above the equivalent municipal fee.")
        cons.append("The voucher does not hold the seat. The daycare also has to accept him, and English or small houses fill before the municipal deadline.")
    elif row["municipality"] != "vantaa" and row["sector"] == "municipal":
        cons.append(f"A {row['city']} municipal place is organised for {row['city']} residents. Living in Vantaa, you should not count on being offered one.")
    else:
        cons.append("Outside the Vantaa voucher list, or private without a published family fee. Ask what a Vantaa family pays after any Kela private-care support.")

    for label in row["curriculum"]:
        if label in {"Montessori", "Reggio Emilia", "Steiner pedagogy", "Science", "Sports and movement", "Music", "Arts", "Arts and expression", "Adventure and outdoors", "Nature"}:
            traits.append(label)
    if traits:
        pros.append("Distinct programme: " + ", ".join(traits[:3]) + ".")

    if "shift" in row["traits"]:
        traits.append("Round-the-clock care")
        cons.append("Set up for shift and overnight care. Ask whether a regular daytime toddler place exists.")
    if "evening" in row["traits"]:
        traits.append("Evening care")
    if "special" in row["traits"]:
        traits.append("Has a special-education group")
    if "family" in row["traits"]:
        cons.append("Group family daycare is small and home-like, usually with a shorter day than a daycare centre.")
    if row.get("hours"):
        h = row["hours"].lower()
        if re.search(r"7\.30-16\.30|7:30-16:30|8\.00-16", h):
            cons.append(f"Opening hours are short for a full workday ({row['hours']}).")
        elif re.search(r"(?<!\d)6[:.]", h):
            traits.append(f"Opens early ({row['hours']})")

    if not pros:
        pros.append("Included so the 10 km map is complete. It is a weak match for a November 2027 start.")

    # De-duplicate while keeping order, cap length.
    def uniq(items, limit):
        out = []
        for item in items:
            if item and item not in out:
                out.append(item)
            if len(out) == limit:
                break
        return out

    return uniq(pros, 4), uniq(cons, 4), uniq(traits, 6)


def from_servicemap(unit) -> dict | None:
    services = set(unit.get("services") or [])
    name = txt(unit.get("name"))
    if not name:
        return None
    is_core = bool(services & CORE)
    is_preschool_unit = SVC_PRESCHOOL in services and not is_core
    if not is_core and not (PRESCHOOL_ONLY_OK and is_preschool_unit):
        return None
    # Drop info desks and clubs that also carry a stray preschool tag? Preschool units are named päiväkoti.
    if not re.search(r"päiväkoti|daghem|daycare|kindergarten|perhepäiv|playschool|kiddy", name, re.I):
        if not is_core:
            return None
    lon, lat = unit["location"]["coordinates"]
    km = unit.get("distance")
    km = (km / 1000.0) if isinstance(km, (int, float)) else hav(HOME[0], HOME[1], lat, lon)
    if km > RADIUS_KM + 0.05:
        return None
    blob = clean_space(txt(unit.get("description")) + " " + txt(unit.get("short_description")))
    municipality = (unit.get("municipality") or "").lower()
    city = {"vantaa": "Vantaa", "helsinki": "Helsinki"}.get(municipality, municipality.title())
    contract = (unit.get("contract_type") or {}).get("id") or ""
    sector, sector_label = sector_of(unit.get("provider_type") or "", contract)
    if municipality != "vantaa" and sector == "voucher":
        sector_label = f"Private, {city} service voucher"
    lang, lang_label, lang_f = language_of(name, blob, services)
    age, age_label, age_f = age_from_text(blob, services, name)
    access_f, price_f, price_band, price_label = factors_for_sector(municipality, sector)
    curriculum = curriculum_of(name, blob)
    if SVC_MEALS in services and "Meals included" not in curriculum:
        curriculum.append("Meals included")
    phone, email, person = contact_of(unit)
    extra_traits = []
    if SVC_SHIFT in services:
        extra_traits.append("shift")
    if SVC_EVENING in services:
        extra_traits.append("evening")
    if SVC_SPECIAL in services:
        extra_traits.append("special")
    if SVC_FAMILY in services:
        extra_traits.append("family")
        sector_label = sector_label + ", group family daycare"
    address = txt(unit.get("street_address"))
    row = {
        "id": f"sm-{unit['id']}",
        "name": name,
        "lat": lat,
        "lon": lon,
        "address": address,
        "zip": unit.get("address_zip") or "",
        "city": city,
        "municipality": municipality,
        "distanceKm": round(km, 2),
        "sector": sector,
        "sectorLabel": sector_label,
        "language": lang,
        "languageLabel": lang_label,
        "languageFactor": lang_f,
        "ageFit": age,
        "ageLabel": age_label,
        "ageFactor": age_f,
        "accessFactor": access_f,
        "priceBand": price_band,
        "priceLabel": price_label,
        "priceFactor": price_f,
        "curriculum": curriculum,
        "hours": hours_of(unit),
        "phone": phone,
        "contact": person,
        "email": email,
        "website": website_of(unit),
        "summary": "",
        "pros": [],
        "cons": [],
        "traits": extra_traits,
        "source": "Helsinki region Service Map",
        "sourceUrl": f"https://palvelukartta.hel.fi/unit/{unit['id']}",
        "confidence": "high",
    }
    # Specific corrections from the unit text, where the generic rules are too blunt.
    if "pohjantähti" in name.lower() or "pohjantahti" in norm(name):
        row["language"] = "english"
        row["languageLabel"] = "Bilingual Finnish and English, extensive"
        row["languageFactor"] = 1.0
        row["ageFit"] = "strong"
        row["ageLabel"] = "Bilingual early education for young children through pre-primary"
        row["ageFactor"] = 1.0
        row["summary"] = (
            "Pilke Playschool Pohjantähti in Koivuhaka runs an extensive bilingual programme: "
            "English is the main language of the groups and Finnish stays in the day. "
            "It accepts the Vantaa service voucher, so the fee stays close to a municipal place. "
            "Open Mon-Fri 6:15–17:00."
        )
    if name.lower().startswith("y.e.s"):
        row["language"] = "english"
        row["languageLabel"] = "English about 75%, Finnish about 25%"
        row["languageFactor"] = 1.0
        row["ageFit"] = "strong"
        row["ageLabel"] = "Eight groups, including English groups below pre-primary age"
        row["ageFactor"] = 0.92
        row["summary"] = (
            "Y.E.S. is Vantaa's own extensive bilingual daycare at Kartanonkoski, inside the POINT building "
            "with the international school. About three quarters of the day is in English and a quarter in Finnish. "
            "Pre-primary hours 9–13 are entirely in English. It is a municipal fee, and it serves families from across Vantaa."
        )
    if "little tots" in name.lower():
        row["language"] = "english"
        row["languageLabel"] = "English-language private daycare"
        row["languageFactor"] = 1.0
        row["summary"] = (
            "Little Tots International in Malmi is a private English-language daycare. "
            "It sits in Helsinki, almost 10 km away, and the service-map record does not publish a fee."
        )
    if "emilia" in name.lower():
        row["curriculum"] = ["Montessori", "Reggio Emilia", "English language shower"]
        row["language"] = "shower"
        row["languageLabel"] = "Finnish, with an English language shower"
        row["languageFactor"] = 0.55
        row["ageFit"] = "strong"
        row["ageLabel"] = "Ages 0–6, 18 places"
        row["ageFactor"] = 1.0
    if "maauuninpolun" in name.lower():
        row["language"] = "shower"
        row["languageLabel"] = "Finnish daycare; English enrichment is described for pre-primary"
        row["languageFactor"] = 0.42
    if "karuselli" in name.lower():
        row["priceLabel"] = (
            "Vantaa service voucher. The daycare says the under-3 fee matches the city, "
            "and the over-3 fee is about €10/month higher."
        )
        row["ageFit"] = "strong"
        row["ageLabel"] = "Ages 0–6"
        row["ageFactor"] = 1.0
    if "montsa" in name.lower():
        row["ageFit"] = "strong"
        row["ageLabel"] = "Under-3 group (Tähti) and a 3–6 group"
        row["ageFactor"] = 1.0
        row["curriculum"] = ["Montessori", "Meals included"]
    if "kiddy" in name.lower():
        pass
    pros, cons, traits = build_notes(row)
    row["pros"] = pros
    row["cons"] = cons
    row["traits"] = traits
    if not row["summary"]:
        row["summary"] = summary_for(
            name, city, row["languageLabel"], row["ageLabel"], sector_label, km, [c for c in curriculum if c != "Meals included"]
        )
    return row


def load_servicemap() -> list[dict]:
    cache = CACHE / "units_raw.json"
    if cache.exists():
        units = json.loads(cache.read_text())
    else:
        units = []
        page = 1
        while True:
            params = urllib.parse.urlencode(
                {
                    "service_node": "868",
                    "lat": str(HOME[0]),
                    "lon": str(HOME[1]),
                    "distance": "10000",
                    "page_size": "100",
                    "page": str(page),
                }
            )
            with urllib.request.urlopen("https://api.hel.fi/servicemap/v2/unit/?" + params, timeout=60) as resp:
                data = json.load(resp)
            units.extend(data["results"])
            if not data.get("next"):
                break
            page += 1
    rows = []
    for unit in units:
        row = from_servicemap(unit)
        if row:
            rows.append(row)
    return rows


def guess_municipality(tags: dict, lat: float, lon: float) -> str:
    city = (tags.get("addr:city") or "").lower()
    if "vantaa" in city or "vanda" in city:
        return "vantaa"
    if "helsinki" in city or "helsing" in city:
        return "helsinki"
    if "kerava" in city or "kervo" in city:
        return "kerava"
    if "tuusula" in city or "tusby" in city:
        return "tuusula"
    if lat >= 60.37 and lon >= 25.07:
        return "kerava"
    if lat >= 60.37 and lon < 25.07:
        return "tuusula"
    if lat < 60.30:
        return "helsinki"
    return "vantaa"


# Hand-checked centres the service map misses, mostly Kerava and Tuusula.
MANUAL = {
    "kiddy house": {
        "name": "Pilke Playschool Kiddy House",
        "address": "Tiilitehtaankatu 10",
        "zip": "04250",
        "city": "Kerava",
        "municipality": "kerava",
        "lat": 60.3783473,
        "lon": 25.0985858,
        "sector": "private",
        "sectorLabel": "Private bilingual daycare",
        "language": "english",
        "languageLabel": "Bilingual Finnish and English",
        "languageFactor": 1.0,
        "ageFit": "strong",
        "ageLabel": "Ages 0–6",
        "ageFactor": 1.0,
        "curriculum": ["Bilingual Finnish and English", "National ECEC curriculum"],
        "hours": "Mon-Fri, daytime groups (confirm the exact clock times)",
        "website": "https://pilkepaivakodit.fi/en/paivakodit/kerava/playschool-kiddy-house-2/",
        "phone": "+358 40 451 7034",
        "contact": "Nina Finsk",
        "email": "nina.finsk@pilkepaivakodit.fi",
        "confidence": "medium",
        "summary": (
            "Pilke Playschool Kiddy House is a small bilingual daycare in Kerava for ages 0–6. "
            "Finnish and English are both everyday languages. Kerava, Tuusula and Järvenpää grant service vouchers for it. "
            "A Vantaa voucher is a separate question: ask Pilke whether a Rekola family can use one, or what the private fee is. "
            "An older map pin sits on Annikinkatu; Pilke's own page gives Tiilitehtaankatu 10, which is the pin used here."
        ),
    },
    "spielhaus": {
        "language": "german",
        "languageLabel": "German",
        "languageFactor": 0.22,
        "sector": "private",
        "sectorLabel": "Private, Kerava",
        "curriculum": ["German-language programme"],
        "ageFit": "likely",
        "ageLabel": "Early childhood education; confirm toddler places",
        "ageFactor": 0.7,
        "confidence": "medium",
    },
    "montessoripaivakoti mio": {
        "language": "finnish",
        "languageLabel": "Finnish",
        "languageFactor": 0.34,
        "sector": "private",
        "sectorLabel": "Private Montessori, Kerava",
        "curriculum": ["Montessori"],
        "ageFit": "likely",
        "ageLabel": "Montessori daycare; confirm the under-3 group",
        "ageFactor": 0.78,
        "website": "https://www.montessori-mio.fi/",
        "confidence": "medium",
    },
    "taidepaivakoti konsti": {
        "curriculum": ["Arts"],
        "sector": "private",
        "sectorLabel": "Private arts daycare, Kerava",
        "confidence": "medium",
    },
    "stainerpaivakoti pohjantahti": {
        "name": "Steinerpäiväkoti Pohjantähti",
        "curriculum": ["Steiner pedagogy"],
        "language": "finnish",
        "languageLabel": "Finnish, Steiner pedagogy",
        "languageFactor": 0.34,
        "sector": "private",
        "sectorLabel": "Private Steiner daycare, Tuusula",
        "municipality": "tuusula",
        "city": "Tuusula",
        "summary": (
            "This is the Steiner daycare in Tuusula, not Pilke Playschool Pohjantähti in Koivuhaka. "
            "The programme follows Steiner pedagogy in Finnish. It is outside Vantaa's voucher system."
        ),
        "confidence": "medium",
    },
    "norlandia pikkukarhu": {
        "sector": "private",
        "sectorLabel": "Private, Tuusula",
        "municipality": "tuusula",
        "city": "Tuusula",
        "confidence": "medium",
    },
    "norlandia kipina": {
        "sector": "private",
        "sectorLabel": "Private, Kerava",
        "confidence": "medium",
    },
    "liikuntapaivakoti huiske": {
        "curriculum": ["Sports and movement"],
        "sector": "private",
        "sectorLabel": "Private sports daycare, Tuusula",
        "municipality": "tuusula",
        "city": "Tuusula",
        "confidence": "medium",
    },
    "aarteiden talo": {
        "sector": "private",
        "sectorLabel": "Private Pilke daycare",
        "confidence": "low",
    },
}


def manual_key(name: str) -> str | None:
    n = norm(name)
    for key in MANUAL:
        if key in n or n in key:
            return key
    return None


def ensure_osm() -> None:
    cache = CACHE / "osm.json"
    if cache.exists():
        return
    CACHE.mkdir(parents=True, exist_ok=True)
    query = (
        "[out:json][timeout:80];("
        "node[\"amenity\"=\"kindergarten\"](around:10000,60.3381055,25.0572163);"
        "way[\"amenity\"=\"kindergarten\"](around:10000,60.3381055,25.0572163);"
        "relation[\"amenity\"=\"kindergarten\"](around:10000,60.3381055,25.0572163);"
        ");out center tags;"
    )
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": query}).encode(),
        headers={"User-Agent": "rekola-daycare/1.0"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        cache.write_bytes(resp.read())


def from_osm(existing_names: set[str], existing_points: list[tuple[float, float]]) -> list[dict]:
    ensure_osm()
    cache = CACHE / "osm.json"
    if not cache.exists():
        return []
    data = json.loads(cache.read_text())
    rows = []
    seen = set()
    for el in data.get("elements") or []:
        tags = el.get("tags") or {}
        name = tags.get("name") or ""
        if not name or name.strip("?") == "":
            continue
        n = norm(name)
        if n in seen or n in existing_names:
            continue
        if any(bad in n for bad in ["sivukoulu", "toimintakeskus", "leikkipuisto", "kerho"]):
            continue
        lat = el.get("lat") or (el.get("center") or {}).get("lat")
        lon = el.get("lon") or (el.get("center") or {}).get("lon")
        if lat is None:
            continue
        if any(hav(lat, lon, la, lo) < 0.12 for la, lo in existing_points):
            continue
        km = hav(HOME[0], HOME[1], lat, lon)
        if km > RADIUS_KM:
            continue
        municipality = guess_municipality(tags, lat, lon)
        # Service map already covers Vantaa and Helsinki thoroughly. OSM extras there
        # are usually duplicate buildings or unnamed wings.
        if municipality in {"vantaa", "helsinki"} and not manual_key(name):
            continue
        seen.add(n)
        city = {"kerava": "Kerava", "tuusula": "Tuusula", "vantaa": "Vantaa", "helsinki": "Helsinki"}[municipality]
        sector = "municipal"
        sector_label = f"Municipal, {city}"
        lang, lang_label, lang_f = "finnish", "Finnish (not confirmed in a city register extract)", 0.30
        age, age_label, age_f = (
            "likely",
            f"{city} daycares include under-3 groups; this building's groups are not in the extract",
            0.7,
        )
        curriculum = []
        address = " ".join(x for x in [tags.get("addr:street"), tags.get("addr:housenumber")] if x)
        zip_code = tags.get("addr:postcode") or ""
        hours = "Kerava municipal daycares can open 6:00–18:00 when the family needs it." if municipality == "kerava" and sector == "municipal" else ""
        website = ""
        phone = ""
        email = ""
        contact = ""
        confidence = "low"
        summary = ""
        key = manual_key(name)
        if key:
            over = MANUAL[key]
            name = over.get("name", name)
            address = over.get("address", address)
            zip_code = over.get("zip", zip_code)
            city = over.get("city", city)
            municipality = over.get("municipality", municipality)
            lat = over.get("lat", lat)
            lon = over.get("lon", lon)
            km = hav(HOME[0], HOME[1], lat, lon)
            sector = over.get("sector", sector)
            sector_label = over.get("sectorLabel", sector_label)
            lang = over.get("language", lang)
            lang_label = over.get("languageLabel", lang_label)
            lang_f = over.get("languageFactor", lang_f)
            age = over.get("ageFit", age)
            age_label = over.get("ageLabel", age_label)
            age_f = over.get("ageFactor", age_f)
            curriculum = over.get("curriculum", curriculum)
            hours = over.get("hours", hours)
            website = over.get("website", website)
            phone = over.get("phone", phone)
            email = over.get("email", email)
            contact = over.get("contact", contact)
            confidence = over.get("confidence", "medium")
            summary = over.get("summary", "")
        elif municipality == "kerava":
            lang_f = 0.34
            lang_label = "Finnish"
            lang = "finnish"
            confidence = "medium"
            summary = (
                f"{name} is one of Kerava's municipal daycares, {km:.1f} km from Rekola. "
                "Kerava runs under-3, 3–5 and 1–5 groups, and centres can open 6:00–18:00. "
                "Which groups sit in this building is not in the open extract. "
                "A municipal place is for Kerava residents."
            )
        elif municipality == "tuusula":
            lang = "finnish"
            lang_label = "Finnish"
            lang_f = 0.34
            confidence = "low"
        access_f, price_f, price_band, price_label = factors_for_sector(municipality, sector)
        row = {
            "id": f"osm-{el.get('id')}",
            "name": name,
            "lat": lat,
            "lon": lon,
            "address": address,
            "zip": zip_code,
            "city": city,
            "municipality": municipality,
            "distanceKm": round(km, 2),
            "sector": sector,
            "sectorLabel": sector_label,
            "language": lang,
            "languageLabel": lang_label,
            "languageFactor": lang_f,
            "ageFit": age,
            "ageLabel": age_label,
            "ageFactor": age_f,
            "accessFactor": access_f,
            "priceBand": price_band,
            "priceLabel": price_label,
            "priceFactor": price_f,
            "curriculum": curriculum,
            "hours": hours,
            "phone": phone,
            "contact": contact,
            "email": email,
            "website": website,
            "summary": summary,
            "pros": [],
            "cons": [],
            "traits": [],
            "source": "OpenStreetMap, checked against municipal pages where noted",
            "sourceUrl": f"https://www.openstreetmap.org/{el.get('type')}/{el.get('id')}",
            "confidence": confidence,
        }
        pros, cons, traits = build_notes(row)
        if confidence != "high":
            cons.append("Fewer official details than the Vantaa and Helsinki register. Confirm groups, hours and fees before applying.")
        row["pros"] = pros
        row["cons"] = cons[:4]
        row["traits"] = traits
        if not row["summary"]:
            row["summary"] = summary_for(name, city, lang_label, age_label, sector_label, km, curriculum)
        rows.append(row)
    # Kiddy House may not be merged if the OSM name did not match after coordinate skip.
    if not any("kiddy" in r["name"].lower() for r in rows):
        over = MANUAL["kiddy house"]
        lat, lon = over["lat"], over["lon"]
        km = hav(HOME[0], HOME[1], lat, lon)
        access_f, price_f, price_band, price_label = factors_for_sector("kerava", "private")
        row = {
            "id": "manual-kiddy-house",
            "name": over["name"],
            "lat": lat,
            "lon": lon,
            "address": over["address"],
            "zip": over["zip"],
            "city": "Kerava",
            "municipality": "kerava",
            "distanceKm": round(km, 2),
            "sector": "private",
            "sectorLabel": over["sectorLabel"],
            "language": "english",
            "languageLabel": over["languageLabel"],
            "languageFactor": 1.0,
            "ageFit": "strong",
            "ageLabel": over["ageLabel"],
            "ageFactor": 1.0,
            "accessFactor": access_f,
            "priceBand": price_band,
            "priceLabel": price_label,
            "priceFactor": price_f,
            "curriculum": over["curriculum"],
            "hours": over["hours"],
            "phone": over["phone"],
            "contact": over["contact"],
            "email": over["email"],
            "website": over["website"],
            "summary": over["summary"],
            "pros": [],
            "cons": [],
            "traits": [],
            "source": "Pilke Playschool page, geocoded to Tiilitehtaankatu 10",
            "sourceUrl": over["website"],
            "confidence": "medium",
        }
        pros, cons, traits = build_notes(row)
        cons.append("Kerava is not your home municipality. Confirm whether a Vantaa service voucher is accepted.")
        row["pros"] = pros
        row["cons"] = cons[:4]
        row["traits"] = traits
        rows.append(row)
    return rows


def main() -> None:
    rows = load_servicemap()
    names = {norm(r["name"]) for r in rows}
    points = [(r["lat"], r["lon"]) for r in rows]
    extra = from_osm(names, points)
    # Drop OSM rows that duplicate a manual insert.
    seen = {norm(r["name"]) for r in rows}
    for row in extra:
        key = norm(row["name"])
        if key in seen:
            continue
        if any(hav(row["lat"], row["lon"], r["lat"], r["lon"]) < 0.08 and norm(r["name"])[:8] == key[:8] for r in rows):
            continue
        rows.append(row)
        seen.add(key)

    payload = {
        "home": {"label": HOME_LABEL, "lat": HOME[0], "lon": HOME[1], "radiusKm": RADIUS_KM},
        "child": {
            "asOf": "2026-10-06",
            "ageNow": "7 weeks",
            "bornApprox": "mid-August 2026",
            "start": "November 2027",
            "ageAtStart": "about 15 months",
            "applyBy": "early July 2027",
        },
        "fees": {
            "effective": "2026-08-01",
            "maxFullTimeEur": 335,
            "secondChildEur": 134,
            "minFeeEur": 32,
            "vantaaVoucherSurchargeMaxEur": 30,
            "nextIndex": "2028-08-01",
            "note": (
                "Municipal early childhood education fees are set by law and depend on family size, "
                "gross income and weekly hours. From 1 August 2026 the full-time maximum for the youngest "
                "child is €335 a month. The next index adjustment is 1 August 2028, so a November 2027 start "
                "uses the August 2026 schedule unless the law changes. Vantaa limits the family fee at a "
                "voucher daycare to €30 a month above the municipal fee."
            ),
        },
        "weights": {"language": 32, "distance": 18, "age": 20, "access": 15, "price": 15},
        "generated": "2026-10-06",
        "daycares": rows,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"wrote {len(rows)} daycares to {OUT}")


if __name__ == "__main__":
    main()
