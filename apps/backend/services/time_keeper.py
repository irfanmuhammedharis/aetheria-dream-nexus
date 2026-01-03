# apps/backend/services/time_keeper.py
import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple
import sys
import os

# Add packages to path - use absolute path resolution
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repo_root = os.path.dirname(os.path.dirname(backend_dir))
sys.path.insert(0, os.path.join(repo_root, 'packages', 'shared-schema', 'src'))

from schemas import Planet

# Initialize ephemeris path
swe.set_ephe_path(os.getenv("SWEPHE_PATH", "/usr/share/ephe"))

# ============================================================================
# NAKSHATRA CALCULATION (27 Lunar Mansions)
# ============================================================================

NAKSHATRA_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_DEITIES = {
    "Ashwini": "Ashwini Kumaras (Divine Physicians)",
    "Bharani": "Yama (Lord of Death)",
    "Krittika": "Agni (Fire)",
    "Rohini": "Prajapati (Creator)",
    "Mrigashira": "Soma (Moon God)",
    "Ardra": "Rudra (Storm God)",
    "Punarvasu": "Aditi (Mother of Gods)",
    "Pushya": "Brihaspati (Jupiter)",
    "Ashlesha": "Nagas (Serpent Deities)",
    "Magha": "Pitris (Ancestors)",
    "Purva Phalguni": "Bhaga (Prosperity)",
    "Uttara Phalguni": "Aryaman (Nobility)",
    "Hasta": "Savitar (Sun)",
    "Chitra": "Tvashtar (Celestial Architect)",
    "Swati": "Vayu (Wind)",
    "Vishakha": "Indra-Agni (King-Fire)",
    "Anuradha": "Mitra (Friendship)",
    "Jyeshtha": "Indra (King of Gods)",
    "Mula": "Nirriti (Dissolution)",
    "Purva Ashadha": "Apas (Waters)",
    "Uttara Ashadha": "Vishvadevas (Universal Gods)",
    "Shravana": "Vishnu (Preserver)",
    "Dhanishta": "Vasus (Elemental Deities)",
    "Shatabhisha": "Varuna (Cosmic Order)",
    "Purva Bhadrapada": "Aja Ekapada (One-footed Serpent)",
    "Uttara Bhadrapada": "Ahir Budhnya (Serpent of Depths)",
    "Revati": "Pushan (Nourisher)"
}

NAKSHATRA_THEMES = {
    "Ashwini": "Beginnings, swift action, healing",
    "Bharani": "Restraint, gestation, transformation",
    "Krittika": "Cutting away, purification",
    "Rohini": "Growth, fertility, beauty",
    "Mrigashira": "Searching, questing",
    "Ardra": "Storm, dissolution, renewal",
    "Punarvasu": "Return, restoration, renewal",
    "Pushya": "Nourishment, protection",
    "Ashlesha": "Coiling, entwining, occult knowledge",
    "Magha": "Ancestral power, throne",
    "Purva Phalguni": "Relaxation, pleasure",
    "Uttara Phalguni": "Contracts, commitments",
    "Hasta": "Skill, dexterity, manifestation",
    "Chitra": "Beauty, craftsmanship",
    "Swati": "Independence, movement",
    "Vishakha": "Goal-directed focus",
    "Anuradha": "Devotion, friendship",
    "Jyeshtha": "Seniority, protection",
    "Mula": "Roots, foundation, destruction",
    "Purva Ashadha": "Invincibility, victory",
    "Uttara Ashadha": "Final victory, permanence",
    "Shravana": "Listening, learning",
    "Dhanishta": "Wealth, rhythm",
    "Shatabhisha": "Healing, secrecy",
    "Purva Bhadrapada": "Purification, intensity",
    "Uttara Bhadrapada": "Depth, wisdom",
    "Revati": "Nourishment, completion"
}


def calculate_nakshatra(moon_longitude: float) -> Tuple[str, int, str, str]:
    """
    Deterministic Nakshatra calculation from Moon's ecliptic longitude.
    
    Returns: (nakshatra_name, pada [1-4], deity, theme)
    """
    # Each Nakshatra = 13.333333° (360° / 27)
    nakshatra_span = 360.0 / 27.0
    nakshatra_index = int(moon_longitude / nakshatra_span)
    nakshatra_index = min(nakshatra_index, 26)  # Cap at Revati
    
    nakshatra_name = NAKSHATRA_LIST[nakshatra_index]
    
    # Calculate pada (1-4)
    offset_in_nakshatra = moon_longitude - (nakshatra_index * nakshatra_span)
    pada = int(offset_in_nakshatra / (nakshatra_span / 4.0)) + 1
    pada = min(pada, 4)
    
    deity = NAKSHATRA_DEITIES.get(nakshatra_name, "Unknown")
    theme = NAKSHATRA_THEMES.get(nakshatra_name, "Unknown")
    
    return nakshatra_name, pada, deity, theme


def get_planet_position(jd: float, planet_const: int) -> float:
    """
    Get ecliptic longitude of a planet at Julian Day.
    Returns: longitude in degrees (0-360)
    """
    result, _ = swe.calc(jd, planet_const)
    return result[0]  # Longitude


def calculate_julian_day(dt: datetime) -> float:
    """Convert datetime to Julian Day (UT)"""
    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    )


# ============================================================================
# ARABIC LOTS (DETERMINISTIC FORMULAS)
# ============================================================================

def lot_of_fortune(asc: float, sun: float, moon: float, is_day_chart: bool) -> float:
    """
    Lot of Fortune = Asc + Moon - Sun (day chart)
                   = Asc + Sun - Moon (night chart)
    """
    if is_day_chart:
        return (asc + moon - sun) % 360
    else:
        return (asc + sun - moon) % 360


def lot_of_spirit(asc: float, sun: float, moon: float, is_day_chart: bool) -> float:
    """
    Lot of Spirit = Asc + Sun - Moon (day chart)
                  = Asc + Moon - Sun (night chart)
    """
    if is_day_chart:
        return (asc + sun - moon) % 360
    else:
        return (asc + moon - sun) % 360


def is_day_chart(sun_longitude: float, asc_longitude: float) -> bool:
    """Check if Sun is above horizon (day chart)"""
    # Sun above ASC-DESC axis = day chart
    desc = (asc_longitude + 180) % 360
    if asc_longitude < desc:
        return asc_longitude <= sun_longitude <= desc
    else:
        return sun_longitude >= asc_longitude or sun_longitude <= desc


# ============================================================================
# FIRDARIA CALCULATION (PERSIAN TIME-LORD SYSTEM)
# ============================================================================

FIRDARIA_SEQUENCE_DAY = [
    (Planet.SUN, 10),
    (Planet.VENUS, 8),
    (Planet.MERCURY, 13),
    (Planet.MOON, 9),
    (Planet.SATURN, 11),
    (Planet.JUPITER, 12),
    (Planet.MARS, 7),
]

FIRDARIA_SEQUENCE_NIGHT = [
    (Planet.MOON, 9),
    (Planet.SATURN, 11),
    (Planet.JUPITER, 12),
    (Planet.MARS, 7),
    (Planet.SUN, 10),
    (Planet.VENUS, 8),
    (Planet.MERCURY, 13),
]


def calculate_firdaria(current_age: float, is_day_birth: bool) -> Dict:
    """
    Calculate current Firdaria period.
    
    Args:
        current_age: Age in years
        is_day_birth: True if day chart, False if night chart
    
    Returns: {planet, start_age, end_age, archetypal_task}
    """
    sequence = FIRDARIA_SEQUENCE_DAY if is_day_birth else FIRDARIA_SEQUENCE_NIGHT
    
    # Firdaria cycle = 75 years
    age_in_cycle = current_age % 75.0
    
    age_cursor = 0.0
    for planet, duration in sequence:
        if age_cursor <= age_in_cycle < age_cursor + duration:
            return {
                "ruling_planet": planet.value,
                "start_age": age_cursor,
                "end_age": age_cursor + duration,
                "current_phase": True,
                "archetypal_task": get_firdaria_theme(planet)
            }
        age_cursor += duration
    
    # Fallback (shouldn't happen with modulo)
    return {
        "ruling_planet": Planet.SUN.value,
        "start_age": 0.0,
        "end_age": 10.0,
        "current_phase": True,
        "archetypal_task": "Authority, identity consolidation"
    }


def get_firdaria_theme(planet: Planet) -> str:
    """Archetypal themes for each Firdaria lord"""
    themes = {
        Planet.SUN: "Authority, identity consolidation",
        Planet.MOON: "Emotional tides, instinct",
        Planet.MERCURY: "Communication, skill acquisition",
        Planet.VENUS: "Relationships, pleasure",
        Planet.MARS: "Conflict, assertion",
        Planet.JUPITER: "Expansion, fortune",
        Planet.SATURN: "Restriction, crystallization"
    }
    return themes.get(planet, "Unknown")


def calculate_ascendant(jd: float, lat: float, lon: float) -> float:
    """Calculate Ascendant (rising sign) using Placidus house system"""
    try:
        houses, ascmc = swe.houses(jd, lat, lon, b'P')
        return ascmc[0]  # Ascendant
    except:
        return 0.0  # Fallback
